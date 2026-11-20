import type { Metadata } from "next";
import { toLocale } from "@/lib/i18n";
import { pageMetadata } from "@/lib/seo";

type Props = { params: Promise<{ lang: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return pageMetadata(toLocale((await params).lang), "acasa");
}

// Temporary home page for stage E0 (the foundation). The real Acasă is built in stage E2.
export default async function Home() {
  return (
    <main className="mx-auto grid min-h-dvh max-w-[1240px] place-content-center px-5 text-center">
      <h1 className="text-[clamp(56px,9vw,128px)] leading-[.95] tracking-[-0.025em]">AVA</h1>
      <p className="font-script text-[clamp(32px,4vw,48px)] text-terra">Art &amp; Soul</p>
      <p className="mt-4 text-ink2">autocunoaștere prin creație</p>
    </main>
  );
}
