#!/usr/bin/env bash
#

CURDIR=`pwd`

set -e

usage() {
    cat <<EOOPTS
$(basename $0) [OPTIONS] <name>
OPTIONS:
  -p "<packages>"  The list of packages to install in the container.
                   The default is blank.
  -g "<groups>"    The groups of packages to install in the container.
                   The default is "Core".
  -y <yumconf>     The path to the yum config to install packages from. The
                   default is /etc/yum.conf for Centos/RHEL and /etc/dnf/dnf.conf for Fedora
EOOPTS
    exit 1
}

# option defaults
yum_config=/etc/yum.conf
if [ -f /etc/dnf/dnf.conf ] && command -v dnf &> /dev/null; then
	yum_config=/etc/dnf/dnf.conf
	alias yum=dnf
fi
install_groups="Core"
while getopts ":y:p:g:h" opt; do
    case $opt in
        y)
            yum_config=$OPTARG
            ;;
        h)
            usage
            ;;
        p)
            install_packages="$OPTARG"
            ;;
        g)
            install_groups="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
    esac
done
shift $((OPTIND - 1))
name=$1

if [[ -z $name ]]; then
    usage
fi

target=$(mktemp -d --tmpdir $(basename $0).XXXXXX)

set -x

mkdir -m 755 "$target"/dev
mknod -m 600 "$target"/dev/console c 5 1
mknod -m 600 "$target"/dev/initctl p
mknod -m 666 "$target"/dev/full c 1 7
mknod -m 666 "$target"/dev/null c 1 3
mknod -m 666 "$target"/dev/ptmx c 5 2
mknod -m 666 "$target"/dev/random c 1 8
mknod -m 666 "$target"/dev/tty c 5 0
mknod -m 666 "$target"/dev/tty0 c 4 0
mknod -m 666 "$target"/dev/urandom c 1 9
mknod -m 666 "$target"/dev/zero c 1 5

mkdir -m 755 -p "$target"/usr/bin
mkdir -m 755 -p "$target"/usr/sbin
mkdir -m 755 -p "$target"/usr/lib
mkdir -m 755 -p "$target"/usr/lib64
cd $target
ln -s usr/bin bin
ln -s usr/sbin sbin
ln -s usr/lib lib
ln -s usr/lib64 lib64

mkdir -m 755 -p "$target"/boot
mkdir -m 755 -p "$target"/home
mkdir -m 755 -p "$target"/media
mkdir -m 755 -p "$target"/mnt
mkdir -m 755 -p "$target"/opt
mkdir -m 755 -p "$target"/proc
mkdir -m 755 -p "$target"/root
mkdir -m 755 -p "$target"/run
mkdir -m 755 -p "$target"/srv
mkdir -m 755 -p "$target"/sys
mkdir -m 755 -p "$target"/tmp

cd ${CURDIR}

if [[ -n "$install_packages" ]];
then
    yum -c "$yum_config" --installroot="$target" --releasever=/ --setopt=tsflags=nodocs \
        --setopt=group_package_types=mandatory -y install $install_packages
fi

yum -c "$yum_config" --installroot="$target" -y clean all

mkdir -p "$target"/etc/sysconfig/
cat > "$target"/etc/sysconfig/network << EOF
NETWORKING=yes
HOSTNAME=localhost.localdomain
EOF

mkdir -p --mode=0755 "$target"/var/cache/yum
rm -rf "$target"/etc/ld.so.cache "$target"/var/cache/ldconfig
mkdir -p --mode=0755 "$target"/var/cache/ldconfig

cd "$target"/bin

version=
for file in "$target"/etc/{redhat,system}-release
do
    if [ -r "$file" ]; then
        version="$(sed 's/^[^0-9\]*\([0-9.]\+\).*$/\1/' "$file")"
        break
    fi
done

if [ -z "$version" ]; then
    echo >&2 "warning: cannot autodetect OS version, using '$name' as tag"
    version=$name
fi

cd ${CURDIR}
rm -rf rpm-rootfs-v2r7
mkdir rootfs-relay
cp -rf $target/* rootfs-relay/
cp -rf ch_passwd.sh rootfs-relay/
chroot rootfs-relay/ /ch_passwd.sh
date > rootfs-relay/osc-build.tag
rm -rf rootfs-relay/ch_passwd.sh

rm -rf "$target"

