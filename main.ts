// Tuesday 24 November 2026, summed up in one image.
//
// The page itself is drawn by src/render.py while the entry is built; this
// program is the entry the grader runs. It copies that finished page to
// /output/entry.png, which is the whole of the job: the gate takes a whole PNG
// or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly
// the bytes copied here. Node 22, standard library only, no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT_NAME = 'entry.png';
const CAP_BYTES = 1048576;
const CAP_SIDE = 1024;
// The rules name the file entry.png whatever the format, so the name is stated
// once here and every path below is built from it.
const SOURCE_NAME = 'entry.png';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const here = dirname(fileURLToPath(import.meta.url));
const target = join(outDir, OUT_NAME);

// The image is the entry, so check it is still a whole PNG of the size the
// rules ask for before it goes out: the 1 MiB cap, the signature, and the
// width and height in the IHDR chunk that follows it.
const bytes = readFileSync(join(here, SOURCE_NAME));
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length > CAP_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png does not start with the PNG signature');
}
if (bytes.length < 24 || bytes.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk at the head of the file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > CAP_SIDE || height > CAP_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over 1024 by 1024`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), target);
