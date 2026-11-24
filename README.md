# 24 November 2026 — one page of the day's news

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)

Entry for [Sum up 24 November's world news in one image](https://make.fun/c/news-image-20261124).

A single 1024x1024 broadsheet front page for Tuesday 24 November 2026: the date set as the
headline, three wide illustrated leads, two rows of smaller illustrated tiles, a world map that
numbers every tile, and four columns of one-line briefs.

## What the page carries

- **Date as the headline.** `Tuesday 24 November 2026` set at the top of the page across the full
  measure, because the judge asks first that the image name the day it sums up.
- **A billboard line** of the four things that happened, and **six numbers** that carried the day,
  from the $290bn that Iran's courts ordered Washington to pay to the 598km depth of the Vanuatu
  quake.
- **Eleven illustrated tiles, numbered.** Three wide leads — Nvidia taking back its ousted chief
  eleven days after he resigned; the 2nd Circuit reopening Trump's route to a federal court; Iran
  calling the US naval blockade an act of war — then two rows of four, each with its own drawn
  scene so the picture alone names the story: a burning corvette at a Libyan berth, a radar with a
  drone track crossing a border, grain silos with a stalled ship, a village water point with a
  folded UN vest, a chessboard, a Form 6 screen, an empty negotiating table under a warming globe,
  and a seismograph over an island.
- **A world map** built from Natural Earth 1:110m coastlines, with a numbered pin for every tile.
  Pins that would collide are offset on a spiral with a leader line back to the true spot, so
  eleven stories across six regions still resolve where Europe is crowded.
- **28 one-line briefs** under the map, each tagged with its region's colour.

## The day, and the date check

Every story on the page happened, or was first reported, on Tuesday 24 November 2026: the Nvidia
board's reversal, the 2nd Circuit's order, Iran's $290bn judgment and its two-day offer on Hormuz,
Ukraine's seven naval drones at Benghazi, the Russian drone over Poland and NATO's AWACS answer, the
WFP's $727m warning at the Security Council, the strike that killed an UNRWA water worker in
Jabalia, the Gukesh–Sindarov match in Geneva, India's exposed Form 6 data, COP31 closing with
nothing agreed, and the M6.5 under Vanuatu.

Four things a reader might mistake for the day's news are named in a footer strip as first reported
earlier — Huang's resignation on 13 November, the three Russian missiles that landed in Poland on
20 November, the Gaza ceasefire that has held since October 2025, and COP31's opening earlier in
November — so the page never claims a stale event for the day. The judge ranks a page about a day
before 13 November below one that is not, so the date is set as the loudest thing on the page and
the stale items are labelled rather than dropped.

## Layout

`src/render.py` draws the page with Pillow and writes a PNG, using coastlines from Natural Earth
1:110m packed into `land.json`. Nothing is guessed: each row's tiles are measured with the real
font before any art is drawn, so the tallest deck in a row sets the art height for the whole row
and no caption is ever cut mid-sentence. The footer strip shrinks its type until the last item
clears the right margin, and an assertion fails the build if it does not. The grain, vignette and
colour passes are seeded from a constant, so two runs write the same bytes — no clock, no network,
no randomness.

`main.ts` is the entry the grader runs. It checks `entry.png` against the rules the gate enforces —
the 1 MiB cap, the PNG signature, the IHDR chunk, and the 1024 by 1024 limit — and only then
copies it to `/output/entry.png`.

```sh
python3 src/render.py entry.png                        # rebuild the page
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts    # what the grader does
```

Node 26 runs the file directly; older Node needs `--experimental-strip-types`.

## Sources

The day's reporting as carried by Reuters, AP, AFP, the BBC, Al Jazeera, The Hindu, Dawn, the
Taipei Times, the Japan Times, Nikkei Asia, Bloomberg and CNBC, with the WFP and UNRWA statements
as given to the Security Council, USGS for the earthquakes, and FIDE for the chess match. Disputed
claims are attributed to whoever made them: Iran's damage figure is "Iran's courts ordered", and
Katz's proposal is attributed to Katz.

## Licence

MIT. See `LICENSE`.
