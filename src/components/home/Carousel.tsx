"use client";

import { useEffect, useRef, useState, useSyncExternalStore, type CSSProperties, type ReactNode } from "react";
import type { Testimonial } from "@/content/testimoniale";
import s from "./testimoniale.module.css";

/** Plain strings only: this crosses from the server to the browser. */
export type CarouselCopy = {
  carousel: string;
  carouselLabel: string;
  slide: string;
  /** One per testimonial: „1 din 4”… */
  slideLabels: string[];
  /** One per testimonial: „Testimonialul 1”… */
  dots: string[];
  prev: string;
  next: string;
  stop: string;
  start: string;
};

type Props = {
  quotes: readonly Testimonial[];
  copy: CarouselCopy;
  /** Server-rendered parts around the carousel: the heading row and the two photo bands. */
  head: ReactNode;
  bandTop: ReactNode;
  bandBottom: ReactNode;
  className?: string;
};

const cx = (...names: (string | false | undefined)[]) => names.filter(Boolean).join(" ");

// Read once on the client; the server (and the first paint) assume reduced motion, so nothing autoplays before we know.
const noSubscribe = () => () => {};
const prefersReduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

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
 * „Ce spun oamenii”: one testimonial at a time. It moves on by itself when the progress bar under the dots fills
 * (a CSS animation), pauses while the pointer or focus is on it and while it is off screen, and stops for good once
 * the visitor uses the arrows, the dots, a swipe or ← → (W3C APG carousel). With reduced motion it never moves by itself.
 */
export function Carousel({ quotes, copy, head, bandTop, bandBottom, className }: Props) {
  const n = quotes.length;
  const reduce = useSyncExternalStore(noSubscribe, prefersReduced, () => true);
  const [{ a, out, dir }, setPos] = useState({ a: 0, out: -1, dir: 1 });
  const [took, setTook] = useState(false);
  const [hold, setHold] = useState(false);
  const [off, setOff] = useState(false);
  const [still, setStill] = useState(false);
  const run = !reduce && !took;
  const stage = useRef<HTMLDivElement>(null);
  const x0 = useRef<number | null>(null);
  const swipedAt = useRef(-Infinity);

  useEffect(() => {
    const el = stage.current;
    if (!el || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver(([e]) => e && setOff(!e.isIntersecting), { threshold: 0.3 });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const go = (i: number, d: number) => setPos((p) => (i === p.a ? p : { a: i, out: p.a, dir: d }));
  const user = (d: number) => {
    setTook(true);
    go((a + d + n) % n, d);
  };
  const pick = (i: number, at: number) => {
    if (at - swipedAt.current < 400) return; // the tap that ended a swipe
    setTook(true);
    go(i, i > a ? 1 : -1);
  };

  return (
    <section
      className={cx(s.og, className)}
      id="oameni"
      aria-labelledby="og-h"
      data-hold={hold || undefined}
      data-still={still || undefined}
      data-off={off || undefined}
      style={{ "--d": dir } as CSSProperties}
    >
      {head}
      {bandTop}
      <div
        ref={stage}
        className={s.stage}
        role="region"
        aria-roledescription={copy.carousel}
        aria-label={copy.carouselLabel}
        data-reveal=""
        onKeyDown={(e) => {
          if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
          e.preventDefault();
          user(e.key === "ArrowLeft" ? -1 : 1);
        }}
        // Swipe on touch screens (the mouse uses the arrows).
        onPointerDown={(e) => (x0.current = e.pointerType === "mouse" ? null : e.clientX)}
        onPointerUp={(e) => {
          if (x0.current === null) return;
          const dx = e.clientX - x0.current;
          x0.current = null;
          if (Math.abs(dx) > 40) {
            swipedAt.current = e.timeStamp;
            user(dx < 0 ? 1 : -1);
          }
        }}
        onPointerCancel={() => (x0.current = null)}
        onPointerEnter={(e) => e.pointerType === "mouse" && setHold(true)}
        onPointerLeave={(e) => e.pointerType === "mouse" && setHold(false)}
        onFocus={() => setHold(true)}
        onBlur={(e) => !e.currentTarget.contains(e.relatedTarget as Node | null) && setHold(false)}
      >
        <div className={s.segs}>
          {quotes.map((_, i) => (
            <button
              key={i}
              className={s.seg}
              type="button"
              aria-label={copy.dots[i]}
              aria-current={i === a || undefined}
              onClick={(e) => pick(i, e.timeStamp)}
            >
              <span>
                <i
                  className={cx(s.tk, i === a && run ? s.tick : i <= a && s.full)}
                  onAnimationEnd={i === a && run ? () => go((a + 1) % n, 1) : undefined}
                />
              </span>
            </button>
          ))}
        </div>
        <div className={s.sls} aria-live={run ? "off" : "polite"}>
          {quotes.map((q, i) => (
            <div
              key={i}
              className={cx(s.sl, i === a && s.on, i === out && s.out)}
              role="group"
              aria-roledescription={copy.slide}
              aria-label={copy.slideLabels[i]}
            >
              <figure className={s.q}>
                <blockquote>{q.quote}</blockquote>
                <figcaption>
                  <b>{q.name}</b>
                </figcaption>
              </figure>
            </div>
          ))}
        </div>
        <button className={cx(s.rd, s.pv)} type="button" aria-label={copy.prev} onClick={() => user(-1)}>
          <Chevron />
        </button>
        <button className={cx(s.rd, s.nx)} type="button" aria-label={copy.next} onClick={() => user(1)}>
          <Chevron />
        </button>
      </div>
      {bandBottom}
      <div className={cx(s.wrap, s.stillrow)} data-reveal="">
        <button className={s.still} type="button" aria-pressed={still} onClick={() => setStill((v) => !v)}>
          <svg viewBox="0 0 16 16" aria-hidden="true">
            {still ? (
              <path d="M5 3.2v9.6L12.6 8z" fill="currentColor" />
            ) : (
              <path d="M5 3.5v9M11 3.5v9" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" />
            )}
          </svg>
          <span>{still ? copy.start : copy.stop}</span>
        </button>
      </div>
    </section>
  );
}
