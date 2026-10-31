#!/bin/sh
# Local fail-closed replacement. No filesystem or network operations.
printf "%s\n" "BLOCKED: printing-press-import disabled by owner after security audit." >&2
exit 78
