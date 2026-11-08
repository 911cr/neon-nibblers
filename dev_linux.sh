#!/usr/bin/env sh
set -eu
exec sh "$(dirname "$0")/run_linux.sh" --simulate-controllers "$@"
