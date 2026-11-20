// Makes the favicon set from the vase in the logo (assets/brand/ava-vas.svg), drawn on the sand background:
//   src/app/icon.svg        the modern favicon (sharp at any size)
//   src/app/favicon.ico     for old browsers and tools that only ask for /favicon.ico (32 + 48 px PNGs inside)
//   src/app/apple-icon.png  180 px, for "Add to Home Screen" on iPhone
//   public/icon-192.png, public/icon-512.png   for the web app manifest (Android)
// The results are committed; re-run only when the logo changes: node scripts/icons.mjs

import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";

const ROOT = path.resolve(import.meta.dirname, "..");
const vase = await readFile(path.join(ROOT, "assets/brand/ava-vas.svg"), "utf8");
const inner = vase.replace(/^<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "");

// The vase (64×80) centred on a rounded sand square; strokes slightly thicker so it survives 16 px.
const icon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="22" fill="#F4EDE4"/>
<g transform="translate(23 12) scale(0.84)" fill="none" stroke="#3A2A20" stroke-linecap="round" stroke-linejoin="round" style="stroke-width:3.4">${inner.replace(/stroke-width="[^"]*"/g, "")}</g>
</svg>
`;

const png = (size) => sharp(Buffer.from(icon)).resize(size, size).png({ compressionLevel: 9 }).toBuffer();

/** An .ico file is a tiny directory followed by the images; modern ICOs may simply contain PNGs. */
function ico(images) {
  const header = Buffer.alloc(6 + 16 * images.length);
  header.writeUInt16LE(0, 0); // reserved
  header.writeUInt16LE(1, 2); // type: icon
  header.writeUInt16LE(images.length, 4);
  let offset = header.length;
  images.forEach(({ size, data }, i) => {
    const e = 6 + 16 * i;
    header.writeUInt8(size % 256, e); // width (0 means 256)
    header.writeUInt8(size % 256, e + 1); // height
    header.writeUInt16LE(1, e + 4); // colour planes
    header.writeUInt16LE(32, e + 6); // bits per pixel
    header.writeUInt32LE(data.length, e + 8);
    header.writeUInt32LE(offset, e + 12);
    offset += data.length;
  });
  return Buffer.concat([header, ...images.map((i) => i.data)]);
}

await writeFile(path.join(ROOT, "src/app/icon.svg"), icon);
await writeFile(path.join(ROOT, "src/app/apple-icon.png"), await png(180));
await writeFile(path.join(ROOT, "public/icon-192.png"), await png(192));
await writeFile(path.join(ROOT, "public/icon-512.png"), await png(512));
await writeFile(
  path.join(ROOT, "src/app/favicon.ico"),
  ico([
    { size: 32, data: await png(32) },
    { size: 48, data: await png(48) },
  ]),
);
console.log("icons: written");
