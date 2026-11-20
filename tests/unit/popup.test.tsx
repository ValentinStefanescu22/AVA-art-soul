// @vitest-environment jsdom
import { act, fireEvent, render, screen } from "@testing-library/react";
import { PopupNewsletter } from "@/components/home/PopupNewsletter";
import { POPUP_COPY } from "@/content/ro/home/popup";

vi.mock("next/navigation", () => ({ usePathname: () => "/ro" }));

beforeAll(() => {
  HTMLDialogElement.prototype.showModal = function () {
    this.setAttribute("open", "");
  };
  HTMLDialogElement.prototype.close = function () {
    this.removeAttribute("open");
  };
});
beforeEach(() => {
  vi.useFakeTimers();
  localStorage.clear();
});
afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});

const dialog = () => document.querySelector("dialog")!;
const wait = (ms: number) => act(() => void vi.advanceTimersByTime(ms));
const scrollTo = (y: number) => {
  Object.defineProperty(document.documentElement, "scrollHeight", { value: 2000, configurable: true });
  Object.defineProperty(window, "innerHeight", { value: 1000, configurable: true });
  Object.defineProperty(window, "scrollY", { value: y, configurable: true });
  act(() => void fireEvent.scroll(window));
};

describe("<PopupNewsletter>", () => {
  it("opens after 8 seconds", () => {
    render(<PopupNewsletter lang="ro" />);
    wait(7999);
    expect(dialog()).not.toHaveAttribute("open");
    wait(1);
    expect(dialog()).toHaveAttribute("open");
  });

  it("opens at 40% scroll, not before", () => {
    render(<PopupNewsletter lang="ro" />);
    scrollTo(300); // 300 of 1000 scrollable = 30%
    expect(dialog()).not.toHaveAttribute("open");
    scrollTo(400);
    expect(dialog()).toHaveAttribute("open");
  });

  it("opens only once per visitor", () => {
    const first = render(<PopupNewsletter lang="ro" />);
    wait(8000);
    expect(localStorage.getItem("ava.popup.newsletter")).toBeTruthy();
    first.unmount();
    render(<PopupNewsletter lang="ro" />);
    wait(8000);
    expect(dialog()).not.toHaveAttribute("open");
  });

  it("still works when localStorage throws", () => {
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("blocked");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("blocked");
    });
    render(<PopupNewsletter lang="ro" />);
    wait(8000);
    expect(dialog()).toHaveAttribute("open");
  });

  it("stays closed after the footer form subscribed", () => {
    render(<PopupNewsletter lang="ro" />);
    act(() => void window.dispatchEvent(new CustomEvent("ava:subscribed")));
    wait(8000);
    expect(dialog()).not.toHaveAttribute("open");
  });

  it("closes with ✕", () => {
    render(<PopupNewsletter lang="ro" />);
    wait(8000);
    fireEvent.click(screen.getByRole("button", { name: POPUP_COPY.close }));
    expect(dialog()).not.toHaveAttribute("open");
  });
});
