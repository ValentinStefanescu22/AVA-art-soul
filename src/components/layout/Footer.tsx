import Link from "next/link";
import { Vase } from "@/components/icons";
import { CONTACT, INFO, LAYOUT_COPY, LEGAL, NAV, SERVICES } from "@/content/ro/layout";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import { NewsletterForm } from "./NewsletterForm";
import s from "./footer.module.css";

/** The ceramic stamp beside the newsletter: the brand line written around a circle, the vase in the middle. */
function Seal() {
  return (
    <svg className={s.seal} viewBox="0 0 120 120" width="120" height="120" aria-hidden="true">
      <defs>
        <path id="ft-seal-ring" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0" />
      </defs>
      <circle cx="60" cy="60" r="57" fill="none" stroke="currentColor" strokeWidth={1.4} />
      <circle cx="60" cy="60" r="34" fill="none" stroke="currentColor" strokeWidth={1.1} />
      <text style={{ font: "600 7.4px var(--font-text)" }} fill="currentColor">
        <textPath href="#ft-seal-ring" textLength={272} lengthAdjust="spacing">
          {LAYOUT_COPY.footer.sealText}
        </textPath>
      </text>
      <svg x="38" y="34" width="44" height="52" viewBox="0 0 64 80">
        <Vase />
      </svg>
    </svg>
  );
}

export function Footer({ lang }: { lang: Locale }) {
  const copy = LAYOUT_COPY.footer;
  const columns = [
    { title: copy.columns.nav, links: NAV },
    { title: copy.columns.services, links: SERVICES },
    { title: copy.columns.info, links: INFO },
  ];
  return (
    <footer className={s.footer} id="newsletter" aria-label={copy.label}>
      <div className={s.wrap}>
        <div className={s.card} data-reveal="">
          <div className={s.left}>
            <h2 className={s.title}>{copy.newsletterTitle}</h2>
            <p className={s.lead}>{copy.newsletterLead}</p>
            <p className={s.sig}>{copy.signature}</p>
          </div>
          <div className={s.right}>
            <Seal />
            <NewsletterForm id="ft-nl" copy={LAYOUT_COPY.newsletter} privacyHref={href(lang, "confidentialitate")} />
          </div>
        </div>

        <div className={s.dark}>
          <div className={s.grid}>
            <div className={s.brand} data-reveal="">
              <Link className={s.flogo} href={href(lang, "acasa")}>
                <Vase />
                <span>
                  <span className={s.fword}>AVA</span> <span className={s.fsub}>ART &amp; SOUL</span>
                </span>
              </Link>
              <p className={s.tag}>{LAYOUT_COPY.tagline}</p>
            </div>
            {columns.map((c) => (
              <nav key={c.title} className={s.col} aria-label={c.title} data-reveal="">
                <p className={s.colTitle}>{c.title}</p>
                <ul>
                  {c.links.map((l) => (
                    <li key={l.page}>
                      <Link href={href(lang, l.page)}>{l.label}</Link>
                    </li>
                  ))}
                </ul>
              </nav>
            ))}
            <div className={`${s.col} ${s.contactCol}`} data-reveal="">
              <p className={s.colTitle}>{copy.columns.contact}</p>
              <ul>
                <li>
                  <a href={`mailto:${CONTACT.email}`}>{CONTACT.email}</a>
                </li>
                <li>
                  <a href={CONTACT.phone.href}>{CONTACT.phone.display}</a>
                </li>
                <li>
                  <a href={CONTACT.instagram.href} rel="noopener">
                    {CONTACT.instagram.handle}
                  </a>
                </li>
                <li>
                  <span>{CONTACT.area}</span>
                </li>
              </ul>
            </div>
          </div>
          <div className={s.legal}>
            <p>
              © {new Date().getFullYear()} AVA Art &amp; Soul · {LEGAL.company} · CUI {LEGAL.cui} · Reg. Com.{" "}
              {LEGAL.regCom} · Sediu: {LEGAL.office} · {CONTACT.email}
            </p>
            <a className={s.anpc} href={LEGAL.anpc.href} rel="noopener">
              {LEGAL.anpc.label}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
