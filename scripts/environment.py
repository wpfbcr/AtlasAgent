#!/usr/bin/env python3
"""Maintain only AtlasAgent's shell configuration block, with safe quoting."""
import os
from pathlib import Path
import re
import shlex
import sys
import tempfile

BEGIN = "# >>> AtlasAgent >>>"
END = "# <<< AtlasAgent <<<"


def update_environment(path, root):
    path = Path(path)
    original = path.read_text() if path.exists() else ""
    if original.count(BEGIN) != original.count(END):
        raise ValueError("Incomplete AtlasAgent configuration block; existing file preserved")
    block = BEGIN + "\nexport ATLAS_ROOT=" + shlex.quote(str(root)) + "\n" + END
    pattern = re.compile(re.escape(BEGIN) + r"\n.*?" + re.escape(END), re.S)
    if pattern.search(original):
        updated = pattern.sub(lambda match: block, original)
    else:
        # Migrate the legacy project-owned two-line snippet; leave manual settings intact.
        legacy = re.compile(r'^# AtlasAgent \(https://github\.com/wpfbcr/AtlasAgent\)\nexport ATLAS_ROOT=.*$', re.M)
        if legacy.search(original):
            updated = legacy.sub(lambda match: block, original)
        else:
            updated = original.rstrip("\n") + "\n\n" + block + "\n"
    if updated == original:
        return
    # Replace the referent so an existing symlinked shell rc keeps its link.
    target = path.resolve() if path.is_symlink() else path
    fd, temp = tempfile.mkstemp(prefix=".atlas-env-", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w") as output:
            output.write(updated)
        os.chmod(temp, target.stat().st_mode & 0o777 if target.exists() else 0o600)
        os.replace(temp, target)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


if __name__ == "__main__":
    try:
        update_environment(sys.argv[1], sys.argv[2])
    except (OSError, UnicodeError, ValueError) as exc:
        print("Cannot update shell configuration: " + str(exc), file=sys.stderr)
        sys.exit(1)
