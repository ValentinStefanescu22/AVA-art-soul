import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";
import s from "./button.module.css";

export type ButtonVariant = "accent" | "accentOnDark" | "ink" | "cream";

type Common = {
  variant: ButtonVariant;
  children: ReactNode;
  /** Full width on phones (the default for solid buttons, per DESIGN.md). */
  block?: boolean;
  className?: string;
};
type LinkRest = { href: string } & Omit<ComponentProps<"a">, "href" | "className" | "children">;
type ButtonRest = { href?: undefined } & Omit<ComponentProps<"button">, "className" | "children">;

const EXTERNAL = /^(https?:|mailto:|tel:)/;

/** A pill button. With `href` it is a link (internal links use Next's <Link>), otherwise a real <button>. */
export function Button({ variant, block = true, className, children, ...rest }: Common & (LinkRest | ButtonRest)) {
  const cls = [s.btn, s[variant], block && s.block, className].filter(Boolean).join(" ");
  if (rest.href !== undefined) {
    const { href, ...a } = rest as LinkRest;
    return EXTERNAL.test(href) ? (
      <a href={href} className={cls} {...a}>
        {children}
      </a>
    ) : (
      <Link href={href} className={cls} {...a}>
        {children}
      </Link>
    );
  }
  const { type = "button", ...b } = rest as ButtonRest;
  return (
    <button type={type} className={cls} {...b}>
      {children}
    </button>
  );
}
