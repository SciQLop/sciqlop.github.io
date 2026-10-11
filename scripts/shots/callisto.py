"""The e-CALLISTO HUMAIN type II burst of 2017-09-06 as plain arrays.

e-CALLISTO is not a Speasy provider. The radio plugin wraps the same radiospectra
client; the shots use it directly so they don't depend on a plugin install.
"""
from pathlib import Path

import numpy as np

CACHE = Path.home() / ".cache" / "sciqlop-shots" / "callisto"
START, STOP = "2017-09-06 11:58", "2017-09-06 12:16"
FOCUS_CODE = "59"  # 45-110 MHz receiver
SEARCH_FROM = "2017-09-06 11:45"  # files are 15 min long; this one covers 11:58
F_MAX = 85.0  # MHz; the burst lives below it


def _files() -> list[Path]:
    from sunpy.net import Fido, attrs as a
    import radiospectra.net  # noqa: F401  registers the eCALLISTO client

    result = Fido.search(a.Time(SEARCH_FROM, STOP), a.Instrument("eCALLISTO"))
    table = result[0]
    rows = table[(table["Observatory"] == "HUMAIN") & (table["ID"] == FOCUS_CODE)]
    CACHE.mkdir(parents=True, exist_ok=True)
    return sorted(Path(p) for p in Fido.fetch(rows, path=str(CACHE / "{file}")))


def _read(path: Path):
    from radiospectra.spectrogram import Spectrogram

    spec = Spectrogram(str(path))
    t = spec.times.unix.astype(float)  # seconds since 1970
    f = spec.frequencies.to_value("MHz").astype(float)
    return t, f, np.asarray(spec.data, dtype=float)  # data is (freq, time)


def burst() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(t [s], f [MHz] ascending, z (time, freq)) over START..STOP."""
    parts = [_read(p) for p in _files()]
    f = parts[0][1]
    t = np.concatenate([p[0] for p in parts])
    z = np.concatenate([p[2] for p in parts], axis=1).T
    f_unique, first = np.unique(f, return_index=True)  # sorted; repeated channels dropped
    channels = first[f_unique <= F_MAX]
    keep = (t >= _epoch(START)) & (t <= _epoch(STOP))
    return t[keep], f[channels], z[keep][:, channels]


def _epoch(text: str) -> float:
    return np.datetime64(text.replace(" ", "T"), "s").astype(float)
