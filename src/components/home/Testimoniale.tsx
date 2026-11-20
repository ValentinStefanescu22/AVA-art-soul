import Link from "next/link";
import { Arrow } from "@/components/icons";
import { Picture } from "@/components/ui/Picture";
import { OAMENI } from "@/content/ro/home/oameni";
import { CONTACT } from "@/content/ro/layout";
import { TESTIMONIALE } from "@/content/testimoniale";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import { Carousel, type CarouselCopy } from "./Carousel";
import s from "./testimoniale.module.css";

/** A band of photos that drifts sideways forever: the list twice, the copy hidden from screen readers. */
function Band({ items, className }: { items: (typeof OAMENI)["bandTop" | "bandBottom"]; className?: string }) {
  return (
    <div className={`${s.mq} ${className}`}>
      <ul>
        {[...items, ...items].map((it, i) => {
          const twin = i >= items.length;
          return (
            <li key={i} aria-hidden={twin || undefined}>
              <Picture
                image={it.image}
                alt={twin ? "" : it.alt}
                sizes="(max-width: 820px) 255px, 375px"
                style={{ objectPosition: it.position }}
              />
            </li>
          );
        })}
      </ul>
    </div>
  );
}

/** „Ce spun oamenii” on Acasă: testimonials (src/content/testimoniale.ts) between two bands of workshop photos. */
export function Testimoniale({ lang, className }: { lang: Locale; className?: string }) {
  const head = (
    <div className={s.wrap} data-reveal="">
      <div className={s.head}>
        <h2 id="og-h">{OAMENI.title}</h2>
        <div className={s.links}>
          <Link className={s.more} href={href(lang, "galerie")}>
            {OAMENI.gallery} <Arrow className={s.ar} />
          </Link>
          <a className={s.more} href={CONTACT.instagram.href}>
            {OAMENI.instagram(CONTACT.instagram.handle)} <Arrow className={s.ar} />
          </a>
        </div>
      </div>
    </div>
  );
  const n = TESTIMONIALE.length;
  const copy: CarouselCopy = {
    carousel: OAMENI.carousel,
    carouselLabel: OAMENI.carouselLabel,
    slide: OAMENI.slide,
    slideLabels: TESTIMONIALE.map((_, i) => OAMENI.slideLabel(i + 1, n)),
    dots: TESTIMONIALE.map((_, i) => OAMENI.dot(i + 1)),
    prev: OAMENI.prev,
    next: OAMENI.next,
    stop: OAMENI.stop,
    start: OAMENI.start,
  };
  return (
    <Carousel
      className={className}
      quotes={TESTIMONIALE}
      copy={copy}
      head={head}
      bandTop={<Band items={OAMENI.bandTop} className={s.r1} />}
      bandBottom={<Band items={OAMENI.bandBottom} className={s.r2} />}
    />
  );
}
