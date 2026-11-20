// The few line icons the design uses, drawn inline so they take the text colour (currentColor) and need no request.
// All are decorative: the text or aria-label next to them says what they do.

type IconProps = { className?: string };

const line = { fill: "none", stroke: "currentColor", strokeLinecap: "round", strokeLinejoin: "round" } as const;

/** The vase from the logo. */
export function Vase({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 64 80" aria-hidden="true">
      <g {...line}>
        <path d="M22 6H42" strokeWidth={5} />
        <path
          d="M26 7C26 13 27 15 25 18C17 24 12 31 12 43C12 55 19 64 24 72H40C45 64 52 55 52 43C52 31 47 24 39 18C37 15 38 13 38 7"
          strokeWidth={3.6}
        />
        <path d="M14.5 35Q32 40 49.5 35M12.6 48Q32 53 51.4 48" strokeWidth={3.2} />
      </g>
    </svg>
  );
}

export function Arrow({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 16 16" aria-hidden="true">
      <path d="M3 8H13M9 4L13 8L9 12" {...line} strokeWidth={1.5} />
    </svg>
  );
}

/** Points right; rotate it with CSS for down/up. */
export function Chevron({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 16 16" aria-hidden="true">
      <path d="M6 3L11 8L6 13" {...line} strokeWidth={1.5} />
    </svg>
  );
}

export function ChevronBack({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 16 16" aria-hidden="true">
      <path d="M10 3.5 5.5 8l4.5 4.5" {...line} strokeWidth={1.6} />
    </svg>
  );
}

export function Close({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      <path d="M5 5L15 15M15 5L5 15" {...line} strokeWidth={1.6} />
    </svg>
  );
}
