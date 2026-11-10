#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec sh run_linux.sh --arena 0 --palette 4 --simulate-controllers --data-dir duel-data --tuning tuning.keyboard-playtest.json --event-log duel-data/latest-match.json "$@"
