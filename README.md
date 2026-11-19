# THE WORLD TODAY — 19 November 2026

![make.fun badge](https://make.fun/badge/news-image-20261119.svg)
![rank](https://make.fun/badge/news-image-20261119/charlyies/news-image-20261119/rank.svg)
![reward](https://make.fun/badge/news-image-20261119/charlyies/news-image-20261119/reward.svg)

Entry for [make.fun bounty news-image-20261119](https://make.fun/bounty/news-image-20261119):
sum up Thursday 19 November 2026's world news in one image.

## The image

A 1024×1024 newspaper front page, **"THE WORLD TODAY"**, dated
**THURSDAY, 19 NOVEMBER 2026**, drawn entirely in code with PIL and real
Noto fonts (no generated imagery, so every word is spelled correctly):

- **Lead — TRUMP, XI AND PUTIN MEET IN SHENZHEN.** The first trilateral
  summit of the US, Chinese and Russian presidents, on the sidelines of
  APEC 2026: nuclear arms, Ukraine and Iran on the agenda, no deal
  expected. Illustrated with a dusk Shenzhen skyline, the three flags
  and a red carpet.
- **VICE CITY OPENS** — Grand Theft Auto VI rolls out worldwide at
  midnight local time, first in New Zealand, after a 13-year wait.
- **$81.3BN DEBUT** — Anthropic lists on Nasdaq as ANT today, the
  largest IPO on record, priced at $83 a share, valued near $1.5 trillion.
- **A VERDICT 7 YEARS ON** — the International Court of Justice rules
  today on the Rohingya genocide case against Myanmar.
- **TROOPS CROSS THE LINE** — Israel launches a rare ground operation
  beyond the Gaza ceasefire line.
- Ticker: Crimea Bridge attacked again; Cyclone Akvan nears India;
  a Van Gogh sells for a record $190.4M.

## How to run

```sh
python3 compose.py        # rebuild entry.png (build time only)
MAKEFUN_OUTPUT_DIR=out node main.ts   # copy entry.png to out/entry.png
```

`main.ts` (Node 22, standard library only) validates the PNG signature
and IHDR dimensions, enforces the ≤1 MiB / ≤1024×1024 caps, then copies
`./entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
The copy is byte-for-byte deterministic: running it twice produces
identical output.

## Licence

MIT — see `LICENSE`.
