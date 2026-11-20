"use client";

import Link from "next/link";
import { useState } from "react";
import { Picture } from "@/components/ui/Picture";
import { CE_OFERIM } from "@/content/ro/home/ce-oferim";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import s from "./ce-oferim.module.css";

/**
 * Horizontal accordion of photo panels. Client component only because hover / focus / click
 * pick the open panel (`data-a`); every panel is a real link, so it works without the accordion too.
 */
export function CeOferim({ lang, className }: { lang: Locale; className?: string }) {
  const [active, setActive] = useState(0);
  return (
    <section className={[s.cf, className].filter(Boolean).join(" ")} id="ce-facem" aria-labelledby="cf-h">
      <div className={s.wrap}>
        <div className={s.head} data-reveal="">
          <h2 id="cf-h">{CE_OFERIM.title}</h2>
          <p>{CE_OFERIM.lede}</p>
        </div>
        <div className={s.panels} data-a={active} data-reveal="">
          {CE_OFERIM.panels.map((p, i) => (
            <Link
              key={p.page}
              className={s.p}
              href={href(lang, p.page)}
              data-active={i === active}
              onMouseEnter={() => setActive(i)}
              onFocus={() => setActive(i)}
              onClick={() => setActive(i)}
            >
              <Picture
                image={p.image}
                alt={p.alt}
                sizes="(max-width: 820px) 100vw, 60vw"
                style={{ objectPosition: p.position }}
              />
              <span className={s.vl} aria-hidden="true">
                {p.name}
              </span>
              <span className={s.tx}>
                <span className={s.m}>{p.meta}</span>
                <span className={s.n}>{p.name}</span>
                <span className={s.l}>{p.text}</span>
                <span className={s.cta}>{p.cta}</span>
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
