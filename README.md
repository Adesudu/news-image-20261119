# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Adesudu/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Adesudu/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page that sums up the world news of Thursday
19 November 2026 in a single image — built for make.fun's
"Sum up 19 November's world news in one image" bounty ($250 in USDC).

The lead story is Anthropic's record IPO: priced at $83 a share, raising
$81.3 billion — the biggest public debut in history — with ANT starting
to trade on Nasdaq today at about a $1.5 trillion valuation. Around it:
GTA VI's global launch after a 13-year wait, the Trump–Putin–Xi trilateral
in Shenzhen while Europe's allies meet in Berlin, Hakeem Jeffries set to
become the first African-American Speaker of the US House, Israel's ground
operation in central Gaza, and the Crimea bridge hit again — plus an "Also
today" strip (Cyclone Akvan, Voyager 1's one-light-day milestone, Australia
sanctioning settlers, India–Japan defence talks, Fed minutes).

Every headline is a real event reported on 19 November 2026 (Reuters, AP,
BBC, Bloomberg, TradingView). The illustrations — the rising ANT chart,
the Vice City sunset, the three flags — and the whole page were drawn from
scratch by `render.py` (Pillow) at build time; `main.py` (Python 3.13,
standard library only) copies the finished `entry.png` to `/output/entry.png`,
so the program is deterministic and needs no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image from scratch (needs Pillow, build time only):

```sh
python3 render.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=qq4pkark&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
