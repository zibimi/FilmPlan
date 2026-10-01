#!/usr/bin/env bash
set -euo pipefail

NAS_HOST="192.168.113.196"

timestamp() {
  /bin/date '+%Y-%m-%d %H:%M:%S'
}

is_mounted() {
  /sbin/mount | /usr/bin/grep -Fq " on $1 "
}

mount_share() {
  local mount_point="$1"
  local share_url="$2"

  if is_mounted "$mount_point"; then
    return
  fi

  echo "$(timestamp) Requesting mount: $mount_point"
  /usr/bin/open -gj "$share_url"
}

# Avoid repeated Finder connection errors while the NAS is offline.
if ! /usr/bin/nc -z -G 2 "$NAS_HOST" 445 >/dev/null 2>&1; then
  echo "$(timestamp) NAS is unavailable: $NAS_HOST"
  exit 0
fi

mount_share '/Volumes/分类' "smb://zibimi@${NAS_HOST}/%E5%88%86%E7%B1%BB"
mount_share '/Volumes/导演们' "smb://zibimi@${NAS_HOST}/%E5%AF%BC%E6%BC%94%E4%BB%AC"

echo "$(timestamp) NAS mount check complete."
