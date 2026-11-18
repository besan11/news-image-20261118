// The World in One Frame - 18 November 2026.
// A make.fun news-image entry (Node 22, standard library only).
// The program copies the pre-rendered ./entry.png (produced by
// render.py in this repo) into the grader's output directory.
//
// Usage outside the grader's container:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Inside the grader, MAKEFUN_OUTPUT_DIR is unset and the image
// lands in /output/entry.png.

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}

// The grader's output directory may not exist yet; create it
// (including parents) instead of failing on a missing folder.
mkdirSync(outDir, { recursive: true });

const target = join(outDir, 'entry.png');
copyFileSync(source, target);
console.log(`copied entry.png -> ${target}`);
