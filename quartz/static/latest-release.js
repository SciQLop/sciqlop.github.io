// Point the landing-page download cards at the latest SciQLop GitHub release.
// Each link carries a data-asset regex matched against the release's asset names;
// the hardcoded href stays as the fallback when the API call fails.
// The repo also publishes launcher releases (tags like launcher-v0.1.3), so
// "releases/latest" is not usable: take the newest vX.Y.Z release instead.
(function () {
  const API = "https://api.github.com/repos/SciQLop/SciQLop/releases?per_page=20";
  const SCIQLOP_TAG = /^v\d+\.\d+\.\d+$/;
  let release = null;

  async function fetchRelease() {
    if (release) return release;
    const r = await fetch(API, { headers: { Accept: "application/vnd.github+json" } });
    if (!r.ok) throw new Error(`GitHub API ${r.status}`);
    const all = await r.json();
    // a release whose installer build has not published yet has no assets: skip it
    release = all.find((x) => SCIQLOP_TAG.test(x.tag_name) && !x.draft && !x.prerelease && x.assets.length > 0);
    if (!release) throw new Error("no SciQLop release found");
    return release;
  }

  async function update() {
    const grid = document.querySelector(".download-grid");
    if (!grid) return;
    try {
      const rel = await fetchRelease();
      let matched = 0;
      for (const a of grid.querySelectorAll("a[data-asset]")) {
        const re = new RegExp(a.dataset.asset);
        const asset = rel.assets.find((x) => re.test(x.name));
        if (asset) { a.href = asset.browser_download_url; matched++; }
      }
      const v = document.querySelector(".download-version");
      if (v && matched > 0) v.textContent = rel.tag_name;
    } catch (e) {
      console.warn("latest-release: keeping the hardcoded links", e);
    }
  }

  if (!window.__sciqlopLatestRelease) {
    window.__sciqlopLatestRelease = true;
    document.addEventListener("nav", update);
  }
  update();
})();
