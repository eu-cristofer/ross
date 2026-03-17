#!/usr/bin/env bash
#
# Render all .mermaid files in this directory to .png using the Mermaid CLI.
# Usage: ./render_diagrams.sh
#
# Requires: npx @mermaid-js/mermaid-cli  (or globally installed mmdc)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MMDC="npx -y @mermaid-js/mermaid-cli mmdc"

for mermaid_file in *.mermaid; do
    [ -f "$mermaid_file" ] || continue
    png_file="${mermaid_file%.mermaid}.png"
    echo "Rendering $mermaid_file -> $png_file"
    $MMDC -i "$mermaid_file" -o "$png_file" -b transparent -w 2048
done

echo "All diagrams rendered."
