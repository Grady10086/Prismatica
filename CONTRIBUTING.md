# Contributing

## Set up

```sh
uv sync --all-extras --locked
uv run pytest -q
```

## Keep changes reviewable

- Choose one scientific question or plotting behavior per contribution.
- Keep the raw input, transformation and uncertainty definition traceable.
- Label synthetic fixtures, actual demo runs and published reference material distinctly.
- Preserve sample/run matching and losing cases. Do not add unsupported significance.
- Give the final canvas size and a reproducible command. Inspect PNG and vector output for clipping, label collisions and grayscale readability.
- New compositions should have a purpose beyond another arrangement of the same panels.
- Retain existing resources and their callers when reorganizing documentation.

## Preview assets

Homepage assets come from `examples/showcase_gallery.py`. Keep showcase data explicitly synthetic, and do not silently change fixtures to make a method look better. Store editable SVG plus PNG for display; generated PDFs and raw outputs remain outside Git unless there is a specific distribution need.

Use your own assets or appropriate source rights. Do not commit proprietary color books, private data, source PDFs, extracted third-party figures, credentials or local-machine paths.

## Check before a pull request

Run relevant tests, the example command and local Markdown-link checks. Include what changed, why that plot fits the question, and any limits in the evidence or rendering.
