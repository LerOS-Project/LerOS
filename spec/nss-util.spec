%global nspr_version 4.19.0
# adjust to the very latest build needed
%global nspr_build_version -1

Summary:          Network Security Services Utilities Library
Name:             nss-util
Version:          3.36.0
Release:          1%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}%{nspr_build_version}
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}%{nspr_build_version}
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl

Source0:          %{name}-%{version}.tar.gz
# The nss-util tar ball is a subset of nss-{version}.tar.gz.
# We use the nss-split-util.sh script for keeping only what we need
# nss-util is produced via via nss-split-util.sh {version}
# Detailed Steps:
# rhpkg clone nss-util
# cd nss-util
# Make the source tarball for nss-util out of the nss one:
# sh ./nss-split-util.sh ${version}
# A file named ${name}-${version}.tar.gz should appear
# ready to upload to the lookaside cache.
Source1:          nss-split-util.sh
Source2:          nss-util.pc.in
Source3:          nss-util-config.in

# Local patches
Patch2: hasht-dont-include-prtypes.patch
Patch7: pkcs1sig-include-prtypes.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=951455
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=923089
Patch8: nss-util-3.19.1-tls12-mechanisms.patch
# To revert the change in:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1377940
Patch9: nss-util-sql-default.patch

%description
Utilities for Network Security Services and the Softoken module

# We shouln't need to have a devel subpackage as util will be used in the
# context of nss or nss-softoken. keeping to please rpmlint.
# 
%package devel
Summary:          Development libraries for Network Security Services Utilities
Group:            Development/Libraries
Requires:         nss-util = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig

%description devel
Header and library files for doing development with Network Security Services.


%prep
%setup -q
%patch2 -p0 -b .prtypes
%patch7 -p0 -b .include_prtypes
%patch8 -p1 -b .tls12_mechs
pushd nss
%patch9 -p1 -R -b .sql-default
popd


%build

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSS_USE_SYSTEM_SQLITE=1

export NSS_BUILD_UTIL_ONLY=1

# external tests are not suitable for nss-util and
# won't compile as they depend on ssl
export NSS_DISABLE_GTESTS=1

%ifnarch noarch
%if 0%{__isa_bits} == 64
USE_64=1
export USE_64
%endif
%endif

# make util
%{__make} -C ./nss/coreconf
%{__make} -C ./nss

# Set up our package file
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-util.pc

NSSUTIL_VMAJOR=`cat nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMAJOR" | awk '{print $3}'`
NSSUTIL_VMINOR=`cat nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMINOR" | awk '{print $3}'`
NSSUTIL_VPATCH=`cat nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VPATCH" | awk '{print $3}'`

export NSSUTIL_VMAJOR
export NSSUTIL_VMINOR
export NSSUTIL_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSSUTIL_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSSUTIL_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSSUTIL_VPATCH,g" \
                          > ./dist/pkgconfig/nss-util-config

chmod 755 ./dist/pkgconfig/nss-util-config


%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}

for file in libnssutil3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the include files we want
# The util headers, the rest come from softokn and nss
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the template files we want
for file in dist/private/nss/templates.c
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-util.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-util.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-util-config $RPM_BUILD_ROOT/%{_bindir}/nss-util-config

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libnssutil3.so

%files devel
%defattr(-,root,root)
# package configuration files
%{_libdir}/pkgconfig/nss-util.pc
%{_bindir}/nss-util-config

# co-owned with nss
%dir %{_includedir}/nss3
# these are marked as public export in nss/lib/util/manifest.mk
%{_includedir}/nss3/base64.h
%{_includedir}/nss3/ciferfam.h
%{_includedir}/nss3/eccutil.h
%{_includedir}/nss3/hasht.h
%{_includedir}/nss3/nssb64.h
%{_includedir}/nss3/nssb64t.h
%{_includedir}/nss3/nsslocks.h
%{_includedir}/nss3/nssilock.h
%{_includedir}/nss3/nssilckt.h
%{_includedir}/nss3/nssrwlk.h
%{_includedir}/nss3/nssrwlkt.h
%{_includedir}/nss3/nssutil.h
%{_includedir}/nss3/pkcs11.h
%{_includedir}/nss3/pkcs11f.h
%{_includedir}/nss3/pkcs11n.h
%{_includedir}/nss3/pkcs11p.h
%{_includedir}/nss3/pkcs11t.h
%{_includedir}/nss3/pkcs11u.h
%{_includedir}/nss3/pkcs11uri.h
%{_includedir}/nss3/pkcs1sig.h
%{_includedir}/nss3/portreg.h
%{_includedir}/nss3/secasn1.h
%{_includedir}/nss3/secasn1t.h
%{_includedir}/nss3/seccomon.h
%{_includedir}/nss3/secder.h
%{_includedir}/nss3/secdert.h
%{_includedir}/nss3/secdig.h
%{_includedir}/nss3/secdigt.h
%{_includedir}/nss3/secerr.h
%{_includedir}/nss3/secitem.h
%{_includedir}/nss3/secoid.h
%{_includedir}/nss3/secoidt.h
%{_includedir}/nss3/secport.h
%{_includedir}/nss3/utilmodt.h
%{_includedir}/nss3/utilpars.h
%{_includedir}/nss3/utilparst.h
%{_includedir}/nss3/utilrename.h
%{_includedir}/nss3/templates/templates.c

%changelog
* Mon Mar  5 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-1
- Rebase to NSS 3.36

* Thu Mar  1 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-0.1.beta
- Rebase to NSS 3.36 BETA

* Tue Jan 16 2018 Daiki Ueno <dueno@redhat.com> - 3.34.0-2
- Recognize "ECC" flag in slotFlags

* Thu Nov 23 2017 Daiki Ueno <dueno@redhat.com> - 3.34.0-1
- Rebase to nss-3.34

* Mon Oct 30 2017 Daiki Ueno <dueno@redhat.com> - 3.34.0-0.1.beta1
- Rebase to nss-3.34-beta1

* Fri Oct  6 2017 Daiki Ueno <dueno@redhat.com> - 3.33.0-1
- Rebase to nss-3.33

* Mon May 15 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-3
- Backport patch to allow empty line at the end of policy file

* Thu Apr 20 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-2
- Rebase to nss-3.28.4

* Thu Mar  9 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-3
- Backport necessary constant definitions

* Thu Mar  2 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-2
- Rebase to nss-3.28.3

* Fri Feb 17 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-1.1
- Prevent ABI incompatibility of SECKEYECPublicKey structure

* Fri Feb 10 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-1.0
- Rebase to nss-3.28.1
- Remove upstreamed build-nss-util-only.patch
- Package new header eccutil.h

* Mon Oct 24 2016 Daiki Ueno <dueno@redhat.com> - 3.21.3-1
- Rebase to nss-3.21.3
- Remove patch for CVE-2016-1950, which is included in the release
- Related: Bug 1347908

* Mon Apr 18 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-4
- Manual merge from the rhel-7.2 branch
- Fix one alias for naming compatibility with prior release
- Remove an unused patch

* Mon Feb 22 2016 Kai Engert <kaie@redhat.com> - 3.21.0-3
- Added upstream patch for CVE-2016-1950

* Thu Jan 28 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-1
- Rebase to nss-util from nss 3.21
- Resolves: Bug 1297940 - Rebase RHEL 7.3 to NSS-util 3.21 in preparation for Firefox 45

* Fri Nov 20 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-5
- Merge security fix from the RHEL-7.1 branch
- Resolves: Bug 1269358 - CVE-2015-7182 CVE-2015-7181

* Thu Jul 16 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-4
- Add links to filed upstream bugs to better track patches in spec file

* Thu Jun 18 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-3
- Remove unused patch

* Thu Jun 18 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-2
- Add support for TLS 1.2 SHA384 per PKCS #11 v2.40

* Fri Jun 05 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-1
- Resolves: Bug 1228913: Rebase to nss-3.19.1 for CVE-2015-4000 [RHEL-7.1]

* Mon Mar 30 2015 Elio Maldonado <emaldona@redhat.com> - 3.18.0-1
- Resolves: Bug 1200931 - [RHEL7.1] nss-util 3.18 rebase required for firefox 38 ESR 

* Thu Jan 22 2015 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-2
- Bump the release number to be higher than the one for rhel-7.0
- Resolves: Bug 1158161 - Upgrade to NSS 3.16.2.3 for Firefox 31.3

* Thu Nov 13 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-1
- Resolves: Bug 1158161 - Upgrade to NSS 3.16.2.3 for Firefox 31.3

* Tue Sep 23 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-3
- Resolves: bug 1145434 - CVE-2014-1568

* Tue Aug 05 2014 Peter Robinson <pbrobinson@redhat.com> 3.16.2-2
- Generic 32/64 bit platform detection (fix ppc64le build)
- Resolves: Bug 1126244 - Ensure nss-util is built for 64 bit on ppc64le
- Fix contributed by Peter Robinson <pbrobinson@redhat.com>

* Tue Jul 08 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-1
- Update to nss-3.16.2
- Resolves: Bug 1103251

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.15.4-2
- Mass rebuild 2014-01-24

* Sun Jan 19 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-4
- Update to nss-3.15.4
- Modified the nss-split-util script to use the nss upstream pristine sources
- Resolves: Bug 1054457 - CVE-2013-1740 nss: false start PR_Recv information disclosure security issue [rhel-7.0]

* Thu Jan 09 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-3
- Add the nss-util portion of a fix for a bug in nss and nss-util
- Resolves: Bug 752980 - Support ECDSA via pluggable ECC in the nss package

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.15.3-2
- Mass rebuild 2013-12-27

* Mon Nov 25 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3-1
- Update to NSS_3_15_3_RTM
- Resolves: Bug 1031463 - CVE-2013-5605 CVE-2013-5606 CVE-2013-1741

* Tue Aug 06 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-2
- Remove an obsolete script and adjust sources numbering accordingly.

* Fri Jul 26 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-1
- Update to NSS_3_15_1_RTM

* Tue Jul 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-2
- Produce source tar ball from the unstripped nss source tar ball

* Wed May 29 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-1
- Update to NSS_3_15_RTM

* Fri Apr 19 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta1.2
- Don't include prtypes.h from hasht.t
- Resolves: rhbz#953277 - rawhide build of glibc fails due to fatal error from nss3/hasht.h

* Fri Apr 05 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.beta1-0.1.beta.1
- Update to NSS_3_15_BETA1
- Update spec file, patches, and helper scripts on account of a shallower source tree

* Fri Feb 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.3-1
- Update to NSS_3_14_3_RTM
- Resolves: rhbz#909782 - specfile support for AArch64

* Sat Feb 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-2
- Retagging to prevent nvr update problems with f18

* Fri Feb 01 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-1
- Update to NSS_3_14_2_RTM

* Thu Dec 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-2
- Install templates.c in /usr/includes/nss3/templates
- Fix bogus date warnings

* Mon Dec 17 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-1
- Update to NSS_3_14_1_RTM

* Sat Oct 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-2
- Update the license to MPLv2.0

* Mon Oct 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-1
- Update to NSS_3_14_RTM

* Fri Oct 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-0.1.rc1.1
- Update to NSS_3_14_RC1
- The hasht.h from now on is provided by nss-util-devel

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-3
- Resolves: rhbz#833529 - revert unwanted change to nss-util.pc.in

* Tue Jun 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-2
- Resolves: rhbz#833529 - Remove space from Libs: line in nss-util.pc.in

* Sat Jun 16 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-1
- Update to NSS_3_13_5_RTM

* Sun Apr 08 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-2
- Resolves: Bug 805716 - Library needs partial RELRO support added
- Patch coreconf/Linux.mk as done on RHEL 6.2

* Fri Apr 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-1
- Update to NSS_3_13_4

* Sun Apr 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-0.1.beta.1
- Update to NSS_3_13_4_BETA1
- Improve steps to splitting off util from the nss
- Add executable attribute to the splitting script

* Tue Mar 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-4
- Resolves: Bug 805716 - Library needs partial RELRO support added

* Fri Mar 16 2012 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.3-3
- Update the release tag to be higher than in f16

* Fri Mar 09 2012 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.3-2
- Require nspr 4.9

* Thu Mar 01 2012 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.1-4
- Update to NSS_3_13_3_RTM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-2
- Fix a gnuc def typo

* Thu Nov 03 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-1
- Update to NSS_3_13_1_RTM

* Sat Oct 15 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-1
- Update to NSS_3_13_RTM

* Fri Oct 07 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.1.rc0.1
- Update to NSS_3_13_RC0

* Thu Sep  8 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.12.11-2
- Avoid %%post/un shell invocations and dependencies.

* Tue Aug 09 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.11-1
- Update to NSS_3_12_11_RTM

* Fri May 06 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-1
- Update to NSS_3_12_10_RTM

* Mon Apr 25 2011 Elio Maldonado Batiz <emaldona@redhat.com> - 3.12.10-0.1.beta1
- Update to NSS_3_12_10_BETA1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-1
- Update to 3.12.9

* Mon Dec 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.9-0.1beta2
- Rebuilt according to fedora pre-release package naming guidelines

* Fri Dec 10 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.2-1
- Update to NSS_3_12_9_BETA2

* Wed Dec 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.1-1
- Update to NSS_3_12_9_BETA1

* Wed Sep 29 2010 jkeating - 3.12.8-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-1
- Update to 3.12.8

* Sat Sep 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.4-1
- NSS 3.12.8 RC0

* Sat Sep 04 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-1
- NSS 3.12.8 Beta 3

* Sun Aug 29 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-2
- Define NSS_USE_SYSTEM_SQLITE and remove nolocalsql patch 

* Mon Aug 16 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-1
- Update to 3.12.7

* Fri Mar 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1
- Update to 3.12.6

* Mon Jan 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-2
- Fix in nss-util-config.in

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1
- Update to 3.12.5

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-8
- Retagging for a chained build with nss-softokn and nss

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-5
- Restoring -rpath-link to nss-util-config

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-4
- Installing shared libraries to %%{_libdir}

* Sat Sep 05 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-3
- Remove symbolic links to shared libraries from devel - 521155
- Apply nss-nolocalsql patch subset for nss-util
- No rpath-link in nss-util-config

* Fri Sep 04 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-2
- Retagging for a chained build

* Thu Sep 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-1
- Update to 3.12.4
- Don't require sqlite

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-15
- Bump the release number for a chained build of nss-util, nss-softokn and nss

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-14
- Cleanup nss-util-config.in

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-13
- nss-util-devel doesn't require nss-devel

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-12
- bump to unique nvr

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-11
- Remove spurious executable permissions from nss-util-config
- Shorten some descriptions to keep rpmlint happy

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> 3.12.3.99.3-10
- dont include the headers in nss-util only in the -devel package
- nss-util-devel Requires nss-devel since its only providing a subset of the headers.

* Thu Aug 20 2009 Dennis Gilmore <dennis@ausil.us> 3.12.3.99.3-9
- Provide nss-devel since we obsolete it

* Wed Aug 19 2009 Elio Maldonado <emaldona@redhat.com> 3.12.3.99.3-8.1
- nss-util-devel obsoletes nss-devel < 3.12.3.99.3-8

* Wed Aug 19 2009 Elio Maldonado <emaldona@redhat.com> 3.12.3.99.3-8
- Initial build
