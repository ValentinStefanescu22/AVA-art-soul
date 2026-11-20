import Link from "next/link";
import { LAYOUT_COPY } from "@/content/ro/layout";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import s from "./breadcrumb.module.css";

/**
 * „Ce oferim › Ateliere de grup” at the top of a service page's hero (desktop; on phones the same way back lives in
 * the header pill). Light text: it always sits on a dark hero.
 */
export function Breadcrumb({ lang, label }: { lang: Locale; label: string }) {
  return (
    <nav className={s.crumb} aria-label={LAYOUT_COPY.breadcrumb}>
      <ol>
        <li>
          <Link href={href(lang, "ceOferim")}>{LAYOUT_COPY.back}</Link>
        </li>
        <li aria-current="page">{label}</li>
      </ol>
    </nav>
  );
}
