#!/usr/bin/env bash
# Copy SciQLop's animated gesture guides into the tutorial folders that embed them.
# SciQLop is the source of truth: never edit the copies here, change them in SciQLop and rerun.
# Only content/ needs them: public/ is build output, the Quartz build copies them there.
# Usage: scripts/sync-guides.sh ~/Documents/prog/SciQLop
set -euo pipefail

SRC="${1:?usage: $0 <SciQLop checkout>}/SciQLop/components/guides/resources"
DEST="$(cd "$(dirname "$0")/.." && pwd)/content/tutorials"

declare -A FOLDER=(
  [new-panel-and-time-range]="basic plotting"
  [plot-a-product]="basic plotting"
  [drop-on-a-panel]="basic plotting"
  [plot-keys-and-wheel]="basic plotting"
  [command-palette]="basic plotting"
  [catalog-tree-sections]="catalogs"
  [show-a-catalog]="catalogs"
  [create-an-event]="catalogs"
  [edit-an-event]="catalogs"
  [jump-to-an-event]="catalogs"
  [color-events-by-attribute]="catalogs"
  [share-a-catalog-project]="catalogs"
  [write-a-virtual-product]="virtual products"
  [tune-a-virtual-product]="virtual products"
)

for name in "${!FOLDER[@]}"; do
  [[ -f "$SRC/$name.svg" ]] || { echo "missing in SciQLop: $name.svg" >&2; exit 1; }
  cp "$SRC/$name.svg" "$DEST/${FOLDER[$name]}/"
done

for svg in "$SRC"/*.svg; do
  name="$(basename "$svg" .svg)"
  [[ -v "FOLDER[$name]" ]] || echo "not on the website yet, add it to FOLDER and a page: $name" >&2
done
echo "synced ${#FOLDER[@]} guides into $DEST"
