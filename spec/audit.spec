%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: User space tools for 2.6 kernel auditing
Name: audit
Version: 2.7.6
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://people.redhat.com/sgrubb/audit/
Source0: http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# This patch switches collecting nametype for objtype because RHEL is different
Patch1: audit-2.7.1-rhel7-fixup.patch
# DO NOT REMOVE - backlog_wait_time is not in RHEL 7 kernel
Patch2: audit-2.7.5-no-backlog-wait-time.patch
# BZ 1455594 - Bad configuration keyword for audispd-remote.conf
Patch3: audit-2.7.7-queue_error_action.patch
# BZ 1460110 - aureport does not report all anomalies
Patch4: audit-2.7.7-aureport.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openldap-devel
BuildRequires: swig
BuildRequires: python-devel
BuildRequires: tcp_wrappers-devel krb5-devel libcap-ng-devel
BuildRequires: kernel-headers >= 2.6.29
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires: systemd-units
Requires(post): systemd-units systemd-sysv chkconfig coreutils
Requires(preun): systemd-units
Requires(postun): systemd-units coreutils

%description
The audit package contains the user space utilities for
storing and searching the audit records generated by
the audit subsystem in the Linux 2.6 kernel.

%package libs
Summary: Dynamic library for libaudit
License: LGPLv2+
Group: Development/Libraries

%description libs
The audit-libs package contains the dynamic libraries needed for 
applications to use the audit framework.

%package libs-embedded
Summary: Dynamic library for libaudit
License: LGPLv2+
Group: Development/Libraries

%description libs-embedded
The audit-libs package contains the dynamic libraries needed for 
applications to use the audit framework.

%package libs-devel
Summary: Header files for libaudit
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kernel-headers >= 2.6.29

%description libs-devel
The audit-libs-devel package contains the header files needed for
developing applications that need to use the audit framework libraries.

%package libs-static
Summary: Static version of libaudit library
License: LGPLv2+
Group: Development/Libraries
Requires: kernel-headers >= 2.6.29

%description libs-static
The audit-libs-static package contains the static libraries
needed for developing applications that need to use static audit
framework libraries

%package libs-python
Summary: Python bindings for libaudit
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description libs-python
The audit-libs-python package contains the bindings so that libaudit
and libauparse can be used by python.

%package -n audispd-plugins
Summary: Plugins for the audit event dispatcher
License: GPLv2+
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: openldap

%description -n audispd-plugins
The audispd-plugins package provides plugins for the real-time
interface to the audit system, audispd. These plugins can do things
like relay events to remote machines or analyze events for suspicious
behavior.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --sbindir=/sbin --libdir=/%{_lib} --with-python=yes --with-libwrap --enable-gssapi-krb5=yes --with-libcap-ng=yes --with-arm --with-aarch64 \
--without-golang --enable-zos-remote --enable-systemd

make CFLAGS="%{optflags}" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,etc/audispd/plugins.d,etc/audit/rules.d}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/audit
mkdir -p --mode=0700 $RPM_BUILD_ROOT/%{_var}/log/audit
mkdir -p $RPM_BUILD_ROOT/%{_var}/spool/audit
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
# This winds up in the wrong place when libtool is involved
mv $RPM_BUILD_ROOT/%{_lib}/libaudit.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libauparse.a $RPM_BUILD_ROOT%{_libdir}
curdir=`pwd`
cd $RPM_BUILD_ROOT/%{_libdir}
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libaudit.so.1.*.*\``
ln -s ../../%{_lib}/$LIBNAME libaudit.so
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libauparse.so.0.*.*\``
ln -s ../../%{_lib}/$LIBNAME libauparse.so
cd $curdir
# Remove these items so they don't get picked up.
rm -f $RPM_BUILD_ROOT/%{_lib}/libaudit.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libauparse.so

find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages -name '*.a' -delete

# Move the pkgconfig file
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

# On platforms with 32 & 64 bit libs, we need to coordinate the timestamp
touch -r ./audit.spec $RPM_BUILD_ROOT/etc/libaudit.conf
touch -r ./audit.spec $RPM_BUILD_ROOT/usr/share/man/man5/libaudit.conf.5.gz

%check
%ifnarch aarch64 ppc %{power64} s390 s390x %{ix86}
make check
%endif
# Get rid of make files that they don't get packaged.
rm -f rules/Makefile*


%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%post
# Copy default rules into place on new installation
files=`ls /etc/audit/rules.d/ 2>/dev/null | wc -w`
if [ "$files" -eq 0 ] ; then
  if [ -e /usr/share/doc/audit-%{version}/rules/10-base-config.rules ] ; then
    cp /usr/share/doc/audit-%{version}/rules/10-base-config.rules /etc/audit/rules.d/audit.rules
  else
    touch /etc/audit/rules.d/audit.rules
  fi
  chmod 0600 /etc/audit/rules.d/audit.rules
fi
%systemd_post auditd.service

%preun
%systemd_preun auditd.service

%postun libs -p /sbin/ldconfig

%postun
if [ $1 -ge 1 ]; then
   /sbin/service auditd condrestart > /dev/null 2>&1 || :
fi

%files libs
%defattr(-,root,root,-)
/%{_lib}/libauparse.*
%config(noreplace) %attr(640,root,root) /etc/libaudit.conf
%{_mandir}/man5/libaudit.conf.5.gz

%files libs-embedded
%defattr(-,root,root,-)
/%{_lib}/libaudit.so.1*

%files libs-devel
%defattr(-,root,root,-)
%doc contrib/skeleton.c contrib/plugin
%{_libdir}/libaudit.so
%{_libdir}/libauparse.so
%{_includedir}/libaudit.h
%{_includedir}/auparse.h
%{_includedir}/auparse-defs.h
%{_datadir}/aclocal/audit.m4
%{_libdir}/pkgconfig/audit.pc
%{_libdir}/pkgconfig/auparse.pc
%{_mandir}/man3/*

%files libs-static
%defattr(-,root,root,-)
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a

%files libs-python
%defattr(-,root,root,-)
%attr(755,root,root) %{python_sitearch}/_audit.so
%attr(755,root,root) %{python_sitearch}/auparse.so
%{python_sitearch}/audit.py*

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog rules init.d/auditd.cron
%attr(644,root,root) %{_mandir}/man8/audispd.8.gz
%attr(644,root,root) %{_mandir}/man8/auditctl.8.gz
%attr(644,root,root) %{_mandir}/man8/auditd.8.gz
%attr(644,root,root) %{_mandir}/man8/aureport.8.gz
%attr(644,root,root) %{_mandir}/man8/ausearch.8.gz
%attr(644,root,root) %{_mandir}/man8/autrace.8.gz
%attr(644,root,root) %{_mandir}/man8/aulast.8.gz
%attr(644,root,root) %{_mandir}/man8/aulastlog.8.gz
%attr(644,root,root) %{_mandir}/man8/auvirt.8.gz
%attr(644,root,root) %{_mandir}/man8/augenrules.8.gz
%attr(644,root,root) %{_mandir}/man8/ausyscall.8.gz
%attr(644,root,root) %{_mandir}/man7/audit.rules.7.gz
%attr(644,root,root) %{_mandir}/man5/auditd.conf.5.gz
%attr(644,root,root) %{_mandir}/man5/audispd.conf.5.gz
%attr(644,root,root) %{_mandir}/man5/ausearch-expression.5.gz
%attr(755,root,root) /sbin/auditctl
%attr(755,root,root) /sbin/auditd
%attr(755,root,root) /sbin/ausearch
%attr(755,root,root) /sbin/aureport
%attr(750,root,root) /sbin/autrace
%attr(750,root,root) /sbin/audispd
%attr(750,root,root) /sbin/augenrules
%attr(755,root,root) %{_bindir}/aulast
%attr(755,root,root) %{_bindir}/aulastlog
%attr(755,root,root) %{_bindir}/ausyscall
%attr(755,root,root) %{_bindir}/auvirt
%attr(644,root,root) %{_unitdir}/auditd.service
%attr(750,root,root) %dir %{_libexecdir}/initscripts/legacy-actions/auditd
%attr(750,root,root) %{_libexecdir}/initscripts/legacy-actions/auditd/resume
%attr(750,root,root) %{_libexecdir}/initscripts/legacy-actions/auditd/rotate
%attr(750,root,root) %{_libexecdir}/initscripts/legacy-actions/auditd/stop
%attr(750,root,root) %{_libexecdir}/initscripts/legacy-actions/auditd/restart
%attr(750,root,root) %{_libexecdir}/initscripts/legacy-actions/auditd/condrestart
%attr(-,root,-) %dir %{_var}/log/audit
%attr(750,root,root) %dir /etc/audit
%attr(750,root,root) %dir /etc/audit/rules.d
%attr(750,root,root) %dir /etc/audisp
%attr(750,root,root) %dir /etc/audisp/plugins.d
%config(noreplace) %attr(640,root,root) /etc/audit/auditd.conf
%ghost %config(noreplace) %attr(640,root,root) /etc/audit/rules.d/audit.rules
%ghost %config(noreplace) %attr(640,root,root) /etc/audit/audit.rules
%config(noreplace) %attr(640,root,root) /etc/audit/audit-stop.rules
%config(noreplace) %attr(640,root,root) /etc/audisp/audispd.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/af_unix.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/syslog.conf

%files -n audispd-plugins
%defattr(-,root,root,-)
%attr(644,root,root) %{_mandir}/man8/audispd-zos-remote.8.gz
%attr(644,root,root) %{_mandir}/man5/zos-remote.conf.5.gz
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/zos-remote.conf
%attr(750,root,root) /sbin/audispd-zos-remote
%config(noreplace) %attr(640,root,root) /etc/audisp/audisp-remote.conf
%config(noreplace) %attr(640,root,root) /etc/audisp/plugins.d/au-remote.conf
%attr(750,root,root) /sbin/audisp-remote
%attr(700,root,root) %dir %{_var}/spool/audit
%attr(644,root,root) %{_mandir}/man5/audisp-remote.conf.5.gz
%attr(644,root,root) %{_mandir}/man8/audisp-remote.8.gz

%changelog
* Mon Jun 12 2017 Steve Grubb <sgrubb@redhat.com> 2.7.6-3
resolves: #1460110 - aureport does not report all anomalies

* Fri May 26 2017 Steve Grubb <sgrubb@redhat.com> 2.7.6-2
resolves: #1455594 - Bad configuration keyword for audispd-remote.conf

* Wed Apr 19 2017 Steve Grubb <sgrubb@redhat.com> 2.7.6-1
resolves: #1443107 - disk full action and infinite loop in audit-remote

* Mon Apr 10 2017 Steve Grubb <sgrubb@redhat.com> 2.7.5-1
resolves: #1437187 - audit rpm postinstall script points to non-existing file
resolves: #1437426 - Remove "--backlog_wait_time" from auditctl man page & rules
resolves: #1437626 - PF_PACKET socket address will cause ausearch to segfault
resolves: #1438997 - SECCOMP records have wrong syscall

* Tue Mar 28 2017 Steve Grubb <sgrubb@redhat.com> 2.7.4-1
resolves: #1367703 - auvirt wasn't supporting date keywords
resolves: #1396792 - augenrules includes files ending in regexp "rules"
resolves: #1406525 - ausearch with '--raw' parameter outputs garbage character

* Tue Feb 28 2017 Steve Grubb <sgrubb@redhat.com> 2.7.3-1
resolves: #1381601 - audit package update
resolves: #1382381 - typo in package description

* Fri Jan 20 2017 Steve Grubb <sgrubb@redhat.com> 2.6.5-4
resolves: #1382397 - write_logs option is not correctly handled
resolves: #1414812 - Setting log_format to NOLOG make auditd core dump

* Wed Aug 10 2016 Steve Grubb <sgrubb@redhat.com> 2.6.5-3
resolves: #1296204 - Rebase audit package

* Wed Jan 14 2015 Steve Grubb <sgrubb@redhat.com> 2.4.1-5
resolves: #1180675 - rules with "-F arch=ppc64le" fail to load

* Tue Jan 13 2015 Steve Grubb <sgrubb@redhat.com> 2.4.1-4
- Remove golang bindings added under the following bz
resolves: #1115196 - Add golang bindings for libaudit

* Wed Dec 17 2014 Steve Grubb <sgrubb@redhat.com> 2.4.1-2
resolves: #1173160 - Audit package needs update for new VPN crypto events

* Tue Oct 28 2014 Steve Grubb <sgrubb@redhat.com> 2.4.1-1
resolves: #963353 - aarch64 userspace auditing needs to be written
resolves: #1150202 - perf trace sleep 1 does not list any syscall information
resolves: #1142989 - Update audit package to 2.4.1
resolves: #1155221 - adjust fstatat naming to match kernel uapi

* Thu Sep 18 2014 Steve Grubb <sgrubb@redhat.com> 2.4-1
resolves: #1115196 - Add golang bindings for libaudit
resolves: #1105150 - audispd config file parser fails on long input
resolves: #1104973 - auparse truncating selinux context after first category
resolves: #1088593 - auditctl man page examples use deprecated syscalls
resolves: #1087849 - support for setting loginuid immutable
resolves: #1073063 - AUDIT_SECCOMP events syscall field is not interpretted
resolves: #975796  - confusing aulast records for bad logins

* Tue Mar 18 2014 Steve Grubb <sgrubb@redhat.com> 2.3.3-4
resolves: #1077249 - Audit update, various issues

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.3.3-3
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Steve Grubb <sgrubb@redhat.com> 2.3.3-2
- New upstream bugfix/enhancement release
resolves: #1053804 - ausearch issues found by ausearch-test
resolves: #1030409 - ausearch help typo for "-x" option

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.2-4
- Mass rebuild 2013-12-27

* Thu Oct 03 2013 Steve Grubb <sgrubb@redhat.com> 2.3.2-3
resolves: #828495 - semanage port should generate an audit event

* Thu Aug 29 2013 Steve Grubb <sgrubb@redhat.com> 2.3.2-2
resolves: #991056 - ausearch ignores USER events with -ua option

* Mon Jul 29 2013 Steve Grubb <sgrubb@redhat.com> 2.3.2-1
- New upstream bugfix/enhancement release
resolves: #982112 Add delay between stopping and starting auditd

* Wed Jul 10 2013 Steve Grubb <sgrubb@redhat.com> 2.3.1-4
resolves: #982112 Add delay between stopping and starting auditd

* Wed Jul 03 2013 Steve Grubb <sgrubb@redhat.com> 2.3.1-3
- Remove prelude support

* Fri May 31 2013 Steve Grubb <sgrubb@redhat.com> 2.3.1-2
- Fix unknown lvalue in auditd.service (#969345)

* Thu May 30 2013 Steve Grubb <sgrubb@redhat.com> 2.3.1-1
- New upstream bugfix/enhancement release

* Fri May 03 2013 Steve Grubb <sgrubb@redhat.com> 2.3-2
- If no rules exist, copy shipped rules into place

* Tue Apr 30 2013 Steve Grubb <sgrubb@redhat.com> 2.3-1
- New upstream bugfix release

* Thu Mar 21 2013 Steve Grubb <sgrubb@redhat.com> 2.2.3-2
- Fix clone syscall interpretation

* Tue Mar 19 2013 Steve Grubb <sgrubb@redhat.com> 2.2.3-1
- New upstream bugfix release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Steve Grubb <sgrubb@redhat.com> 2.2.2-4
- Don't make auditd.service file executable (#896113)

* Fri Jan 11 2013 Steve Grubb <sgrubb@redhat.com> 2.2.2-3
- Do not own /usr/lib64/audit

* Wed Dec 12 2012 Steve Grubb <sgrubb@redhat.com> 2.2.2-2
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Steve Grubb <sgrubb@redhat.com> 2.2.1-1
- New upstream release

* Thu Mar 1 2012 Steve Grubb <sgrubb@redhat.com> 2.2-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Adam Williamson <awilliam@redhat.com> 2.1.3-4
- add in some systemd scriptlets that were missed, including one which
  will cause auditd to be enabled on upgrade from pre-systemd builds

* Wed Sep 14 2011 Steve Grubb <sgrubb@redhat.com> 2.1.3-3
- Enable by default (#737060)

* Tue Aug 30 2011 Steve Grubb <sgrubb@redhat.com> 2.1.3-2
- Correct misplaced ifnarch (#734359)

* Mon Aug 15 2011 Steve Grubb <sgrubb@redhat.com> 2.1.3-1
- New upstream release

* Tue Jul 26 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 2.1.2-2
- Introduce systemd unit file, drop SysV support

* Sat Jun 11 2011 Steve Grubb <sgrubb@redhat.com> 2.1.2-1
- New upstream release

* Wed Apr 20 2011 Steve Grubb <sgrubb@redhat.com> 2.1.1-1
- New upstream release

* Tue Mar 29 2011 Steve Grubb <sgrubb@redhat.com> 2.1-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Steve Grubb <sgrubb@redhat.com> 2.0.6-1
- New upstream release

* Thu Jan 20 2011 Karsten Hopp <karsten@redhat.com> 2.0.5-2
- bump and rebuild as 2.0.5-1 was erroneously linked with python-2.6 on ppc

* Tue Nov 02 2010 Steve Grubb <sgrubb@redhat.com> 2.0.5-1
- New upstream release

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 2.0.4-3
- audit-2.0.4-add-needed.patch: Fix FTBFS for --no-add-needed

* Fri Jan 29 2010 Steve Grubb <sgrubb@redhat.com> 2.0.4-2
- Split out static libs (#556039)

* Tue Dec 08 2009 Steve Grubb <sgrubb@redhat.com> 2.0.4-1
- New upstream release

* Sat Oct 17 2009 Steve Grubb <sgrubb@redhat.com> 2.0.3-1
- New upstream release

* Fri Oct 16 2009 Steve Grubb <sgrubb@redhat.com> 2.0.2-1
- New upstream release

* Mon Sep 28 2009 Steve Grubb <sgrubb@redhat.com> 2.0.1-1
- New upstream release

* Fri Aug 21 2009 Steve Grubb <sgrubb@redhat.com> 2.0-3
- New upstream release