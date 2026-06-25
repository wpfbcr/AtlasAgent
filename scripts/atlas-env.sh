#!/usr/bin/env bash
# AtlasAgent path resolver — source from shell or read ATLAS_ROOT from env.
# Usage: source "$(git rev-parse --show-toplevel 2>/dev/null || echo "$HOME/AtlasAgent")/scripts/atlas-env.sh"

if [[ -n "${ATLAS_ROOT:-}" && -d "$ATLAS_ROOT/scripts" ]]; then
  :
elif [[ -d "${HOME}/AtlasAgent/scripts" ]]; then
  ATLAS_ROOT="${HOME}/AtlasAgent"
elif [[ -n "${BASH_SOURCE[0]:-}" ]]; then
  _atlas_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [[ -d "$_atlas_script_dir" && -f "$_atlas_script_dir/weather_client.py" ]]; then
    ATLAS_ROOT="$(cd "$_atlas_script_dir/.." && pwd)"
  fi
  unset _atlas_script_dir
fi

export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
export ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
export ATLAS_REF="$ATLAS_ROOT/skills/atlas-agent/references"
export ATLAS_EXAMPLES="$ATLAS_ROOT/examples"
