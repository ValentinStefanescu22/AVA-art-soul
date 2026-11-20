import { Fragment, type CSSProperties } from "react";
import s from "./letters.module.css";

/**
 * A big page title whose letters rise in one after another when the page opens (the one orchestrated moment).
 * The letters are hidden from screen readers, so the heading must carry the whole text in `aria-label`.
 * Words never break inside, and without JavaScript or with reduced motion the title is simply there.
 */
export function Letters({ text }: { text: string }) {
  let k = 0;
  return text.split(" ").map((word, i) => (
    <Fragment key={i}>
      {i > 0 && " "}
      <span className={s.w} aria-hidden="true">
        {[...word].map((ch) => (
          <span key={k} className={s.l} style={{ "--k": k++ } as CSSProperties}>
            {ch}
          </span>
        ))}
      </span>
    </Fragment>
  ));
}
