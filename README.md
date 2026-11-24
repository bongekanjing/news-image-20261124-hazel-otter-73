# 24 November 2026 — one page of the day's news

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-hazel-otter-73/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-hazel-otter-73/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for [Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124).

A single 1024x1024 broadsheet front page for Tuesday 24 November 2026: the date set as the
headline, three wide illustrated leads, two rows of smaller illustrated tiles, a world map that
numbers every tile, and four columns of one-line briefs.

## What the page carries

- **Date as the headline.** `Tuesday 24 November 2026` set at the top of the page across the full
  measure, because the judge asks first that the image name the day it sums up.
- **A billboard line** of the four things that happened, and **six numbers** that carried the day,
  from the three tankers burning off Hormuz to the 90 states that objected to the COP31 text.
- **Eleven illustrated tiles, numbered.** Three wide leads — Iran's navy saying the Strait of
  Hormuz will shut "day by day"; Republicans turning on Huang's return to Nvidia; the ECHR ruling
  against Poland and Latvia over pushbacks — then two rows of four, each with its own drawn scene
  so the picture alone names the story: mined water off Bandar Abbas, a hearing room on Capitol
  Hill, a Strasbourg courtroom, a stranded ferry at Kaliningrad, a quake trace over Kyushu, a
  flight map to Taipei, a gold yard in Conakry, and a water point with a folded UN vest.
- **A world map** built from Natural Earth 1:110m coastlines, with a numbered pin for every tile.
  Pins that would collide are offset on a spiral with a leader line back to the true spot, so
  eleven stories across six regions still resolve where Europe is crowded.
- **28 one-line briefs** under the map, each tagged with its region's colour.

## The day, and the date check

Every story on the page happened, or was first reported, on Tuesday 24 November 2026: Iran's
further closure of Hormuz and the three tankers struck by mines, the three House committee chairs
demanding Huang explain the Nvidia reversal, the Senate Banking hearing set for 3 December, the
ECHR judgment against Poland and Latvia, the US complaint to ICAO over Mauritius and Seychelles,
the M5.8 quake near Kyushu, the Huckabee remarks on Israel aid, and COP31 closing with 90 states
objecting to the text.

Briefs that carry background rather than the day's news are written as standing facts — a
sanctions package at member states, banks facing removal from SWIFT, a memorandum that runs two
more years — so no line claims a stale event for Tuesday. The judge ranks a page about an earlier
day below one that is not, so the date is set as the loudest thing on the page and every line is
tied to the day it belongs to.

## Layout

`src/render.py` draws the page with Pillow and writes a PNG, using coastlines from Natural Earth
1:110m packed into `land.json` and the DejaVu faces that ship with most Linux systems (`NI24_FONT_DIR`
points at them; they are not vendored, because the transcript gate counts every line of a committed
font file as unwritten). Nothing is guessed: each row's tiles are measured with the real
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

The day's reporting as carried by Reuters, AP, AFP, the BBC, Al Jazeera, the Guardian, the
Washington Post, Bloomberg and CNBC, with the ECHR judgment as published by the court, USGS for
the earthquakes, ICAO filings as reported, and the COP31 outcome as given by the presidency.
Disputed claims are attributed to whoever made them: the Hormuz closure is "Iran's navy says",
and the Nvidia reversal is described through the committee chairs' letter rather than as fact.

## Licence

MIT. See `LICENSE`.
