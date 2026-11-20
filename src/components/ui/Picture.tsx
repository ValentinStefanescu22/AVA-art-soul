import type { CSSProperties } from "react";
import { IMAGES, type ImageKey } from "@/generated/images";

type Props = {
  image: ImageKey;
  /** Required. Describe what the photo shows; pass "" only for purely decorative images. */
  alt: string;
  /** How wide the image is drawn, so the browser picks the right file, e.g. "(max-width: 820px) 100vw, 50vw". */
  sizes: string;
  /** true for the one image that is the first big thing on screen (LCP): loads immediately, at high priority. */
  priority?: boolean;
  className?: string;
  style?: CSSProperties;
};

const srcSet = (list: readonly { w: number; src: string }[]) => list.map(({ w, src }) => `${src} ${w}w`).join(", ");

/**
 * A responsive photo: AVIF for browsers that support it, WebP otherwise, each at several widths,
 * with width/height set (no layout shift) and a blurred preview painted until the file arrives.
 */
export function Picture({ image, alt, sizes, priority = false, className, style }: Props) {
  const img = IMAGES[image];
  const fallback = img.webp.at(-1)!;
  return (
    <picture>
      <source type="image/avif" srcSet={srcSet(img.avif)} sizes={sizes} />
      <source type="image/webp" srcSet={srcSet(img.webp)} sizes={sizes} />
      <img
        src={fallback.src}
        alt={alt}
        width={img.width}
        height={img.height}
        loading={priority ? "eager" : "lazy"}
        fetchPriority={priority ? "high" : "auto"}
        decoding={priority ? "sync" : "async"}
        className={className}
        style={{ backgroundImage: `url(${img.blur})`, backgroundSize: "cover", backgroundPosition: "center", ...style }}
      />
    </picture>
  );
}
