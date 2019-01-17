Name:		kmod
Version:	20
Release:	15.7%{?dist}.h3
Summary:	Linux kernel module management utilities

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
Source1:	weak-modules
Source2:	depmod.conf.dist
Exclusiveos:	Linux

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch01:	kmod-20-9.el7-0001-depmod-Don-t-fall-back-to-uname-on-bad-version.patch
Patch02:	kmod-20-9.el7-0002-depmod-Ignore-PowerPC64-ABIv2-.TOC.-symbol.patch
Patch03:	kmod-20-9.el7-0003-libkmod-Handle-long-lines-in-proc-modules.patch
Patch04:	kmod-20-15.el7-0004-libkmod-elf-resolve-CRC-if-module-is-built-with-MODU.patch
Patch05:	kmod-20-15.el7-0005-depmod-backport-external-directories-support.patch
Patch06:	kmod-20-15.el7-0006-depmod-module_is_higher_priority-fix-modname-length-.patch
Patch07:	kmod-20-8.h1-0001-depmod-Don-t-unlinkat-orig-depfile-and-add-fsync.patch

BuildRequires:	chrpath
BuildRequires:	zlib-devel
BuildRequires:	xz-devel
BuildRequires:  libxslt
# Remove it as soon as no need for Patch05 anymore (Makefile.am updated)
BuildRequires:  automake autoconf libtool

Provides:	module-init-tools = 4.0-1
Obsoletes:	module-init-tools < 4.0-1
Provides:	/sbin/modprobe

# Required for the weak-modules script
Requires:	/usr/bin/nm
Requires:	/usr/bin/gzip
Requires:	/usr/bin/xz
Requires:	/usr/bin/cpio
Requires:       dracut
Requires:       diffutils

%description
The kmod package provides various programs needed for automatic
loading and unloading of modules under 2.6, 3.x, and later kernels, as well
as other module management programs. Device drivers and filesystems are two
examples of loaded and unloaded modules.

%package libs
Summary:	Libraries to handle kernel module loading and unloading
License:	LGPLv2+
Group:		System Environment/Libraries

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary:	Header files for kmod development
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The kmod-devel package provides header files used for development of
applications that wish to load or unload Linux kernel modules.

%prep
%setup -q
%patch01 -p1 -b .0001-depmod-Don-t-fall-back-to-uname-on-bad-version
%patch02 -p1 -b .0002-depmod-Ignore-PowerPC64-ABIv2-.TOC.-symbol
%patch03 -p1 -b .0003-libkmod-Handle-long-lines-in-proc-modules
%patch04 -p1 -b .0004-libkmod-elf-resolve-CRC-if-module-is-built-with-MODU
%patch05 -p1 -b .0005-depmod-backport-external-directories-support
%patch06 -p1 -b .0006-depmod-module_is_higher_priority-fix-modname-length-.patch
%patch07 -p1 -b .0001-depmod-Don-t-unlinkat-orig-depfile-and-add-fsync

%build
export V=1
aclocal
autoreconf --install --symlink
%configure \
  --with-zlib \
  --with-xz
make %{?_smp_mflags}
#make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modprobe
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modinfo
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/insmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/rmmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/depmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/lsmod

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d

mkdir -p $RPM_BUILD_ROOT/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules

install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/dist.conf

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/depmod.d
%dir %{_sysconfdir}/modprobe.d
%dir %{_prefix}/lib/modprobe.d
%{_bindir}/kmod
%{_sbindir}/modprobe
%{_sbindir}/modinfo
%{_sbindir}/insmod
%{_sbindir}/rmmod
%{_sbindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/weak-modules
%{_datadir}/bash-completion/completions/kmod
%{_sysconfdir}/depmod.d/dist.conf
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*
%doc NEWS README TODO COPYING

%files libs
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%changelog
* Fri Sep  2 2016 Tony Camuso <tcamuso@redhat.com> - 20-9
- Must be bumped to 20-9 due to changes and version bumps in the
  7.2-z stream.
  Resolves: rhbz#1320204

* Sat Jun 25 2016 Tony Camuso <tcamuso@redhat.com> - 20-7
- Backported some needed fixes.
  Resolves: rhbz#1320204

* Fri Feb 26 2016 David Shea <dshea@redhat.com> - 20-6
- Accept '.' as part of a symbol exported by the kernel
  Resolves: rhbz#1283486
- Check the addon modules of the new kernel for exported symbols
  Resolves: rhbz#1296465

* Wed Jun  3 2015 David Shea <dshea@redhat.com> - 20-5
- Check for changes in non-module files that affect that initramfs
  Resolves: rhbz#1108166
- Use dracut to skip early cpio archives in the initramfs
  Resolves: rhbz#1210449

* Mon Apr 13 2015 David Shea <dshea@redhat.com> - 20-4
- Do not remove the weak-updates directory
  Resolves: rhbz#1124352

* Thu Apr  2 2015 David Shea <dshea@redhat.com> - 20-3
- Require kmod-libs instead of kmod from kmod-devel
  Related: rhbz#1199646

* Thu Apr  2 2015 David Shea <dshea@redhat.com> - 20-2
- Remove the explicit requirement on kmod-libs
  Related: rhbz#1199646

* Wed Mar 11 2015 David Shea <dshea@redhat.com> - 20-1
- Rebase to kmod-20
  Resolves: rhbz#1199646

* Wed Jan 14 2015 David Shea <dshea@redhat.com> - 14-10
- Allow module paths to start with /usr
  Resolves: rhbz#1177266

* Tue Apr  1 2014 David Shea <dshea@redhat.com> - 14-9
- Support initramfs files with early_cpio
  Resolves: rhbz#1070035

* Wed Feb 26 2014 David Shea <dshea@redhat.com> - 14-8
- Support xz-compressed and uncompressed initramfs files
  Resolves: rhbz#1070035

* Tue Feb 25 2014 David Shea <dshea@redhat.com> - 14-7
- Require binutils for weak-modules
  Resolves: rhbz#1069612

* Mon Feb 17 2014 David Shea <dshea@redhat.com> - 14-6
- Added a depmod search order as /etc/depmod.d/dist.conf
  Resolves: rhbz#1065354

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 14-5
- Mass rebuild 2014-01-24

* Mon Jan 06 2014 Václav Pavlín <vpavlin@redhat.com> - 14-4
- Version bump due to build fail
  Resolves: rhbz#1048868

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 14-3
- Mass rebuild 2013-12-27

* Wed Aug 07 2013 Václav Pavlín <vpavlin@redhat.com> - 14-2
- Run tests during build

* Fri Jul 05 2013 Josh Boyer <jwboyer@redhat.com> - 14-1
- Update to version 14

* Fri Apr 19 2013 Václav Pavlín <vpavlin@redhat.com> - 13-2
- Main package should require -libs

* Wed Apr 10 2013 Josh Boyer <jwboyer@redhat.com> - 13-1
- Update to version 13

* Wed Mar 20 2013 Weiping Pan <wpan@redhat.com> - 12-3
- Pull in weak-modules for kABI from Jon Masters <jcm@redhat.com> 

* Mon Mar 18 2013 Josh Boyer <jwboyer@redhat.com>
- Add patch to make rmmod understand built-in modules (rhbz 922187)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 12

* Thu Nov 08 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 11

* Fri Sep 07 2012 Josh Boyer <jwboyer@redaht.com>
- Update to version 10

* Mon Aug 27 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Josh Boyer <jwboyer@redhat.com> - 8-2
- Provide modprobe.conf(5) (rhbz 824552)

* Tue May 08 2012 Josh Boyer <jwboyer@redhat.com> - 8-1
- Update to version 8

* Mon Mar 19 2012 Kay Sievers <kay@redhat.com> - 7-1
- update to version 7
  - fix issue with --show-depends, where built-in
    modules of the running kernel fail to include
    loadable modules of the kernel specified

* Sun Mar 04 2012 Kay Sievers <kay@redhat.com> - 6-1
- update to version 6
- remove all patches, they are included in the release

* Fri Feb 24 2012 Kay Sievers <kay@redhat.com> - 5-8
- try to address brc#771285

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 5-7
- fix infinite loop with softdeps

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 5-6
- add upstream patch to fix "modprobe --ignore-install --show-depends"
  otherwise dracut misses a lot of modules, which are already loaded

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 5-5
- add "lsmod"

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-4
- remove temporarily added fake-provides

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-3
- temporarily add fake-provides to be able to bootstrap
  the new udev which pulls the old udev into the buildroot

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-1
- Update to version 5
- replace the module-init-tools package and provide all tools
  as compatibility symlinks

* Mon Jan 16 2012 Kay Sievers <kay@redhat.com> - 4-1
- Update to version 4
- set --with-rootprefix=
- enable zlib and xz support

* Thu Jan 05 2012 Jon Masters <jcm@jonmasters.org> - 3-1
- Update to latest upstream (adds new depmod replacement utility)
- For the moment, use the "kmod" utility to test the various functions

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-6
- Update kmod-2-with-rootlibdir patch with rebuild automake files

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-5
- Initial build for Fedora following package import

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-4
- There is no generic macro for non-multilib "/lib", hardcode like others

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-3
- Update package incorporating fixes from initial review feedback
- Cleaups to SPEC, rpath, documentation, library and binary locations

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-2
- Update package for posting to wider test audience (initial review submitted)

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-1
- Initial Fedora package for module-init-tools replacement (kmod) library
