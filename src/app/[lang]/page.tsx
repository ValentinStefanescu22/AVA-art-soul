import type { Metadata } from "next";
import { CeOferim } from "@/components/home/CeOferim";
import { Coperta } from "@/components/home/Coperta";
import { FaqAcasa } from "@/components/home/FaqAcasa";
import { Hero } from "@/components/home/Hero";
import { PopupNewsletter } from "@/components/home/PopupNewsletter";
import { Testimoniale } from "@/components/home/Testimoniale";
import { UrmatorulAtelier } from "@/components/home/UrmatorulAtelier";
import { toLocale } from "@/lib/i18n";
import { pageMetadata } from "@/lib/seo";
import s from "./page.module.css";

type Props = { params: Promise<{ lang: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return pageMetadata(toLocale((await params).lang), "acasa");
}

/** Acasă, in the order of the approved canvas page „Acasă: lucru”. The footer comes from the layout. */
export default async function Home({ params }: Props) {
  const lang = toLocale((await params).lang);
  return (
    <>
      <Hero lang={lang} />
      <Coperta lang={lang} className={s.despre} />
      <CeOferim lang={lang} className={s.ceOferim} />
      <UrmatorulAtelier lang={lang} className={s.urmator} />
      <Testimoniale lang={lang} className={s.oameni} />
      <FaqAcasa lang={lang} className={s.faq} />
      <PopupNewsletter lang={lang} />
    </>
  );
}
