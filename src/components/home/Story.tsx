"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import { Picture } from "@/components/ui/Picture";
import type { ImageKey } from "@/generated/images";
import s from "./urmatorul-atelier.module.css";

export type StoryFrame = { image: ImageKey; alt: string; position: string; cover?: boolean; content: ReactNode };

type Props = { frames: StoryFrame[]; who: ReactNode; labels: { prev: string; next: string } };

function Chevron() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <path
        d="M6 3.5L10.5 8L6 12.5"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/**
 * The photo story beside the workshop card. A CSS fill animation on the current bar times each frame; when it ends,
 * the next frame comes. It starts from the first frame whenever the story comes into view and stops when it leaves.
 * A finger held down pauses it. With reduced motion nothing plays by itself; the arrows and tap zones still work.
 */
export function Story({ frames, who, labels }: Props) {
  const n = frames.length;
  const [a, setA] = useState(0);
  const [run, setRun] = useState(false);
  const [cycle, setCycle] = useState(0); // remounts the bars, so a restart on frame 0 replays its animation
  const [hold, setHold] = useState(false);
  const sy = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = sy.current;
    if (!el || !("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const io = new IntersectionObserver(
      ([e]) => {
        if (!e) return;
        if (e.isIntersecting) {
          setA(0);
          setCycle((c) => c + 1);
        }
        setRun(e.isIntersecting);
      },
      { threshold: 0.5 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const step = (d: number) => setA((x) => (x + d + n) % n);
  const release = () => setHold(false);

  return (
    <div className={s.sw} data-reveal="">
      <button
        className={`${s.arw} ${s.pv}`}
        type="button"
        aria-label={labels.prev}
        onClick={() => step(-1)}
        aria-hidden={a === 0 || undefined}
        tabIndex={a === 0 ? -1 : undefined}
      >
        <Chevron />
      </button>
      <div
        ref={sy}
        className={s.sy}
        data-hold={hold || undefined}
        onPointerDown={() => setHold(true)}
        onPointerUp={release}
        onPointerLeave={release}
        onPointerCancel={release}
      >
        <div className={s.ph}>
          {frames.map((f, i) => (
            <Picture
              key={i}
              image={f.image}
              alt={f.alt}
              sizes="(max-width: 820px) min(100vw - 40px, 360px), 400px"
              className={i === a ? s.on : undefined}
              style={{ objectPosition: f.position }}
            />
          ))}
        </div>
        <span className={s.shade} aria-hidden="true" />
        <div className={s.bars} aria-hidden="true" key={cycle}>
          {frames.map((_, i) => (
            <span key={i} className={s.bar}>
              <i
                className={i === a && run ? s.fill : i <= a ? s.full : undefined}
                onAnimationEnd={i === a ? () => step(1) : undefined}
              />
            </span>
          ))}
        </div>
        {who}
        <button
          className={`${s.nav} ${s.p}`}
          type="button"
          aria-label={labels.prev}
          tabIndex={-1}
          onClick={() => step(-1)}
        />
        <button
          className={`${s.nav} ${s.n}`}
          type="button"
          aria-label={labels.next}
          tabIndex={-1}
          onClick={() => step(1)}
        />
        {frames.map((f, i) => (
          <div
            key={i}
            className={[s.fr, f.cover && s.cover, i === a && s.on].filter(Boolean).join(" ")}
            inert={i !== a}
          >
            {f.content}
          </div>
        ))}
      </div>
      <button className={`${s.arw} ${s.nx}`} type="button" aria-label={labels.next} onClick={() => step(1)}>
        <Chevron />
      </button>
    </div>
  );
}
