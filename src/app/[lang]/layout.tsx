import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import "../globals.css";
import { bodoni, literata, pinyon } from "@/lib/fonts";
import { LANG_TAG, PUBLISHED_LOCALES, toLocale } from "@/lib/i18n";
import { SITE } from "@/lib/site";

// Only the languages listed here are generated; any other /xx/ path is a 404 (nothing is rendered on demand).
export const dynamicParams = false;
export function generateStaticParams() {
  return PUBLISHED_LOCALES.map((lang) => ({ lang }));
}

export const metadata: Metadata = {
  metadataBase: SITE.url,
  title: { default: SITE.name, template: `%s · ${SITE.name}` },
  applicationName: SITE.name,
  formatDetection: { telephone: false, email: false, address: false },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover", // lets the layout use env(safe-area-inset-*) on phones with a notch
  themeColor: "#F4EDE4",
};

export default async function RootLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ lang: string }>;
}) {
  const lang = toLocale((await params).lang);
  return (
    <html lang={LANG_TAG[lang].html} className={`${bodoni.variable} ${literata.variable} ${pinyon.variable}`}>
      <body>
        {children}
        {SITE.analyticsToken && (
          // Cloudflare Web Analytics: no cookies, no personal data, so no cookie banner is needed.
          <script
            defer
            src="https://static.cloudflareinsights.com/beacon.min.js"
            data-cf-beacon={JSON.stringify({ token: SITE.analyticsToken })}
          />
        )}
      </body>
    </html>
  );
}
