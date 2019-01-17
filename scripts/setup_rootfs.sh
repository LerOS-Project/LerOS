#!/bin/bash
command -v yum >/dev/null 2>&1 || { echo >&2 "yum is required but it's not installed.  Aborting."; exit 1; }
source mkimage-yum.sh -g "core" -p "$1" leros
tar -czf rootfs-relay.tar.gz rootfs-relay
