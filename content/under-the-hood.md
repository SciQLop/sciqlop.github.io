---
title: Under the hood
description: How SciQLop stays fast from the CDF file to the GPU, and how it updates itself without breaking.
---

This page explains what happens between "I want this product on this day" and the pixels on your screen. It also
explains how SciQLop updates itself without breaking a working setup. It is for curious users, plugin authors and
contributors.

Every number here was measured. Each one comes from a commit message, the SciQLop
[changelog](https://github.com/SciQLop/SciQLop/blob/main/CHANGELOG.md) or the
[pycdfpp documentation](https://pycdfpp.readthedocs.io/en/latest/optimizations.html). The machines differ between
sections. Your numbers will differ too. The reasons should not.

<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="uh-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="arrowhead" d="M 0 0 L 10 5 L 0 10 z" style="fill: var(--darkgray)"/></marker></defs></svg>

## The path of one plot

<figure class="uh-diagram">
<svg viewBox="0 0 760 270" role="img" aria-label="The path of one plot, from a pan to the GPU">
<rect class="panel" x="10" y="30" width="170" height="70" rx="8"/>
<text class="tb c" x="95" y="58">You pan or zoom</text>
<text class="ts c" x="95" y="78">many times a second</text>
<path class="arrow" d="M180 65 H201"/>
<rect class="blue" x="205" y="30" width="170" height="70" rx="8"/>
<text class="text-blue c" x="290" y="56">SciQLopPlots</text>
<text class="ts c" x="290" y="74">waits 20 ms, keeps the last</text>
<text class="ts c" x="290" y="89">range, adds a margin</text>
<path class="arrow" d="M375 65 H396"/>
<rect class="blue" x="400" y="30" width="170" height="70" rx="8"/>
<text class="text-blue c" x="485" y="56">Worker thread</text>
<text class="ts c" x="485" y="74">runs the product's</text>
<text class="ts c" x="485" y="89">Python function</text>
<path class="arrow" d="M570 65 H591"/>
<rect class="violet" x="595" y="30" width="155" height="70" rx="8"/>
<text class="text-violet c" x="672" y="56">Speasy cache</text>
<text class="ts c" x="672" y="74">on disk, cut into</text>
<text class="ts c" x="672" y="89">fixed-size pieces</text>
<path class="arrow" d="M672 100 V176"/>
<text class="ts" x="680" y="142">miss</text>
<path class="arrow dash" d="M610 100 L380 178"/>
<text class="ts c" x="445" y="114">hit: no network, no decoding</text>
<rect class="orange" x="595" y="180" width="155" height="70" rx="8"/>
<text class="text-orange c" x="672" y="206">Network</text>
<text class="ts c" x="672" y="224">Speasy proxy, or the</text>
<text class="ts c" x="672" y="239">archive itself</text>
<path class="arrow" d="M595 215 H574"/>
<rect class="orange" x="400" y="180" width="170" height="70" rx="8"/>
<text class="text-orange c" x="485" y="206">pycdfpp</text>
<text class="ts c" x="485" y="224">decodes the CDF files</text>
<text class="ts c" x="485" y="239">into numpy arrays</text>
<path class="arrow" d="M400 215 H379"/>
<rect class="green" x="205" y="180" width="170" height="70" rx="8"/>
<text class="text-green c" x="290" y="206">NeoQCP</text>
<text class="ts c" x="290" y="224">millions of points down</text>
<text class="ts c" x="290" y="239">to a few per pixel</text>
<path class="arrow" d="M205 215 H184"/>
<rect class="green" x="10" y="180" width="170" height="70" rx="8"/>
<text class="text-green c" x="95" y="206">GPU</text>
<text class="ts c" x="95" y="224">draws lines, spectrograms</text>
<text class="ts c" x="95" y="239">and grids</text>
</svg>
<figcaption>Each stage below has its own section. Once Speasy hands the arrays over, neither SciQLop nor the plot copies them.</figcaption>
</figure>

1. You drag a plot. SciQLopPlots waits 20 ms for the movement to settle, then asks for the newest range only.
2. It asks for more than you see: half a view extra on each side. Small pans then need no new data at all.
3. A worker thread runs the product's Python function, so the window never waits for data.
4. For a Speasy product, Speasy first looks in its disk cache. Only the missing pieces go to the network.
5. pycdfpp decodes the downloaded CDF files.
6. The numpy arrays reach the plot without a copy.
7. NeoQCP, the plotting engine under SciQLopPlots, reduces millions of points to a few per pixel, on worker
   threads.
8. The GPU draws the result.

The rest of this page follows that path, then covers updates.

## Reading CDF files: pycdfpp

Most space physics data arrives as CDF files. SciQLop reads them with
[pycdfpp](https://github.com/SciQLop/CDFpp), our C++ CDF library. This is a short tour. The
[full story](https://pycdfpp.readthedocs.io/en/latest/optimizations.html), with every counter and diagram, is in
the pycdfpp docs.

### Opening a file reads only its headers

pycdfpp maps the file into memory. It reads only the headers: variable names, attributes, and where the values are.
Values are read the first time you touch them.

Opening a 178 MB MMS FPI file takes 0.6 ms. NASA's library, used by spacepy, takes 264 ms on the same file. It
hashes the whole file before you can read anything.

### Values reach numpy without a copy

A variable's values are exposed through Python's buffer protocol. `np.asarray(variable)` sees the same memory, with
no copy.

The exceptions are files stored big-endian or column-major. Their values are converted once, when they are loaded.

### Compressed variables use every core

A compressed variable is stored as many blocks. An MMS FPI variable has 640 of them. pycdfpp decompresses all the
blocks at once, on every core, each straight into its own slice of the result. It uses libdeflate, 1.5–1.7×
faster than zlib. It releases Python's GIL meanwhile, so SciQLop keeps drawing.

One fix there is a good example of how small details matter:

1. Big results are allocated with 2 MB "huge" memory pages.
2. Many threads then wrote into the fresh buffer at the same time.
3. They hit the same new page together. The kernel zeroed that page once for each thread.
4. Now one thread touches every page first, before the other threads start.
5. Loading 100 MB went from 82 ms to 27 ms.

### Time conversion at billions of values per second

CDF times (TT2000, CDF_EPOCH) must become `datetime64` before anything can be plotted. TT2000 also has to account
for leap seconds. pycdfpp converts 1.3 to 2.9 billion values per second on one core, exact to the nanosecond. It
picks SSE2, AVX2, AVX-512 or ARM NEON instructions at run time, so one wheel gets the best out of every CPU.

### How it compares

Ryzen 7 5800X, Linux, Python 3.13, files already in the page cache. Lower is better.

| Task                                     | pycdfpp | spacepy | cdflib |
| ---------------------------------------- | ------- | ------- | ------ |
| Open a 178 MB MMS FPI file               | 0.6 ms  | 264 ms  | 9.9 ms |
| THEMIS FGM: field and TT2000 time        | 7.8 ms  | 3.77 s  | 306 ms |
| Read a whole MMS FPI file                | 110 ms  | 960 ms  | 620 ms |
| 23 files, 528 MB                         | 391 ms  | 2.37 s  | 2.81 s |
| Same 23 files, 8 threads                 | 161 ms  | not thread-safe | 2.41 s |

Big compressed files read at about 3.5 GB/s. More numbers, including an Apple M2, are on the
[performance page](https://pycdfpp.readthedocs.io/en/latest/performance.html).

## Getting data: Speasy, its cache and its proxy

[Speasy](https://github.com/SciQLop/speasy) fetches data from AMDA, CDAWeb, CSA, SSC and more. The fastest request is
the one it never sends. So most of its work happens in a cache.

### The cache is cut into pieces

Speasy never caches "your request". It caches fixed-size pieces of time, usually 12 hours.

<figure class="uh-diagram">
<svg viewBox="0 0 760 190" role="img" aria-label="A request split into cached fragments">
<text class="tb" x="10" y="24">Your request</text>
<rect class="blue" x="150" y="10" width="420" height="22" rx="4"/>
<text class="ts c" x="360" y="25">Monday 10:00 → Wednesday 02:00</text>
<text class="tb" x="10" y="74">12 h pieces</text>
<rect class="green" x="90" y="58" width="120" height="26" rx="4"/>
<text class="ts c" x="150" y="75">in cache</text>
<rect class="green" x="214" y="58" width="120" height="26" rx="4"/>
<text class="ts c" x="274" y="75">in cache</text>
<rect class="orange" x="338" y="58" width="120" height="26" rx="4"/>
<text class="ts c" x="398" y="75">missing</text>
<rect class="orange" x="462" y="58" width="120" height="26" rx="4"/>
<text class="ts c" x="522" y="75">missing</text>
<rect class="green" x="586" y="58" width="120" height="26" rx="4"/>
<text class="ts c" x="646" y="75">in cache</text>
<path class="line dash" d="M338 92 V112 H582 V92"/>
<path class="arrow" d="M460 112 V128"/>
<rect class="orange" x="330" y="132" width="260" height="44" rx="6"/>
<text class="t c" x="460" y="151">one network request</text>
<text class="ts c" x="460" y="167">then stored back as two pieces</text>
<text class="ts" x="10" y="151">Pieces are merged and</text>
<text class="ts" x="10" y="167">trimmed to your range.</text>
</svg>
<figcaption>Only the missing pieces are fetched. Neighbouring missing pieces go in one request.</figcaption>
</figure>

1. Speasy widens your range a little and rounds it to piece boundaries.
2. It looks up each piece in the cache.
3. Missing pieces next to each other are fetched in one request.
4. The answer is cut back into pieces and stored.
5. The pieces are merged and trimmed to exactly what you asked for.

So panning a day later reuses everything but the new edge. A plot opened twice costs no network at all.

### A cache built for big arrays

The cache is [sciqlop-cache](https://sciqlop-cache.readthedocs.io/en/latest/), a small C++ library we wrote to
replace diskcache. It keeps an SQLite index, and stores big values as plain files that are memory-mapped when read.
It is 20 GB by default, and forgets the least recently used data first.

Two changes made it fit SciQLop:

- **Arrays stay out of the pickle.** A cached variable is a pickle with big numpy arrays inside. Python copies those
  bytes while holding the GIL, so loading data stalled every other thread. The arrays are now stored beside the
  pickle and copied by C++, with the GIL released. Many threads now read at 9.6 GB/s, against 4.8 GB/s before. Time
  axes are also compressed with blosc2, about 15× smaller.
- **A lower memory peak.** A cached read used to keep every piece alive while building the result, margins included.
  It peaked at 2.5× the result's size. Pieces are now trimmed as they load and freed once copied. The peak is 1.5×.

When two plots, or two SciQLop windows, ask for the same missing piece, only one fetches it. The first claims the
piece in the cache. The others wait for it to land.

### Old entries must die

Cache entries live for years. That is the point. It is also a trap:

1. Speasy before 1.7 wrote entries with a version the new code did not expect.
2. Their refresh path kept the old content and only renewed its date.
3. So those entries never expired. Whatever was wrong in them stayed wrong.
4. Our proxy started failing on them: crashes, and old pieces with the wrong shape merged with new ones.
5. Now a version that does not match means "missing". Each entry also records the Speasy version that wrote it, so
   a known bad generation can be discarded once, on purpose.

Live data has a similar trap. AMDA appends new data to some datasets without changing their version. A piece past the
end of the data was cached as empty, forever. Pieces that reach past a dataset's end now live only one hour.

### The proxy: a cache shared by everyone

By default Speasy asks our [Speasy proxy](https://sciqlop.lpp.polytechnique.fr/cache/) first. It runs Speasy on a
server, with one large cache shared by every user. If someone already fetched that day of MMS data, you get it
from there, not from the archive.

- **Arrays travel compressed.** Each array is byte-shuffled and compressed with zstd (blosc). An MMS FGM answer went
  from 13.4 MB to 8.0 MB. Decoding it on your side went from 28 ms to 4 ms.
- **Inventories come ready-made.** The list of tens of thousands of products comes from the proxy in one piece. It is
  kept for two days, then re-checked. If nothing changed, the proxy answers "not modified" and nothing is sent.
- **Most answers are fast.** On the production proxy, half the requests take under 14 ms. The slow ones are those the
  proxy itself has to fetch from an archive.

## Inside SciQLop

SciQLop glues the pieces together. Most of its own work is about not doing things: not fetching twice, not copying,
not running Python where C++ can answer.

### Fetch a margin, then pan for free

Speasy products, and virtual products declared `cachable=True`, fetch half a view extra on each side. Panning or
zooming inside that range fetches nothing and re-bins nothing.

Other virtual products keep exact fetches. They may return a fixed number of points for any range, so a wider fetch
would mean coarser data.

### One time axis, not two

1. Speasy gives times as `datetime64` nanoseconds. The plot wants seconds as floats.
2. Converting made a second time array, the same size as the first.
3. A 1 kHz product over two days is 68 million points. Two time axes of that size cost real memory.
4. SciQLop now converts the timestamps in place, in the same buffer.
5. That fetch holds 0.55 GB less, and peaks 1.1 GB lower. On an 8 GB laptop, that is the difference between
   working and swapping.

Only Speasy results get this treatment. A virtual product may return an array it keeps using, so SciQLop leaves those
alone.

### Keep Python out of the hot path

Python can run on one thread at a time. Data loading uses Python on worker threads. So any Python code on the window's
thread has to wait for them.

1. Every plot panel used to watch every event of every plot from Python, only to catch right-clicks.
2. So each repaint and each mouse move ran a bit of Python.
3. Each of those waited for the data-loading threads to let go of Python.
4. The panel stuttered exactly when data was loading.
5. Now the plot asks for the menu itself, in C++. Python runs only on an actual right-click.

The same idea applies elsewhere:

- The time-range bar updates at most ten times a second while you drag, not on every frame. It shows the final
  range as soon as you stop.
- The field highlights on a new panel are animated by Qt, not restyled from Python on every frame.
- Closing a panel whose data request is stalled no longer waits for the request to return.

### A splash screen in 140 ms

1. The launcher imported the workspace settings before showing the splash screen.
2. That import pulled in SciQLop's core, Speasy, matplotlib, scipy and IPython.
3. The splash appeared only after about 3 seconds.
4. The launcher now shows the window first, and the workspace package loads its names only when they are used.
5. That import dropped to about 140 ms. The splash paints before any heavy module is loaded.

## Plotting: SciQLopPlots and NeoQCP

[SciQLopPlots](https://github.com/SciQLop/SciQLopPlots) is the plotting library behind every panel. Its engine is
NeoQCP, our fork of QCustomPlot rebuilt around the GPU.

### Drawn on the GPU

NeoQCP draws through Qt's QRhi, which talks to Metal, Direct3D, Vulkan or OpenGL. Lines are turned into triangles
and drawn by the GPU. So are grids, tick marks, scatter markers, spans, contour lines and spectrogram images. Text,
dashed lines and a few rare items are still painted on the CPU and uploaded as images.

Exports to PDF, SVG and PNG skip the GPU, so they stay true vector graphics.

### Your arrays are not copied

When you give a plot numpy arrays, SciQLopPlots wraps their memory as it is. It keeps a reference to the arrays, so
worker threads can read them safely while Python moves on.

A few rules make that possible:

- The arrays must be contiguous. A strided view is refused with a hint to call `np.ascontiguousarray`.
- Time (x) must be `float64`. Values can be any integer or float type.
- `float32` values, and row-major `(n, k)` arrays, which is what Speasy returns, take the fastest path.

### From millions of points to a few per pixel

A screen is about 2000 pixels wide. Drawing 10 million points on it means drawing 5000 points per pixel column. You
would see the same picture with four. So NeoQCP reduces the data in two levels.

<figure class="uh-diagram">
<svg viewBox="0 0 760 170" role="img" aria-label="Two-level reduction of line data">
<rect class="panel" x="10" y="30" width="170" height="80" rx="8"/>
<text class="tb c" x="95" y="56">Your data</text>
<text class="ts c" x="95" y="76">10 million points</text>
<text class="ts c" x="95" y="91">or more</text>
<path class="arrow" d="M180 70 H201"/>
<rect class="blue" x="205" y="30" width="170" height="80" rx="8"/>
<text class="text-blue c" x="290" y="54">Level 1</text>
<text class="ts c" x="290" y="72">100 000 min/max bins</text>
<text class="ts c" x="290" y="87">over the whole data,</text>
<text class="ts c" x="290" y="102">built once, all cores</text>
<path class="arrow" d="M375 70 H396"/>
<rect class="orange" x="400" y="30" width="170" height="80" rx="8"/>
<text class="text-orange c" x="485" y="54">Level 2</text>
<text class="ts c" x="485" y="72">4 bins per pixel,</text>
<text class="ts c" x="485" y="87">for the current view,</text>
<text class="ts c" x="485" y="102">from level 1 or raw rows</text>
<path class="arrow" d="M570 70 H591"/>
<rect class="green" x="595" y="30" width="155" height="80" rx="8"/>
<text class="text-green c" x="672" y="54">To the GPU</text>
<text class="ts c" x="672" y="72">about 2 points</text>
<text class="ts c" x="672" y="87">per pixel, peaks</text>
<text class="ts c" x="672" y="102">and gaps kept</text>
<text class="ts c" x="380" y="145">Below 100 000 points, or when you zoom in far enough, the raw points are drawn as they are.</text>
</svg>
<figcaption>Min/max binning keeps every spike: a peak one sample wide still shows.</figcaption>
</figure>

1. Level 1 is built once per dataset, on worker threads, split over all cores. It keeps the minimum and the maximum
   of each bin, so no spike is lost.
2. Level 2 is rebuilt for each view, from level 1 when it is fine enough, or from the raw rows when you zoom in.
3. A last pass keeps the first, minimum, maximum and last point of each pixel column. About two points per pixel
   reach the GPU.

Bursty data taught us to choose level 2's source carefully:

1. Level 1 bins all have the same width in time.
2. In bursty data, one bin can hide tens of thousands of raw points.
3. A view inside a burst covered only a few level-1 bins. NeoQCP judged it "sparse" and drew every raw point, on the
   window's thread, on every frame.
4. It now counts raw rows, not level-1 bins, before choosing.
5. On a 60-million-point dataset, a frame went from 110–234 ms to 49–54 ms.

### Panning moves pictures, not points

While you pan, the data does not change. Only its position does. So NeoQCP does not redraw a layer on a pan. It
shifts the last picture on the GPU, and only the lines' offsets are updated.

A pan step on 10 million points × 8 columns went from 3.8 ms to 0.8 ms.

One bug hid that fast path for months:

1. Every plot creates a colour scale up front, hidden until a spectrogram needs it.
2. It lives on the same layer as the lines.
3. The fast path refused to shift a layer when anything else was on it, even something hidden.
4. So every line plot fell back to a full redraw on each pan step.
5. Hidden items no longer count. Four stacked plots went from 5.20 ms to 1.62 ms per pan step.

### Spectrograms

Spectrograms are resampled onto a grid between one and four times the screen's pixels, on worker threads.

1. The first version walked every source column for each pixel column it filled.
2. It now walks the pixel columns and looks up the source columns that fall in each one.
3. A pan step went from 248 ms to 3.8 ms.

Details that matter for science:

- On a log colour scale, cells are averaged in log space. A plain average of 1 and 100 is 50, which is much brighter
  than either decade looks.
- Gaps between columns are detected, so cells do not bleed across a data gap.
- Frequency axes that go downward are handled.
- The colour image is uploaded to the GPU again only when it changed.

### New data swaps in without flicker

When new data arrives during a pan, the old data keeps drawing until the new one is ready. The plot gathers new
results for up to 200 ms after the first one, and waits again while you keep panning, up to one second. Then it swaps
everything at once. Results from an older request are dropped.

### Threads

- Each plot has a pool of worker threads, half the CPU's cores, with a fast queue for view changes and a slow one for
  new data.
- Each data source in SciQLopPlots has its own thread. Your Python callback runs there.
- Only the newest request waits in each queue. Older ones are dropped, not computed.
- Plot items can only be changed on the window's thread. A setter called from a notebook cell is forwarded there
  instead of crashing.

## Updating without breaking: A/B environments

> [!note] Next release
> This ships with the next SciQLop release, after v0.13.1.

Each SciQLop workspace is a folder with its own Python environment. SciQLop, its plugins and your packages are
installed there, with [uv](https://docs.astral.sh/uv/).

### The problem

Updating packages inside a running environment goes wrong in several ways:

1. SciQLop is running from those files while they are replaced.
2. On Windows, a loaded file cannot be replaced or deleted. A plugin update or removal simply failed.
3. Elsewhere, JupyterLab once broke when packages were upgraded or removed under it.
4. Before this change, an update of SciQLop itself only wrote the new version number. The slow install ran on the
   next start, behind the splash screen.

### Two environments per workspace

The fix is the trick phones and immutable Linux systems use. Each workspace has two environments, `.venv` and
`.venv-b`. SciQLop runs from one. Updates are built into the other.

<figure class="uh-diagram">
<svg viewBox="0 0 760 270" role="img" aria-label="A/B environment update in three steps">
<rect class="panel" x="10" y="20" width="230" height="230" rx="8"/>
<text class="tb c" x="125" y="46">1 · Running</text>
<rect class="green" x="25" y="62" width="200" height="56" rx="6"/>
<text class="text-green c" x="125" y="85">.venv</text>
<text class="ts c" x="125" y="104">live: SciQLop runs from here</text>
<rect class="panel" x="25" y="132" width="200" height="56" rx="6"/>
<text class="tb c" x="125" y="155">.venv-b</text>
<text class="ts c" x="125" y="174">spare</text>
<text class="ts c" x="125" y="222">.sciqlop_venv says ".venv"</text>
<path class="arrow" d="M240 135 H261"/>
<rect class="panel" x="265" y="20" width="230" height="230" rx="8"/>
<text class="tb c" x="380" y="46">2 · Update staged</text>
<rect class="green" x="280" y="62" width="200" height="56" rx="6"/>
<text class="text-green c" x="380" y="85">.venv</text>
<text class="ts c" x="380" y="104">still live, untouched</text>
<rect class="orange" x="280" y="132" width="200" height="56" rx="6"/>
<text class="text-orange c" x="380" y="155">.venv-b</text>
<text class="ts c" x="380" y="174">uv builds the update here</text>
<text class="ts c" x="380" y="214">built: .sciqlop_venv_next = .venv-b</text>
<text class="ts c" x="380" y="232">failed: nothing changes</text>
<path class="arrow" d="M495 135 H516"/>
<rect class="panel" x="520" y="20" width="230" height="230" rx="8"/>
<text class="tb c" x="635" y="46">3 · Next start</text>
<rect class="panel" x="535" y="62" width="200" height="56" rx="6"/>
<text class="tb c" x="635" y="85">.venv</text>
<text class="ts c" x="635" y="104">spare: the next update goes here</text>
<rect class="green" x="535" y="132" width="200" height="56" rx="6"/>
<text class="text-green c" x="635" y="155">.venv-b</text>
<text class="ts c" x="635" y="174">live</text>
<text class="ts c" x="635" y="222">.sciqlop_venv says ".venv-b"</text>
</svg>
<figcaption>The running environment is never modified. The switch is one small file, written atomically.</figcaption>
</figure>

1. You update SciQLop, or update or remove a plugin, from the welcome page or the Plugin Store.
2. SciQLop builds the whole new environment into the spare slot, with `uv sync`, while you keep working.
3. If that fails, nothing else happens. The live environment and the pinned version stay as they were.
4. If it succeeds, SciQLop writes the spare slot's name into a small file, `.sciqlop_venv_next`.
5. On the next start, before anything is loaded, that name moves into `.sciqlop_venv`. The spare slot is now live.
6. The usual sync then runs on it. It catches anything that changed meanwhile, like a plugin installed in between.

A workspace that is not running switches at once, with no restart. A newly installed plugin still goes into the
live environment and loads right away, as before: there is no old file to replace.

### Almost free on disk

uv keeps one copy of each package in its cache. Environments get hard links to those files (clones on macOS), not
copies. So the second environment costs almost nothing. On btrfs, each slot holds 2.44 MiB of its own.

### Safe by construction

- **Atomic switch.** `.sciqlop_venv` and `.sciqlop_venv_next` are written to a temporary file, then renamed over the
  old one. A crash leaves either the old name or the new one, never half a name.
- **Marked only when built.** The pending mark is cleared before a build and written only after it succeeds. A
  half-built slot is never made live.
- **One update at a time.** A lock file stops two updates from building into the same slot. It expires after 10
  minutes, in case SciQLop died holding it.
- **No migration.** Slot A is the old `.venv`. A workspace with no pointer file simply runs from it.
- **Copies stay small.** Duplicating or archiving a workspace skips `.venv-b` and the slot files.

### When an environment is broken anyway

A slot can still break after it went live. For that, the launcher's error window has a **Reset environment** button,
and `sciqlop --reset-environment` does the same.

1. It renames both environments aside (`.venv.reset-<date>`) instead of deleting them, so a file Windows refuses to
   delete never blocks the reset.
2. It rebuilds the workspace on the newest SciQLop release.
3. Your notebooks, settings and workspace are kept.
4. Leftover folders are deleted on later starts, once nothing holds them.

## Measuring it yourself

SciQLop has a built-in profiler under **Tools › Profiling**. It records a trace you can open in
[Perfetto](https://ui.perfetto.dev/). The trace is served from your machine and never leaves it.

The trace splits a data request into its layers: SciQLopPlots, the product's function, Speasy's cache, the proxy,
HTTP and CDF decoding. Set the `SCIQLOP_TRACE` environment variable to start recording before the window opens.

If a plot feels slow, a trace is the most useful thing to attach to a
[bug report](https://github.com/SciQLop/SciQLop/issues).
