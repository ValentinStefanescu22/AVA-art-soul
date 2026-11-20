import Link from "next/link";
import { Arrow } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { Picture } from "@/components/ui/Picture";
import { ATELIERE, type Atelier } from "@/content/ateliere";
import { HERO, PLACEHOLDER } from "@/content/ro/home/hero";
import { dateParts, upcoming } from "@/lib/dates";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import { HeroStamp } from "./HeroStamp";
import s from "./hero.module.css";

/** „duminică, 6 decembrie, ora 17:00” (or „ora [ORA]” while the time isn't set). */
export function stripDate(w: Atelier): string {
  const d = dateParts(w.date);
  return `${d.weekday}, ${d.day} ${d.month}, ${HERO.strip.at} ${w.time ?? PLACEHOLDER.time}`;
}

/** The next workshop, on top of the hero. Hidden when nothing is scheduled. */
function Strip({ lang, next }: { lang: Locale; next: Atelier }) {
  return (
    // data-hx-strip: the header pill starts below this strip (header.module.css)
    <p className={s.strip} data-hx-strip="">
      <span className={s.live} aria-hidden="true" />
      <b>{HERO.strip.label}</b>
      <i aria-hidden="true">·</i>
      <span className={s.num}>{stripDate(next)}</span>
      <i className={`${s.hide} ${s.hideNarrow}`} aria-hidden="true">
        ·
      </i>
      <span className={`${s.hide} ${s.hideNarrow}`}>{next.zone ?? PLACEHOLDER.zone}</span>
      <Link href={href(lang, "ateliereDeGrup")}>
        {next.soldOut ? HERO.strip.soldOut : HERO.strip.signUp}
        <Arrow />
      </Link>
    </p>
  );
}

export function Hero({ lang }: { lang: Locale }) {
  const next = upcoming(ATELIERE)[0];
  return (
    <div className={s.root}>
      {next && <Strip lang={lang} next={next} />}
      {/* data-hx-dark: the header shows cream text while it is over this section */}
      <section className={s.hero} id="top" data-hx-dark="">
        <Picture image="hero-lut" alt={HERO.photoAlt} sizes="100vw" priority className={s.photo} />
        <div className={s.stage}>
          <HeroStamp sealText={HERO.sealText} />
          <div className={s.copy}>
            <span className={`${s.soul} ${s.rise} ${s.d1}`} aria-hidden="true">
              {HERO.soul}
            </span>
            <h1 className={`${s.title} ${s.rise} ${s.d2}`}>
              <span className={s.srOnly}>{HERO.titleHidden}</span>
              <span className={s.nb}>{HERO.title[0]}</span> <span className={s.nb}>{HERO.title[1]}</span>
              <br /> <span className={s.nb}>{HERO.title[2]}</span>
            </h1>
            <p className={`${s.lede} ${s.rise} ${s.d3}`}>{HERO.lede}</p>
            <div className={`${s.ctas} ${s.rise} ${s.d4}`}>
              <Button variant="accentOnDark" href={href(lang, "ceOferim")}>
                {HERO.forYou}
              </Button>
              <Button variant="lineOnDark" href={href(lang, "pentruCompanii")}>
                {HERO.forCompanies}
              </Button>
            </div>
          </div>
        </div>
        <svg className={s.edge} viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true">
          <path d="M0 86C240 62 480 62 720 86C960 110 1200 110 1440 86L1440 120L0 120Z" fill="var(--color-paper)" />
        </svg>
      </section>
    </div>
  );
}
