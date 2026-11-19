// news-image-20261119: copy the pre-rendered front page to the output dir.
//
// The image itself (entry.png, 1024x1024, drawn at build time with PIL
// and real Noto fonts) sits next to this file. This program only moves
// it into place, after checking it is really the PNG we expect:
// correct signature, a sane IHDR size, and inside the competition caps
// (at most 1 MiB, at most 1024x1024). Anything off and it fails loudly
// instead of handing the grader a broken file.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message: string): never {
  throw new Error(`news-image-20261119: ${message}`);
}

function readPngSize(bytes: Buffer): { width: number; height: number } {
  if (bytes.length < 33) {
    fail(`entry.png is only ${bytes.length} bytes, too short to hold an IHDR chunk`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("entry.png does not start with the PNG signature bytes");
  }
  const chunkType = bytes.subarray(12, 16).toString("ascii");
  if (chunkType !== "IHDR") {
    fail(`first PNG chunk is ${chunkType}, expected IHDR`);
  }
  return {
    width: bytes.readUInt32BE(16),
    height: bytes.readUInt32BE(20),
  };
}

function main(): void {
  const source = join(import.meta.dirname, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = join(outDir, "entry.png");

  const bytes = readFileSync(source);
  if (bytes.length > MAX_BYTES) {
    fail(`entry.png is ${bytes.length} bytes, over the ${MAX_BYTES} byte cap`);
  }
  const { width, height } = readPngSize(bytes);
  const bitDepth = bytes[24];
  const colourType = bytes[25];
  if (bitDepth !== 8 || (colourType !== 2 && colourType !== 6)) {
    fail(`unexpected IHDR: bit depth ${bitDepth}, colour type ${colourType}`);
  }
  if (width === 0 || height === 0 || width > MAX_SIDE || height > MAX_SIDE) {
    fail(`entry.png is ${width}x${height}, outside the ${MAX_SIDE}x${MAX_SIDE} cap`);
  }

  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);

  const written = statSync(target).size;
  if (written !== bytes.length) {
    fail(`copied ${written} bytes but the source is ${bytes.length} bytes`);
  }
  console.log(`wrote ${target} (${width}x${height}, ${written} bytes)`);
}

main();
