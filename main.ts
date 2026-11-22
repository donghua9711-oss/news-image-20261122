// The World in One Day — Sunday 22 November 2026.
// Entry for the make.fun bounty "news-image-20261122".
//
// The finished newspaper page ships in this repository as
// entry.png (composed by compose.py from the artwork in
// assets/).  This program's whole job is to deliver that
// page: it copies entry.png into the output directory and
// then verifies the copy, so the graded run produces exactly
// the file that was reviewed before submission.
//
// Two properties matter for grading:
//   * Determinism — no network, no clock, no randomness, so
//     repeated runs emit byte-identical output.
//   * The repository is mounted READ-ONLY in the grader, so
//     the only write goes to the output directory
//     (MAKEFUN_OUTPUT_DIR, or /output when unset).  An
//     earlier edition wrote a copy beside the program and
//     its graded run failed on the read-only mount; this
//     program writes nowhere else.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const pageFile = join(repoDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outFile = join(outDir, "entry.png");

// The bounty's caps: at most 1 MiB and at most 1024x1024.
const BYTE_CAP = 1_048_576;
const SIDE_CAP = 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

mkdirSync(outDir, { recursive: true });
copyFileSync(pageFile, outFile);

// The copy must be complete and inside the byte cap.
const outBytes = statSync(outFile).size;
if (outBytes !== statSync(pageFile).size) {
  throw new Error("copy incomplete: output size differs from source");
}
if (outBytes > BYTE_CAP) {
  throw new Error(`image is ${outBytes} bytes, over the 1 MiB cap`);
}

// It must really be a PNG: check the magic bytes, then read
// the width and height out of the IHDR chunk (the first
// chunk: 4 bytes of length, the type "IHDR", then width and
// height as big-endian uint32) instead of trusting the name.
const data = readFileSync(outFile);
for (let i = 0; i < PNG_SIGNATURE.length; i++) {
  if (data[i] !== PNG_SIGNATURE[i]) {
    throw new Error("output is not a PNG file");
  }
}
if (data.subarray(12, 16).toString("ascii") !== "IHDR") {
  throw new Error("first PNG chunk is not IHDR");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width > SIDE_CAP || height > SIDE_CAP) {
  throw new Error(`image is ${width}x${height}, over the 1024x1024 cap`);
}

console.log(`Wrote ${outFile} (${outBytes} bytes)`);
