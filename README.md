# One Picture of Tuesday 17 November 2026

A single 1024×1024 newspaper front page that sums up the world's news of
**Tuesday 17 November 2026**: 43 stories — 3 illustrated heroes, 10 illustrated
cards, a dotted world map with numbered pins, and 30 one-line briefs — drawn
programmatically with Python + Pillow. Every letter is rendered by code; no
AI-generated text appears in the image.

Entry for the make.fun bounty
[news-image-20261117](https://make.fun/c/news-image-20261117).

![Competition](https://make.fun/badge/news-image-20261117.svg)
![Rank](https://make.fun/badge/news-image-20261117/Gobpox/news-image-17nov/rank.svg)
![Reward](https://make.fun/badge/news-image-20261117/Gobpox/news-image-17nov/reward.svg)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (byte-identical copy of the committed entry.png)
```

## Files

- `main.py` — the entrypoint: copies `entry.png` to the output directory.
  Standard library only, no network.
- `entry.png` — the entry image (1024×1024, 195,086 bytes).
- `draw.py` — the generator that drew `entry.png` (requires Pillow and the
  DejaVu fonts). Re-running it reproduces the same image.

## License

MIT — see [LICENSE](LICENSE).
