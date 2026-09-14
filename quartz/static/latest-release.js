// Point the landing-page download cards at the latest GitHub release.
// Each link carries a data-asset regex matched against the release's asset names;
// the hardcoded href stays as the fallback when the API call fails.
(function () {
  const API = "https://api.github.com/repos/SciQLop/SciQLop/releases/latest";
  let release = null;

  async function fetchRelease() {
    if (release) return release;
    const r = await fetch(API, { headers: { Accept: "application/vnd.github+json" } });
    if (!r.ok) throw new Error(`GitHub API ${r.status}`);
    release = await r.json();
    return release;
  }

  async function update() {
    const grid = document.querySelector(".download-grid");
    if (!grid) return;
    try {
      const rel = await fetchRelease();
      for (const a of grid.querySelectorAll("a[data-asset]")) {
        const re = new RegExp(a.dataset.asset);
        const asset = rel.assets.find((x) => re.test(x.name));
        if (asset) a.href = asset.browser_download_url;
      }
      const v = document.querySelector(".download-version");
      if (v && rel.tag_name) v.textContent = rel.tag_name;
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
