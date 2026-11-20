import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PUBLISHED_LOCALES, toLocale } from "@/lib/i18n";
import { PAGES, segments, type PageKey } from "@/lib/routes";
import { pageMeta, pageMetadata } from "@/lib/seo";

// Temporary pages for everything in routes.ts that isn't built yet, so the menu and footer never lead to a 404.
// Each stage that builds a real page removes it from PENDING (the real route folder then takes over).
const BUILT: readonly PageKey[] = ["acasa", "despreNoi", "ceOferim"];
export const PENDING: readonly PageKey[] = (Object.keys(PAGES) as PageKey[]).filter((k) => !BUILT.includes(k));

export const dynamicParams = false;
export function generateStaticParams() {
  return PUBLISHED_LOCALES.flatMap((lang) => PENDING.map((page) => ({ lang, slug: segments(page) })));
}

type Props = { params: Promise<{ lang: string; slug: string[] }> };

function pageOf(slug: string[]): PageKey {
  const key = PENDING.find((k) => PAGES[k].path === slug.join("/"));
  if (!key) notFound();
  return key;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang, slug } = await params;
  // Never indexed, whatever the launch switch says: these are not real pages.
  return { ...pageMetadata(toLocale(lang), pageOf(slug)), robots: { index: false, follow: false } };
}

export default async function PendingPage({ params }: Props) {
  const { lang, slug } = await params;
  const { title } = pageMeta(toLocale(lang), pageOf(slug));
  return (
    <div className="mx-auto grid min-h-[70dvh] max-w-[1240px] place-content-center px-5 pt-28 text-center">
      <h1 className="text-[clamp(40px,4.4vw,64px)] leading-[1.05]">{title}</h1>
      <p className="mt-4 text-ink2">Pagina e în lucru.</p>
    </div>
  );
}
