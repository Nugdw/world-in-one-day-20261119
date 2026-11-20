// news-image-20261119 entry program (Node 22, standard library only).
//
// The entry is one image: a newspaper front page, "The World in One Day",
// summing up the world news of Thursday 19 November 2026. The page itself
// is drawn by make-image.py (kept in this repository) and ships as
// entry.png; this program's only job is to hand that exact file to the
// grader by copying it from the repository root into the output
// directory, where the gate reads it as /output/entry.png.
//
// Local run (the same shape the grader uses):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// On success it prints nothing and out/entry.png matches entry.png byte
// for byte. On any failure it explains what went wrong on stderr and
// exits 1.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const sourcePath = join(botDir, 'entry.png');
const targetPath = join(outputDir, 'entry.png');

if (!existsSync(sourcePath)) {
  fail(`entry.png not found in bot directory "${botDir}"`);
}

try {
  mkdirSync(outputDir, { recursive: true });
} catch (err) {
  fail(`could not create output directory "${outputDir}": ${(err as Error).message}`);
}

try {
  copyFileSync(sourcePath, targetPath);
} catch (err) {
  fail(`could not copy entry.png to "${targetPath}": ${(err as Error).message}`);
}

// The gate tells PNG from JPEG by the first bytes, so refuse to hand it
// a source that is not a PNG at all: its first eight bytes are fixed.
const sourceBytes = readFileSync(sourcePath);
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (sourceBytes.length < PNG_MAGIC.length || !PNG_MAGIC.every((b, i) => sourceBytes[i] === b)) {
  fail(`entry.png in "${botDir}" does not start with the PNG magic bytes`);
}

// Read the copy back and compare: a copy that silently truncated or
// wrote different bytes would hand the gate a broken page, so treat any
// mismatch as a hard failure instead of a quiet success.
const copiedBytes = readFileSync(targetPath);
if (!sourceBytes.equals(copiedBytes)) {
  fail(`copied entry.png (${copiedBytes.length} bytes) differs from the source (${sourceBytes.length} bytes)`);
}
