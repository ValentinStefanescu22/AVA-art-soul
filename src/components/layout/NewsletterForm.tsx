"use client";

import Link from "next/link";
import { useRef, useState, type FormEvent } from "react";
import { Button, type ButtonVariant } from "@/components/ui/Button";
import type { LAYOUT_COPY } from "@/content/ro/layout";
import { subscribe, validateNewsletter, type NewsletterErrors } from "@/lib/newsletter";
import footer from "./footer.module.css";

type Styles = Readonly<Record<string, string>>; // keys used: form, label, row, input, submit, consent, err, done
type Props = {
  id: string;
  copy: (typeof LAYOUT_COPY)["newsletter"];
  privacyHref: string;
  /** Another look for the same form (the pop-up): a CSS module with the same class names. Default: the footer's. */
  styles?: Styles;
  variant?: ButtonVariant;
};
type Status = "idle" | "sending" | "sent" | "failed";

/**
 * Email + consent, with the states the launch checklist asks for: an error under each wrong field (and focus moved to
 * the first one), a disabled „Se trimite…” button while sending, a clear network error that keeps what you typed,
 * and the thank-you line.
 */
export function NewsletterForm({ id, copy, privacyHref, styles: s = footer, variant = "ink" }: Props) {
  const [errors, setErrors] = useState<NewsletterErrors>({});
  const [status, setStatus] = useState<Status>("idle");
  const email = useRef<HTMLInputElement>(null);
  const consent = useRef<HTMLInputElement>(null);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (status === "sending") return;
    const value = { email: email.current?.value ?? "", consent: consent.current?.checked ?? false };
    const found = validateNewsletter(value);
    setErrors(found);
    if (found.email) return email.current?.focus();
    if (found.consent) return consent.current?.focus();
    setStatus("sending");
    const res = await subscribe(value.email);
    setStatus(res.ok ? "sent" : "failed");
    if (res.ok) window.dispatchEvent(new CustomEvent("ava:subscribed")); // the home pop-up stays closed after this
  }

  if (status === "sent") {
    return (
      <p className={s.done} role="status">
        {copy.done}
      </p>
    );
  }

  const describe = (field: string, has?: true) =>
    has ? { "aria-invalid": true, "aria-describedby": `${id}-${field}-err` } : {};
  return (
    <form className={s.form} noValidate onSubmit={onSubmit} aria-busy={status === "sending"}>
      <label className={s.label} htmlFor={`${id}-email`}>
        {copy.email}
      </label>
      <div className={s.row}>
        <input
          ref={email}
          id={`${id}-email`}
          className={s.input}
          type="email"
          name="email"
          autoComplete="email"
          inputMode="email"
          required
          placeholder={copy.placeholder}
          {...describe("email", errors.email)}
        />
        <Button variant={variant} type="submit" disabled={status === "sending"} className={s.submit}>
          {status === "sending" ? copy.sending : copy.submit}
        </Button>
      </div>
      {errors.email && (
        <p className={s.err} id={`${id}-email-err`}>
          {copy.errorEmail}
        </p>
      )}
      <label className={s.consent}>
        <input ref={consent} type="checkbox" name="acord" required {...describe("consent", errors.consent)} />
        <span>
          {copy.consentBefore}
          <Link href={privacyHref}>{copy.consentLink}</Link>
          {copy.consentAfter}
        </span>
      </label>
      {errors.consent && (
        <p className={s.err} id={`${id}-consent-err`}>
          {copy.errorConsent}
        </p>
      )}
      {status === "failed" && (
        <p className={s.err} role="alert">
          {copy.errorNetwork}
        </p>
      )}
    </form>
  );
}
