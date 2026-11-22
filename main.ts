// news-image-20261122 entrypoint.
// Copies the pre-rendered front page (entry.png, made by gen_1122.py)
// into the output directory make.fun reads from. No network, no
// randomness, no writes anywhere else: two runs produce identical bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
// Same input file, same output bytes: nothing here depends on time,
// chance, or the network, so a re-run is a byte-for-byte repeat.
copyFileSync(join(repoRoot, "entry.png"), join(outDir, "entry.png"));
