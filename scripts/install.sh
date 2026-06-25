#!/usr/bin/env bash
# Install AtlasAgent skills for common AI coding agents.
# Requires full repo clone — skills/ alone is NOT sufficient (scripts/ needed).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ATLAS_ROOT="${ATLAS_ROOT:-$REPO_ROOT}"
TARGET="${1:-all}"

install_to() {
  local dest="$1"
  mkdir -p "$dest"
  for skill in "$REPO_ROOT"/skills/*/; do
    name="$(basename "$skill")"
    [[ "$name" == "_shared" ]] && continue
    rm -rf "$dest/$name"
    cp -R "$skill" "$dest/$name"
    echo "  ✓ $name → $dest/$name"
  done
}

write_env_snippet() {
  local rc_file="$1"
  local line="export ATLAS_ROOT=\"$ATLAS_ROOT\""
  if [[ -f "$rc_file" ]] && grep -q 'ATLAS_ROOT=' "$rc_file" 2>/dev/null; then
    echo "  · ATLAS_ROOT already in $(basename "$rc_file")"
  else
    echo "" >> "$rc_file"
    echo "# AtlasAgent (https://github.com/wpfbcr/AtlasAgent)" >> "$rc_file"
    echo "$line" >> "$rc_file"
    echo "  ✓ wrote ATLAS_ROOT to $(basename "$rc_file")"
  fi
}

echo "AtlasAgent installer"
echo "Repository: $REPO_ROOT"
echo "ATLAS_ROOT: $ATLAS_ROOT"
echo ""

case "$TARGET" in
  all)
    install_to "${HOME}/.cursor/skills"
    install_to "${HOME}/.claude/skills"
    install_to "${HOME}/.codex/skills"
    install_to "${HOME}/.agents/skills"
    if [[ -d "${HOME}/.hermes/skills/productivity" ]]; then
      install_to "${HOME}/.hermes/skills/productivity"
    fi
    ;;
  cursor) install_to "${HOME}/.cursor/skills" ;;
  claude) install_to "${HOME}/.claude/skills" ;;
  codex) install_to "${HOME}/.codex/skills" ;;
  copilot|agents) install_to "${HOME}/.agents/skills" ;;
  hermes)
    install_to "${HOME}/.hermes/skills/productivity"
    ;;
  *)
    echo "Usage: $0 [all|cursor|claude|codex|copilot|hermes]"
    exit 1
    ;;
esac

if [[ -f "${HOME}/.zshrc" ]]; then
  write_env_snippet "${HOME}/.zshrc"
elif [[ -f "${HOME}/.bashrc" ]]; then
  write_env_snippet "${HOME}/.bashrc"
fi

echo ""
echo "Verify:"
echo "  export ATLAS_ROOT=\"$ATLAS_ROOT\""
echo "  python3 \"\$ATLAS_ROOT/scripts/weather_client.py\" forecast --city Tokyo --days 3"
echo ""
echo "Optional: pip3 install fpdf2  # PDF export"
