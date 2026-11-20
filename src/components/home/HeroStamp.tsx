"use client";

import { useEffect, useRef, type RefObject } from "react";
import s from "./hero.module.css";

/** Natural frequency of the light's spring (rad/s): it settles in about half a second, without overshoot. */
const W = (2 * Math.PI) / 0.45;

/**
 * One step of a critically damped spring (no bounce): moves `p` (position + velocity) toward `target`.
 * Exported for the unit test.
 */
export function springStep(p: { x: number; v: number }, target: number, dt: number) {
  p.v += (W * W * (target - p.x) - 2 * W * p.v) * dt;
  p.x += p.v * dt;
}

/** How far each layer of the pressed stamp shifts away from the light (px in the 480 viewBox), 0→1 press. */
export function imprint(dx: number, dy: number, radius: number, press: number) {
  const dist = Math.hypot(dx, dy) || 1;
  const low = Math.max(0, Math.min(1, (dist / radius - 0.2) / 1.3)); // a far, low light makes longer shadows
  return {
    ux: -dx / dist,
    uy: -dy / dist,
    shade: (1.2 + 1.4 * low) * press,
    lip: (0.9 + 1 * low) * press,
    wall: (3.2 + 2.4 * low) * press,
    far: 1.1 * press,
  };
}

const STROKE = { fill: "none", stroke: "currentColor" } as const;

/**
 * The brand stamp pressed into the clay, lit by the woodsprite. The light follows the mouse on a spring (or circles
 * the stamp slowly when there's no mouse); the imprint's shadow, soft wall, far wall and bright lip are copies of
 * the same shapes inside SVG masks, shifted away from the light every frame. On load the stamp "presses" in.
 * No feDiffuseLighting: Chrome renders it at viewBox resolution, blurry on Retina (CLAUDE.md).
 */
export function HeroStamp({ sealText }: { sealText: string }) {
  const stamp = useRef<HTMLDivElement>(null);
  const sprite = useRef<HTMLSpanElement>(null);
  const glow = useRef<HTMLDivElement>(null);
  const shade = useRef<SVGGElement>(null);
  const lip = useRef<SVGGElement>(null);
  const wall = useRef<SVGGElement>(null);
  const far = useRef<SVGGElement>(null);

  useEffect(() => {
    const st = stamp.current;
    const hero = st?.closest("section");
    if (!st || !hero) return;
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const target = { x: 0, y: 0, on: false };
    const px = { x: 0, v: 0 };
    const py = { x: 0, v: 0 };
    let started = false;
    let pressed = false;
    let raf = 0;
    let visible = true;
    const t0 = performance.now();
    let last = t0;

    const move = (el: SVGGElement | null, k: number, ux: number, uy: number) =>
      el?.setAttribute("transform", `translate(${(ux * k).toFixed(2)} ${(uy * k).toFixed(2)})`);

    const tick = (now: number) => {
      raf = 0;
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      const h = hero.getBoundingClientRect();
      const sr = st.getBoundingClientRect();
      const c = { x: sr.left - h.left + sr.width / 2, y: sr.top - h.top + sr.height / 2, r: sr.width / 2 };
      if (!target.on) {
        const a = -2.35 + ((now - t0) / 1000) * 0.12;
        target.x = c.x + Math.cos(a) * c.r * 1.25;
        target.y = c.y + Math.sin(a) * c.r * 1.25;
      }
      if (!started) {
        px.x = target.x;
        py.x = target.y;
        started = true;
      }
      springStep(px, target.x, dt);
      springStep(py, target.y, dt);

      sprite.current?.style.setProperty("transform", `translate3d(${px.x.toFixed(1)}px,${py.x.toFixed(1)}px,0)`);
      const g = glow.current?.style;
      g?.setProperty("--lx", `${px.x.toFixed(1)}px`);
      g?.setProperty("--ly", `${py.x.toFixed(1)}px`);
      g?.setProperty("--lr", `${Math.max(200, Math.min(380, h.width * 0.24)).toFixed(0)}px`);

      let press = reduce ? 1 : Math.min(1, Math.max(0, (now - t0 - 150) / 1300));
      press = 1 - Math.pow(1 - press, 3); // ease-out
      const k = imprint(px.x - c.x, py.x - c.y, c.r, press);
      move(shade.current, k.shade, k.ux, k.uy);
      move(lip.current, k.lip, k.ux, k.uy);
      move(wall.current, k.wall, k.ux, k.uy);
      move(far.current, -k.far, k.ux, k.uy);
      if (!pressed) {
        st.style.transform = press < 1 ? `scale(${(1 + 0.035 * (1 - press)).toFixed(4)})` : "";
        pressed = press >= 1;
      }
      // With reduced motion one frame draws the finished imprint and the light stays put.
      if (!reduce && visible) raf = requestAnimationFrame(tick);
    };

    const onMove = (e: PointerEvent) => {
      const h = hero.getBoundingClientRect();
      target.x = e.clientX - h.left;
      target.y = e.clientY - h.top;
      target.on = e.pointerType === "mouse" && target.y < h.height;
    };
    const onLeave = () => {
      target.on = false;
    };
    // Stop drawing while the hero is off screen.
    const io = new IntersectionObserver(([e]) => {
      visible = !!e?.isIntersecting;
      if (visible && !raf && !reduce) {
        last = performance.now();
        raf = requestAnimationFrame(tick);
      }
    });
    io.observe(hero);
    hero.addEventListener("pointermove", onMove);
    hero.addEventListener("pointerleave", onLeave);
    raf = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
      hero.removeEventListener("pointermove", onMove);
      hero.removeEventListener("pointerleave", onLeave);
    };
  }, []);

  return (
    <>
      <div ref={glow} className={s.glow} aria-hidden="true" />
      <span ref={sprite} className={s.sprite} aria-hidden="true" />
      <div ref={stamp} className={s.seal} aria-hidden="true">
        {/* ambient occlusion: a blurred dark copy under everything */}
        <svg className={s.ao} viewBox="0 0 480 480">
          <filter id="hs-ao" x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation="2.4" />
          </filter>
          <g {...STROKE} style={{ filter: "url(#hs-ao)", color: "#1A0F08", stroke: "#1A0F08" }}>
            <use href="#hs-shapes" />
          </g>
        </svg>
        <svg viewBox="0 0 480 480">
          <defs>
            <path id="hs-ring" d="M240 240m-156 0a156 156 0 1 1 312 0a156 156 0 1 1 -312 0" />
            <g id="hs-shapes">
              <circle cx="240" cy="240" r="214" strokeWidth={7.5} />
              <circle cx="240" cy="240" r="198" strokeWidth={3} />
              <circle cx="240" cy="240" r="132" strokeWidth={4.5} />
              <text stroke="none" fill="currentColor" style={{ font: "600 34px var(--font-text)" }}>
                <textPath href="#hs-ring" textLength={965} lengthAdjust="spacing">
                  {sealText}
                </textPath>
              </text>
              <g transform="translate(176 156) scale(2)" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 6H42" strokeWidth={5} />
                <path
                  d="M26 7C26 13 27 15 25 18C17 24 12 31 12 43C12 55 19 64 24 72H40C45 64 52 55 52 43C52 31 47 24 39 18C37 15 38 13 38 7"
                  strokeWidth={3.6}
                />
                <path d="M14.5 35Q32 40 49.5 35M12.6 48Q32 53 51.4 48" strokeWidth={3.2} />
              </g>
            </g>
            <filter id="hs-soft" x="-5%" y="-5%" width="110%" height="110%">
              <feGaussianBlur stdDeviation="1.4" />
            </filter>
            <Mask id="hs-groove" />
            <Mask id="hs-wall" cut={wall} />
            <Mask id="hs-shade" cut={shade} />
            <Mask id="hs-far" cut={far} />
            <mask id="hs-lip" maskUnits="userSpaceOnUse" x="-20" y="-20" width="520" height="520">
              <g ref={lip} {...STROKE} stroke="#fff" color="#fff">
                <use href="#hs-shapes" />
              </g>
              <g {...STROKE} stroke="#000" color="#000">
                <use href="#hs-shapes" />
              </g>
            </mask>
          </defs>
          {/* the bottom of the groove */}
          <g {...STROKE} style={{ stroke: "rgba(20,11,6,.45)", color: "rgba(20,11,6,.45)" }}>
            <use href="#hs-shapes" />
          </g>
          {/* soft shaded wall, cut to the groove */}
          <g mask="url(#hs-groove)">
            <g style={{ filter: "url(#hs-soft)" }}>
              <rect x="-20" y="-20" width="520" height="520" mask="url(#hs-wall)" fill="rgba(12,6,3,.75)" />
            </g>
          </g>
          {/* crisp shadow, lit far wall, bright lip on the light's side */}
          <rect x="-20" y="-20" width="520" height="520" mask="url(#hs-shade)" fill="rgba(10,5,2,.88)" />
          <rect x="-20" y="-20" width="520" height="520" mask="url(#hs-far)" fill="rgba(255,206,160,.26)" />
          <rect x="-20" y="-20" width="520" height="520" mask="url(#hs-lip)" fill="rgba(255,214,170,.6)" />
        </svg>
      </div>
    </>
  );
}

/** A mask showing the stamp's shapes, minus (optionally) a shifted copy of them: the sliver between is the effect. */
function Mask({ id, cut }: { id: string; cut?: RefObject<SVGGElement | null> }) {
  return (
    <mask id={id} maskUnits="userSpaceOnUse" x="-20" y="-20" width="520" height="520">
      <g {...STROKE} stroke="#fff" color="#fff">
        <use href="#hs-shapes" />
      </g>
      {cut && (
        <g ref={cut} {...STROKE} stroke="#000" color="#000">
          <use href="#hs-shapes" />
        </g>
      )}
    </mask>
  );
}
