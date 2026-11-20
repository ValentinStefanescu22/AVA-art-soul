// @vitest-environment jsdom
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NewsletterForm } from "@/components/layout/NewsletterForm";
import { LAYOUT_COPY } from "@/content/ro/layout";

const subscribe = vi.fn();
vi.mock("@/lib/newsletter", async (orig) => ({ ...(await orig<object>()), subscribe: (e: string) => subscribe(e) }));

const copy = LAYOUT_COPY.newsletter;
const setup = () => {
  render(<NewsletterForm id="t" copy={copy} privacyHref="/ro/politica-de-confidentialitate" />);
  return {
    user: userEvent.setup(),
    email: screen.getByLabelText(copy.email),
    consent: screen.getByRole("checkbox"),
    submit: () => screen.getByRole("button"),
  };
};

beforeEach(() => subscribe.mockReset());

describe("<NewsletterForm> (launch checklist 11, 12, 13)", () => {
  it("explains a wrong email under the field and moves focus there", async () => {
    const { user, email, submit } = setup();
    await user.type(email, "ana@");
    await user.click(submit());
    expect(screen.getByText(copy.errorEmail)).toBeInTheDocument();
    expect(email).toHaveAttribute("aria-invalid", "true");
    expect(email).toHaveAccessibleDescription(copy.errorEmail);
    expect(email).toHaveFocus();
    expect(subscribe).not.toHaveBeenCalled();
  });

  it("asks for the consent before subscribing", async () => {
    const { user, email, consent, submit } = setup();
    await user.type(email, "ana@exemplu.ro");
    await user.click(submit());
    expect(screen.getByText(copy.errorConsent)).toBeInTheDocument();
    expect(consent).toHaveFocus();
  });

  it("disables the button and says „Se trimite…” while sending, then thanks you", async () => {
    let finish!: (v: unknown) => void;
    subscribe.mockReturnValue(new Promise((r) => (finish = r)));
    const { user, email, consent, submit } = setup();
    await user.type(email, "ana@exemplu.ro");
    await user.click(consent);
    await user.click(submit());
    expect(submit()).toBeDisabled();
    expect(submit()).toHaveTextContent(copy.sending);
    finish({ ok: true });
    expect(await screen.findByRole("status")).toHaveTextContent(copy.done);
  });

  it("keeps what you typed and lets you try again after a network error", async () => {
    subscribe.mockResolvedValue({ ok: false, reason: "network" });
    const { user, email, consent, submit } = setup();
    await user.type(email, "ana@exemplu.ro");
    await user.click(consent);
    await user.click(submit());
    expect(await screen.findByRole("alert")).toHaveTextContent(copy.errorNetwork);
    expect(email).toHaveValue("ana@exemplu.ro");
    expect(submit()).toBeEnabled();
  });
});
