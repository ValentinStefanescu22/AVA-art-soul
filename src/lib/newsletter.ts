// Newsletter sign-up, in one place, so the footer and the pop-up (E2) share the rules and the sending.
// Sending goes to MailerLite's public form endpoint (no secret key: it's the same URL an embedded MailerLite form
// posts to). Until the MailerLite account exists, NEXT_PUBLIC_NEWSLETTER_URL is empty: `next dev` pretends it
// worked, a production build answers "unavailable" so nobody believes they subscribed.

export type NewsletterInput = { email: string; consent: boolean };
export type NewsletterErrors = Partial<Record<keyof NewsletterInput, true>>;
export type SubscribeResult = { ok: true } | { ok: false; reason: "network" | "unavailable" };

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/** Which fields are wrong (empty object: all good). Messages are chosen by the form, in the page's language. */
export function validateNewsletter({ email, consent }: NewsletterInput): NewsletterErrors {
  const errors: NewsletterErrors = {};
  if (!EMAIL.test(email.trim())) errors.email = true;
  if (!consent) errors.consent = true;
  return errors;
}

export async function subscribe(
  email: string,
  { url = process.env.NEXT_PUBLIC_NEWSLETTER_URL, fetchImpl = fetch, dev = process.env.NODE_ENV !== "production" } = {},
): Promise<SubscribeResult> {
  if (!url) {
    if (!dev) return { ok: false, reason: "unavailable" };
    await new Promise((r) => setTimeout(r, 700));
    return { ok: true };
  }
  const body = new FormData();
  body.set("fields[email]", email.trim());
  body.set("ml-submit", "1");
  body.set("anticsrf", "true");
  try {
    const res = await fetchImpl(url, { method: "POST", body, headers: { Accept: "application/json" } });
    if (!res.ok) return { ok: false, reason: "network" };
    const data = (await res.json().catch(() => ({}))) as { success?: boolean };
    return data.success === false ? { ok: false, reason: "network" } : { ok: true };
  } catch {
    return { ok: false, reason: "network" };
  }
}
