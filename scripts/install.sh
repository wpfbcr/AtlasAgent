#!/usr/bin/env bash
# Install AtlasAgent skills for common AI coding agents.
# Requires full repo clone — skills/ alone is NOT sufficient (scripts/ needed).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ATLAS_ROOT="${ATLAS_ROOT:-$REPO_ROOT}"
TARGET="${1:-all}"
ATLAS_USER_HOME="${ATLAS_USER_HOME:-$HOME}"
OVERWRITE=false
WRITE_ENV=true
STAGING_DIR=""

if [[ $# -gt 0 ]]; then shift; fi
for arg in "$@"; do
  case "$arg" in
    --overwrite) OVERWRITE=true ;;
    --no-env) WRITE_ENV=false ;;
    *) echo "Unknown option: $arg" >&2; exit 1 ;;
  esac
done

cleanup() {
  if [[ -n "$STAGING_DIR" ]]; then rm -rf -- "$STAGING_DIR"; fi
}
trap cleanup EXIT

same_skill() {
  [[ -d "$2" && ! -L "$2" ]] && diff -qr "$1" "$2" >/dev/null 2>&1
}

preflight() {
  local dest="$1" skill name target
  for skill in "$REPO_ROOT"/skills/*/; do
    name="$(basename "$skill")"
    [[ "$name" == "_shared" ]] && continue
    target="$dest/$name"
    if [[ -e "$target" || -L "$target" ]]; then
      if ! same_skill "$skill" "$target" && ! $OVERWRITE; then
        echo "Conflict: $target differs from AtlasAgent. Existing files were preserved." >&2
        echo "Review the existing skill, then use --overwrite to replace it with a backup." >&2
        return 1
      fi
    fi
  done
}

install_to() {
  local dest="$1" skill name target backup
  mkdir -p "$dest"
  for skill in "$REPO_ROOT"/skills/*/; do
    name="$(basename "$skill")"
    [[ "$name" == "_shared" ]] && continue
    target="$dest/$name"
    if same_skill "$skill" "$target"; then
      echo "  · $name already up to date"
      continue
    fi
    # Copy completely before moving any existing installation.
    STAGING_DIR="$(mktemp -d "$dest/.atlas-stage.XXXXXX")"
    cp -R "${skill%/}" "$STAGING_DIR/$name"
    backup=""
    if [[ -e "$target" || -L "$target" ]]; then
      # Check again in case a destination appeared after preflight.
      if ! $OVERWRITE; then
        echo "Conflict: $target appeared during installation; preserved." >&2
        return 1
      fi
      mkdir -p "$dest/.atlas-backups"
      backup="$(mktemp -d "$dest/.atlas-backups/$name.XXXXXX")/$name"
      mv -- "$target" "$backup"
    fi
    if ! mv -- "$STAGING_DIR/$name" "$target"; then
      if [[ -n "$backup" ]]; then mv -- "$backup" "$target"; fi
      echo "Failed to install $name; previous skill restored if present." >&2
      return 1
    fi
    rmdir "$STAGING_DIR"
    STAGING_DIR=""
    echo "  ✓ $name → $target"
    if [[ -n "$backup" ]]; then echo "  · Backup: $backup"; fi
  done
}

write_env_snippet() {
  python3 "$REPO_ROOT/scripts/environment.py" "$1" "$ATLAS_ROOT"
  echo "  ✓ configured ATLAS_ROOT in $(basename "$1")"
}

echo "AtlasAgent installer"
echo "Repository: $REPO_ROOT"
echo "ATLAS_ROOT: $ATLAS_ROOT"
echo ""

case "$TARGET" in
  all)
    destinations=("$ATLAS_USER_HOME/.cursor/skills" "$ATLAS_USER_HOME/.claude/skills" "$ATLAS_USER_HOME/.codex/skills" "$ATLAS_USER_HOME/.agents/skills")
    if [[ -d "$ATLAS_USER_HOME/.hermes/skills/productivity" ]]; then
      destinations+=("$ATLAS_USER_HOME/.hermes/skills/productivity")
    fi
    ;;
  cursor) destinations=("$ATLAS_USER_HOME/.cursor/skills") ;;
  claude) destinations=("$ATLAS_USER_HOME/.claude/skills") ;;
  codex) destinations=("$ATLAS_USER_HOME/.codex/skills") ;;
  copilot|agents) destinations=("$ATLAS_USER_HOME/.agents/skills") ;;
  hermes) destinations=("$ATLAS_USER_HOME/.hermes/skills/productivity") ;;
  *)
    echo "Usage: $0 [all|cursor|claude|codex|copilot|hermes] [--overwrite]"
    exit 1
    ;;
esac

for dest in "${destinations[@]}"; do preflight "$dest"; done
for dest in "${destinations[@]}"; do install_to "$dest"; done

if ! $WRITE_ENV; then
  echo "  · Shell configuration skipped"
elif [[ -f "$ATLAS_USER_HOME/.zshrc" ]]; then
  write_env_snippet "$ATLAS_USER_HOME/.zshrc"
elif [[ -f "$ATLAS_USER_HOME/.bashrc" ]]; then
  write_env_snippet "$ATLAS_USER_HOME/.bashrc"
fi

echo ""
echo "Verify:"
echo "  export ATLAS_ROOT=\"$ATLAS_ROOT\""
echo "  python3 \"\$ATLAS_ROOT/scripts/weather_client.py\" forecast --city Tokyo --days 3"
echo ""
echo "Optional: pip3 install fpdf2  # PDF export"
