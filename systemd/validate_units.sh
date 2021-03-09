#!/usr/bin/env sh
find . -maxdepth 2 -type f \( -name "*.service" -or -name "*.timer" \) -exec sh -c '
  echo "{}";
  systemd-analyze verify "{}";
  ' \;
