"use client";

import Link from "next/link";
import { useState } from "react";
import { Arrow } from "@/components/icons";
import { Picture } from "@/components/ui/Picture";
import { COPERTA } from "@/content/ro/home/coperta";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import s from "./coperta.module.css";

/**
 * „Despre”: Alessia between her two roles. Client component only because hover / focus / click on a role
 * highlights it (`data-r` on the section, `aria-pressed` on the buttons).
 */
export function Coperta({ lang, className }: { lang: Locale; className?: string }) {
  const [role, setRole] = useState(0);
  const [a, b] = COPERTA.roles;
  const roleButton = (i: 0 | 1, r: typeof a | typeof b) => (
    <button
      type="button"
      className={`${s.rb} ${i === 0 ? s.a : s.b}`}
      aria-pressed={role === i}
      onMouseEnter={() => setRole(i)}
      onFocus={() => setRole(i)}
      onClick={() => setRole(i)}
      data-reveal=""
      data-reveal-from={i === 0 ? "left" : "right"}
    >
      <span className={s.w}>{r.word}</span>
      <span className={s.d}>{r.detail}</span>
    </button>
  );
  return (
    <section
      className={[s.cv, className].filter(Boolean).join(" ")}
      id="despre"
      aria-labelledby="despre-h"
      data-r={role}
    >
      <p className={s.name} aria-hidden="true" data-reveal="">
        {COPERTA.name}
      </p>
      <div className={`${s.wrap} ${s.stage}`}>
        {roleButton(0, a)}
        <figure className={s.fig} data-reveal="">
          <Picture image="alessia" alt={COPERTA.photoAlt} sizes="(max-width: 980px) 420px, 500px" />
        </figure>
        {roleButton(1, b)}
      </div>
      <div className={`${s.wrap} ${s.cap}`}>
        <h2 id="despre-h" data-reveal="">
          {COPERTA.headingStart}
          <em>{COPERTA.headingEm}</em>
          {COPERTA.headingEnd}
        </h2>
        <p className={s.body} data-reveal="">
          {COPERTA.body}
        </p>
        <Link className={s.more} href={href(lang, "despreNoi")} data-reveal="">
          {COPERTA.link} <Arrow className={s.ar} />
        </Link>
      </div>
    </section>
  );
}
