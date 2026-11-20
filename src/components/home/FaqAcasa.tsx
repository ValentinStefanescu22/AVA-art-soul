import { Arrow } from "@/components/icons";
import { FAQ } from "@/content/ro/home/faq";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import Link from "next/link";
import s from "./faq-acasa.module.css";

/** Three questions as native <details> sharing a `name`: the browser keeps only one open, no JS. */
export function FaqAcasa({ lang, className }: { lang: Locale; className?: string }) {
  return (
    <section className={[s.fq, className].filter(Boolean).join(" ")} id="intrebari" aria-labelledby="fq-h">
      <div className={s.wrap}>
        <div className={s.head} data-reveal="">
          <h2 id="fq-h">{FAQ.title}</h2>
        </div>
        <div className={s.cards}>
          <div className={s.acc}>
            {FAQ.items.map((item, i) => (
              <details key={item.q} name="faq-acasa" open={i === 0} data-reveal="">
                <summary>
                  <span className={s.qq}>{item.q}</span>
                  <span className={s.ic} aria-hidden="true">
                    <svg viewBox="0 0 16 16">
                      <path d="M3 8H13" />
                      <path className={s.v} d="M8 3V13" />
                    </svg>
                  </span>
                </summary>
                <div className={s.ans}>
                  <p>
                    {item.a.map((part, k) =>
                      typeof part === "string" ? (
                        part
                      ) : (
                        <Link key={k} href={href(lang, part.page)}>
                          {part.text}
                        </Link>
                      ),
                    )}
                  </p>
                </div>
              </details>
            ))}
          </div>
          <aside className={s.other} aria-label={FAQ.other.ask} data-reveal="">
            <p className={s.ask}>{FAQ.other.ask}</p>
            <p className={s.reply}>{FAQ.other.reply}</p>
            <div className={s.links}>
              <Link className={s.more} href={href(lang, "contact")}>
                {FAQ.other.write} <Arrow className={s.ar} />
              </Link>
              <Link className={s.more} href={href(lang, "intrebariFrecvente")}>
                {FAQ.other.all} <Arrow className={s.ar} />
              </Link>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}
