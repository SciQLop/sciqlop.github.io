# sciqlop.github.io

The source of the SciQLop website, https://sciqlop.github.io.

It is built with [Quartz 4](https://quartz.jzhao.xyz/).
The pages are Markdown files in `content/`.
Every push to the `v4` branch rebuilds and publishes the site.

## Preview locally

```bash
npm ci
npx quartz build --serve
```

Then open http://localhost:8080.

## More

Read [HANDOVER.md](HANDOVER.md) before changing the site.
It lists the page layout, the release routine and the known gaps.
