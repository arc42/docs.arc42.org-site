#!/bin/sh
set -eu

# Commands that manage or bypass the bundle themselves are exempt from the
# staleness check below -- otherwise fixing an out-of-date Gemfile.lock
# (via `make install` / `make update`) would be blocked by the very check
# it's meant to satisfy.
case "${1:-}" in
  bash|sh)
    exec "$@"
    ;;
  bundle)
    case "${2:-}" in
      install|update|lock)
        exec "$@"
        ;;
    esac
    ;;
esac

image_stamp_file="/opt/site-deps/.gemfile-lock.sha256"
runtime_lock_file="/site/Gemfile.lock"

if [ ! -f "$runtime_lock_file" ]; then
  echo "Missing $runtime_lock_file inside the container." >&2
  exit 1
fi

image_stamp="$(cat "$image_stamp_file")"
runtime_stamp="$(sha256sum "$runtime_lock_file" | awk '{ print $1 }')"

if [ "$image_stamp" != "$runtime_stamp" ]; then
  echo "The container gems are out of date for Gemfile.lock." >&2
  echo "Run 'make install' to refresh gems, or 'make build' to rebuild the image." >&2
  exit 1
fi

exec "$@"
