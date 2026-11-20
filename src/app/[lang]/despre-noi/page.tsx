import type { Metadata } from "next";
import { Fragment, type CSSProperties } from "react";
import { Letters } from "@/components/ui/Letters";
import { Picture } from "@/components/ui/Picture";
import { DESPRE } from "@/content/ro/despre-noi";
import { toLocale } from "@/lib/i18n";
import { pageMetadata } from "@/lib/seo";
import s from "./page.module.css";

type Props = { params: Promise<{ lang: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return pageMetadata(toLocale((await params).lang), "despreNoi");
}

/**
 * Despre noi, in the order of the approved canvas page „Despre noi: lucru”: the dark opening with Alessia, „Povestea”
 * as an interview, „Formări”, „Comunitatea AVA”. All static (no JavaScript of its own); the scroll reveal is the
 * site-wide one (data-reveal). The footer comes from the layout.
 */
export default async function DespreNoi() {
  const { hero, povestea, formari, comunitate } = DESPRE;
  return (
    <>
      <section className={s.hero} aria-labelledby="dn-h">
        <div className={`${s.wrap} ${s.stage}`}>
          <div className={s.head}>
            <h1 className={s.name} id="dn-h" aria-label={hero.name}>
              <Letters text={hero.name} />
            </h1>
            <span className={`${s.role} ${s.a2}`}>{hero.role}</span>
          </div>
          <figure className={s.fig}>
            <Picture image="alessia-sand" alt={hero.photoAlt} sizes="(max-width: 980px) 420px, 540px" priority />
          </figure>
          <div className={`${s.txt} ${s.a3}`}>
            <p className={s.lede}>{hero.lede}</p>
            <p className={s.body}>{hero.body}</p>
          </div>
        </div>
      </section>

      {/* Starts in the hero's last brown and fades to paper: the header stays cream until the fade's middle. */}
      <section className={s.pov} id="povestea" aria-labelledby="pv-h" data-hx-dark="">
        <div className={s.wrap}>
          <h2 id="pv-h" data-reveal="">
            {povestea.title}
          </h2>
          {povestea.qa.map(({ q, a }) => (
            <div className={s.qa} key={q}>
              <h3 className={s.q} data-reveal="">
                {q.split(" ").map((w, k) => (
                  <Fragment key={k}>
                    {k > 0 && " "}
                    <span style={{ "--k": k } as CSSProperties}>{w}</span>
                  </Fragment>
                ))}
              </h3>
              <div className={s.a} data-reveal="">
                <p>
                  {a.text}
                  {a.mark && <strong>{a.mark}</strong>}
                  {a.after}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className={s.form} aria-labelledby="fm-h">
        <div className={s.wrap}>
          <h2 id="fm-h" data-reveal="">
            {formari.title}
          </h2>
          <ul>
            {formari.items.map((f) => (
              <li key={f.title} data-reveal="">
                <p className={s.t}>{f.title}</p>
                <p className={s.where}>
                  {f.where}
                  <span className={s.yr}>{f.when}</span>
                </p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className={s.com} aria-labelledby="cm-h">
        <div className={s.wrap}>
          <h2 id="cm-h" data-reveal="">
            {comunitate.title}
          </h2>
          <p className={s.intro} data-reveal="">
            {comunitate.intro}
          </p>
          <ul>
            {comunitate.people.map((p) => (
              <li key={p.name} data-reveal="">
                <p className={s.nm}>{p.name}</p>
                <span className={s.pr}>{p.role}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </>
  );
}
