import type { Metadata } from "next";
import { ServiceTabs } from "@/components/ce-oferim/ServiceTabs";
import { Letters } from "@/components/ui/Letters";
import { CE_OFERIM } from "@/content/ro/ce-oferim";
import { toLocale } from "@/lib/i18n";
import { pageMetadata } from "@/lib/seo";
import s from "./page.module.css";

type Props = { params: Promise<{ lang: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return pageMetadata(toLocale((await params).lang), "ceOferim");
}

/**
 * Ce oferim, as on the approved canvas page „Ce oferim: lucru”: the title over a brown that melts into cream, the
 * tabs with the service cards, then „De ce să alegi AVA Art & Soul?”. The footer comes from the layout.
 */
export default async function CeOferim({ params }: Props) {
  const lang = toLocale((await params).lang);
  const { title, lede, tabsLabel, tabs, deCe } = CE_OFERIM;
  return (
    <>
      <section className={s.hero} aria-labelledby="cp-h" data-hx-dark="">
        <div className={s.wrap}>
          <h1 className={s.title} id="cp-h" aria-label={title}>
            <Letters text={title} />
          </h1>
          <p className={s.lede}>{lede}</p>
          <div className={s.tabs}>
            <ServiceTabs lang={lang} label={tabsLabel} tabs={tabs} />
          </div>
        </div>
      </section>

      <section className={s.deCe} aria-labelledby="cw-h">
        <div className={s.wrap}>
          <h2 id="cw-h" data-reveal="">
            {deCe.title}
          </h2>
          <p className={s.todo} data-reveal="">
            {deCe.text}
          </p>
        </div>
      </section>
    </>
  );
}
