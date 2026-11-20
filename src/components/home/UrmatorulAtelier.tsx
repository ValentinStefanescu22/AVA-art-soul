import Link from "next/link";
import { Arrow } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { Picture } from "@/components/ui/Picture";
import { ATELIERE, type Atelier } from "@/content/ateliere";
import { CONTACT } from "@/content/ro/layout";
import { URMATORUL as c } from "@/content/ro/home/urmatorul-atelier";
import { dateParts, upcoming } from "@/lib/dates";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import { Story, type StoryFrame } from "./Story";
import s from "./urmatorul-atelier.module.css";

/**
 * The description in three story frames, cut where the sentence pauses (after , : ; .) so that the longest frame is
 * as short as possible. Without enough pauses it cuts between words.
 */
export function storyLines(text: string): string[] {
  const words = text.split(" ");
  let cuts = words.flatMap((w, i) => (i < words.length - 1 && /[,:;.]$/.test(w) ? [i + 1] : []));
  if (cuts.length < 2) cuts = words.slice(1).map((_, i) => i + 1);
  let best = [text];
  let worst = Infinity;
  for (const i of cuts)
    for (const j of cuts) {
      if (j <= i) continue;
      const parts = [words.slice(0, i), words.slice(i, j), words.slice(j)].map((p) => p.join(" "));
      const m = Math.max(...parts.map((p) => p.length));
      if (m < worst) [worst, best] = [m, parts];
    }
  return best;
}

/** „6 și 13 decembrie”, „13 decembrie și 10 ianuarie”: the month is written once per run of days in it. */
export function dayList(list: readonly Atelier[]): string {
  const ps = list.map((x) => dateParts(x.date));
  const parts = ps.map((p, i) => (ps[i + 1]?.month === p.month ? p.day : `${p.day} ${p.month}`));
  return parts.length > 1 ? `${parts.slice(0, -1).join(", ")} ${c.and} ${parts.at(-1)}` : (parts[0] ?? "");
}

const Todo = ({ text }: { text: string }) => <span className={s.todo}>{text}</span>;

function LinkIcon() {
  return (
    <svg className={s.li} viewBox="0 0 16 16" aria-hidden="true">
      <path
        d="M6.5 9.5l3-3M7 4.5l1-1a2.5 2.5 0 013.5 3.5l-1 1M9 11.5l-1 1A2.5 2.5 0 014.5 9l1-1"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.5}
        strokeLinecap="round"
      />
    </svg>
  );
}

const cx = (...names: (string | false | undefined)[]) => names.filter(Boolean).join(" ");

/** „15 nov”, as a story shows its date. */
const SHORT_MONTH = new Intl.DateTimeFormat("ro-RO", { month: "short", timeZone: "Europe/Bucharest" });
const shortDate = (ymd: string) =>
  `${dateParts(ymd).day} ${SHORT_MONTH.format(new Date(`${ymd}T12:00:00Z`)).replace(".", "")}`;

/** „Următorul atelier” on Acasă: the nearest upcoming group workshop (from src/content/ateliere.ts) and its story. */
export function UrmatorulAtelier({ lang, className }: { lang: Locale; className?: string }) {
  const next = upcoming(ATELIERE);
  const a = next[0];
  const groupPage = href(lang, "ateliereDeGrup");

  if (!a)
    return (
      <section className={cx(s.ua, className)} id="evenimente" aria-labelledby="u-h">
        <div className={cx(s.wrap, s.l)}>
          <h2 id="u-h" data-reveal="">
            {c.title}
          </h2>
          <p className={s.body} data-reveal="">
            {c.empty.text}
          </p>
          <Link className={s.more} href={groupPage} data-reveal="">
            {c.empty.link} <Arrow className={s.ar} />
          </Link>
        </div>
      </section>
    );

  const d = dateParts(a.date);
  const time = a.time ?? <Todo text={c.todoTime} />;
  const zone = a.zone ?? <Todo text={c.todoZone} />;
  const signUp = a.paymentLink ?? groupPage;
  const later = next.slice(1);
  const lines = storyLines(a.description);
  const photos = c.story.photos;

  const frames: StoryFrame[] = [
    <>
      {a.soldOut && <span className={s.so}>{c.soldOut}</span>}
      <p className={s.k}>
        {d.weekday} · {d.day} {d.month} · {c.at} {time}
      </p>
      <p className={s.t}>{a.title}</p>
      <p className={s.w}>{zone}</p>
    </>,
    ...lines.map((l) => (
      <p key={l} className={s.t}>
        {l}
      </p>
    )),
    <>
      <p className={s.t}>{c.story.end}</p>
      <p className={s.w}>
        {c.lei(a.priceLei)} · {a.soldOut ? c.soldOut : c.seatsCall(a.seats)}
      </p>
      <Link className={s.stk} href={a.soldOut ? groupPage : signUp}>
        <LinkIcon />
        {a.soldOut ? c.story.nextWorkshops : c.signUp}
      </Link>
    </>,
  ].map((content, i) => ({ ...photos[Math.min(i, photos.length - 1)]!, cover: i === 0, content }));

  const who = (
    <div className={s.who} aria-hidden="true">
      <Picture image={c.story.avatarImage} alt="" sizes="34px" />
      {CONTACT.instagram.handle.replace(/^@/, "")} <span>· {shortDate(a.date)}</span>
    </div>
  );

  return (
    <section className={cx(s.ua, className)} id="evenimente" aria-labelledby="u-h">
      <div className={cx(s.wrap, s.grid)}>
        <div className={s.l}>
          <h2 id="u-h" data-reveal="">
            {c.title}
          </h2>
          <div className={s.tr} data-reveal="">
            <p className={s.ttl}>{a.title}</p>
            {a.soldOut && <span className={s.badge}>{c.soldOut}</span>}
          </div>
          <p className={s.date} data-reveal="">
            {d.day} {d.month} {d.year}, {d.weekday}, {c.at} {time} ({c.hours(a.durationHours)})
          </p>
          <dl className={s.dl} data-reveal="">
            <div>
              <dt>{c.facts.where}</dt>
              <dd>{zone}</dd>
            </div>
            <div>
              <dt>{c.facts.price}</dt>
              <dd className={s.num}>{c.lei(a.priceLei)}</dd>
            </div>
            <div>
              <dt>{c.facts.seats}</dt>
              <dd>{a.soldOut ? c.seatsTaken(a.seats) : c.seatsFree(a.seats)}</dd>
            </div>
            <div>
              <dt>{c.facts.facilitator}</dt>
              <dd>{c.facilitator}</dd>
            </div>
          </dl>
          <p className={s.note} data-reveal="">
            {c.note(a.priceLei)}
          </p>
          <div className={s.buy} data-reveal="">
            {a.soldOut ? (
              <Link className={s.wait} href={groupPage}>
                {c.seeNext}
              </Link>
            ) : (
              <>
                <Button variant="accent" href={signUp} className={s.cta}>
                  {c.signUp}
                </Button>
                <span className={s.seats}>{c.seatsCall(a.seats)}</span>
              </>
            )}
            {later.length > 0 && <p className={s.wn}>{c.nextList(dayList(later))}</p>}
          </div>
        </div>
        <Story frames={frames} who={who} labels={{ prev: c.story.prev, next: c.story.next }} />
      </div>
    </section>
  );
}
