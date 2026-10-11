#!/usr/bin/env bash
# Regenerate website screenshots with SciQLop's batch mode.
#
#   scripts/shots/run.sh                 every shot
#   scripts/shots/run.sh gallery_01 ...  only these (file names without .py)
#
# Each shot runs in its own fresh SciQLop profile (config + data), so no personal
# catalogs, settings or tours leak into the pictures. The Speasy cache is shared.
# Window shots need QRhi, which the offscreen platform lacks: shots run under Xvfb.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SCIQLOP="${SCIQLOP:-$HERE/../../../SciQLop}"
OUT="$HERE/out"
STATE="$HERE/.state"
mkdir -p "$OUT"

shots=("$@")
if [ ${#shots[@]} -eq 0 ]; then
  shots=($(cd "$HERE" && command ls [a-z]*_*.py | sed 's/\.py$//'))
fi

seed_profile() {
  local profile=$1
  rm -rf "$profile"
  mkdir -p "$profile/config/sciqlop" "$profile/data"
  printf 'completed_tours:\n  getting_started: true\n' > "$profile/config/sciqlop/onboardingsettings.yaml"
  printf 'color_palette: dark\n' > "$profile/config/sciqlop/sciqlopstyle.yaml"
  [ -d "$HOME/.config/speasy" ] && cp -r "$HOME/.config/speasy" "$profile/config/"
}

run_shot() {
  local shot=$1 profile="$STATE/$1"
  seed_profile "$profile"
  local webengine=()
  grep -q '^# needs: webengine' "$HERE/$shot.py" && webengine=(--webengine)
  ( cd "$OUT" && \
    XDG_CONFIG_HOME="$profile/config" XDG_DATA_HOME="$profile/data" \
    QT_QPA_PLATFORM=xcb QT_SCALE_FACTOR=2 SHOTS_OUT="$OUT" \
    timeout 900 xvfb-run -a -s "-screen 0 3200x2000x24" \
      uv run --project "$SCIQLOP" sciqlop -w website-shots "${webengine[@]}" --batch "$HERE/$shot.py" \
      > "$OUT/$shot.log" 2>&1 )
}

failed=0
for shot in "${shots[@]}"; do
  printf '%-40s ' "$shot"
  if run_shot "$shot"; then echo ok; else echo "FAIL ($?), see out/$shot.log"; failed=$((failed + 1)); fi
done
echo "$((${#shots[@]} - failed))/${#shots[@]} shots ok"
[ "$failed" -eq 0 ]
