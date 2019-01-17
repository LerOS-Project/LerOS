Summary: The compression and decompression library
Name: zlib
Version: 1.2.7
Release: 17%{?dist}
# /contrib/dotzlib/ have Boost license
License: zlib and Boost
Group: System Environment/Libraries
URL: http://www.zlib.net/
Source: http://www.zlib.net/zlib-%{version}.tar.bz2

Patch0: zlib-1.2.5-minizip-fixuncrypt.patch
# resolves: #805113
Patch1: zlib-1.2.7-optimized-s390.patch
# resolves: #844791
Patch2: zlib-1.2.7-z-block-flush.patch
# resolves: #1127330
Patch3: zlib-1.2.7-fix-serious-but-very-rare-decompression-bug-in-inftr.patch
# resolves: #1337441
Patch4: zlib-1.2.7-Fix-bug-where-gzopen-gzclose-would-write-an-empty-fi.patch

BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%package -n minizip
Summary: Library for manipulation with .zip archives
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description -n minizip
Minizip is a library for manipulation with files from .zip archives.

%package -n minizip-devel
Summary: Development files for the minizip library
Group: Development/Libraries
Requires: minizip = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%prep
%setup -q
%patch0 -p1 -b .fixuncrypt
%ifarch s390 s390x
%patch1 -p1 -b .optimized-deflate
%endif
%patch2 -p1 -b .z-flush
iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog.tmp
mv ChangeLog.tmp ChangeLog

%patch3 -p1
%patch4 -p1

%build
%ifarch ppc64 ppc64le
export CFLAGS="$RPM_OPT_FLAGS -O3"
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif

export LDFLAGS="$LDFLAGS -Wl,-z,relro"
./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
make %{?_smp_mflags}

cd contrib/minizip
autoreconf --install
%configure --enable-static=no
make %{?_smp_mflags}

%check
make test

%install
make install DESTDIR=$RPM_BUILD_ROOT

cd contrib/minizip
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%doc README ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%doc README doc/algorithm.txt test/example.c
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%doc README
%{_libdir}/libz.a

%files -n minizip
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Thu May 19 2016 jchaloup <jchaloup@redhat.com> - 1.2.7-17
- Fix writing empty files on gzopen()/gzclose()
  resolves: #1337441

* Wed Apr 27 2016 jchaloup <jchaloup@redhat.com> - 1.2.7-16
- Fix serious but very rare decompression bug in inftrees.c (upstream patch)
  resolves: #1127330

* Tue May 12 2015 Peter Robinson <pbrobinson@redhat.com> 1.2.7-15
- Rebuild for rhbz #1123500

* Thu Jul 31 2014 jchaloup <jchaloup@redhat.com> - 1.2.7-14
- resolves: #1123500
  recompiled with -O3 flag for ppc64le arch

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.7-13
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-12
- resolves: #1051079
  recompiled with -O3 flag for ppc64 arch

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.7-11
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct  4 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-9
- updated patch optimizing deflate on s390(x) architectures

* Wed Aug 29 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-8
- related: #832545
  reverted changes for this bug, static libraries shouldn't be compiled with
  -fPIC flag

* Mon Aug 27 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-7
- resolves: #844791
  rank Z_BLOCK flush below Z_PARTIAL_FLUSH only when last flush was Z_BLOCK
- done some minor .spec file cleanup

* Mon Aug 13 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-6
- added patch from IBM which optimizes deflate on s390(x) architectures

* Thu Aug 02 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-5
- resolves: #832545
  recompiled with -fPIC flag

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-3
- moved /lib* to /usr/lib*

* Mon Jun 11 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-2
- recompiled with -Wl,-z,relro flags

* Thu May 10 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.7-1
- resolves: #785726
- resolves: #805874
  update to 1.2.7

* Tue Jan 10 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.5-6
- resolves: #719139
  Zlib fails to read zip64 files on 64-bit system

* Fri Nov 11 2011 Tom Callaway <spot@fedoraproject.org> - 1.2.5-5
- fix minizip to permit uncrypt when NOUNCRYPT is not defined

* Wed Apr  6 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.5-4
- Resolves: #678603
  zlib from minizip allowed NULL pointer parameter of function unzGetCurrentFileInfo 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.5-2
- Resolves: #591317
  pdfedit fails to compile on i686 with zlib.h errors

* Thu Apr 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.5-1
- update to 1.2.5

* Mon Mar 29 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.4-1
- update to 1.2.4
  use the upstream make/configure files for zlib,
  change additional makefile/configure file to be used only to minizip
  add pkgconfig to zlib

* Mon Mar  8 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.3-25
- add Boost license

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.2.3-24
- Use bzipped upstream tarball.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Stepan Kasal <skasal@redhat.com> - 1.2.3-22
- fix the libz.so symlink

* Tue Mar 17 2009 Stepan Kasal <skasal@redhat.com> - 1.2.3-21
- consolidate the autoconfiscation patches into one and clean it up
- consequently, clean up the %%build and %%install sections
- zconf.h includes unistd.h again (#479133)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-19
- fix 473490 - unchecked malloc

* Wed Feb 13 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-18
- change license tag (226671#c29)

* Mon Feb 11 2008 Ivana Varekova <varekova@redhat.com> - 1.2.3-17
- spec file changes

* Fri Nov 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-16
- remove minizip headers to minizip-devel
- spec file cleanup
- fix minizip.pc file

* Wed Nov 14 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-15
- separate static subpackage

* Wed Aug 15 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-14
- create minizip subpackage

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-13
- remove .so,.a

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-12
- Resolves #240277
  Move libz to /lib(64)

* Mon Apr 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-11
- Resolves: 237295
  fix Summary tag

* Fri Mar 23 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-10
- remove zlib .so.* packages to /lib

* Fri Mar  9 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-9
- incorporate package review feedback

* Wed Feb 21 2007 Adam Tkac <atkac redhat com> - 1.2.3-8
- fixed broken version of libz

* Tue Feb 20 2007 Adam Tkac <atkac redhat com> - 1.2.3-7
- building is now automatized
- specfile cleanup

* Tue Feb 20 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-6
- remove the compilation part to build section
  some minor changes

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 1.2.3-5
- incorporate package review feedback

* Mon Oct 23 2006 Ivana Varekova <varekova@redhat.com> - 1.2.3-4
- fix #209424 - fix libz.a permissions

* Wed Jul 19 2006 Ivana Varekova <varekova@redhat.com> - 1.2.3-3
- add cflags (#199379)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Florian La Roche <laroche@redhat.com>
- update to 1.2.3

* Fri Jul 22 2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-5
- fix bug 163038 - CAN-2005-1849 - zlib buffer overflow

* Thu Jul 7  2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-4
- fix bug 162392 - CAN-2005-2096 

* Wed Mar 30 2005 Ivana Varekova <varekova@redhat.com> 1.2.2.2-3
- fix bug 122408 - zlib build process runs configure twice

* Fri Mar  4 2005 Jeff Johnson <jbj@redhat.com> 1.2.2.2-2
- rebuild with gcc4.

* Sat Jan  1 2005 Jeff Johnson <jbj@jbj.org> 1.2.2.2-1
- upgrade to 1.2.2.2.

* Fri Nov 12 2004 Jeff Johnson <jbj@jbj.org> 1.2.2.1-1
- upgrade to 1.2.2.1.

* Sun Sep 12 2004 Jeff Johnson <jbj@redhat.com> 1.2.1.2-1
- update to 1.2.1.2 to fix 2 DoS problems (#131385).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 18 2004 Jeff Johnson <jbj@jbj.org> 1.2.1.1-1
- upgrade to zlib-1.2.1.1.

* Sun Nov 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.1 release

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 1.2.0.7-3
- unrevert zlib.h include constants (#106291), rejected upstream.

* Wed Oct  8 2003 Jeff Johnson <jbj@jbj.org> 1.2.0.7-2
- fix: gzeof not set when reading compressed file (#106424).
- fix: revert zlib.h include constants for now (#106291).

* Tue Sep 23 2003 Jeff Johnson <jbj@redhat.com> 1.2.0.7-1
- update to 1.2.0.7, penultimate 1.2.1 release candidate.

* Tue Jul 22 2003 Jeff Johnson <jbj@redhat.com> 1.2.0.3-0.1
- update to release candidate.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 1.1.4-9
- rebuild, revert from 1.2.0.1.

* Mon Feb 24 2003 Jeff Johnson <jbj@redhat.com> 1.1.4-8
- fix gzprintf buffer overrun (#84961).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.1.4-7
- rebuilt

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 1.1.4-6
- Make ./configure use $CC to ease cross-compilation

* Tue Nov 12 2002 Jeff Johnson <jbj@redhat.com> 1.1.4-5
- rebuild from cvs.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr 26 2002 Jakub Jelinek <jakub@redhat.com> 1.1.4-2
- remove glibc patch, it is no longer needed (zlib uses gcc -shared
  as it should)
- run tests and only build the package if they succeed

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.1.4-1
- 1.1.4

* Wed Jan 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.1.3-25.7
- Fix double free

* Sun Aug 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.1.3-24
- Add example.c and minigzip.c to the doc files, as
  they are listed as examples in the README (#52574)

* Mon Jun 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Updated URL
- Add version dependency for zlib-devel
- s/Copyright/License/

* Wed Feb 14 2001 Trond Eivind Glomsrød <teg@redhat.com>
- bumped version number - this is the old version without the performance enhancements

* Fri Sep 15 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add -fPIC for shared libs (patch by Fritz Elfert)

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- on 64bit systems, make sure libraries are located correctly.

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 13 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging to build on solaris2.5.1.

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir} and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated URL and source location
- moved README to main package

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- link against glibc

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 1.1.3

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.2
- buildroot

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- added URL tag (down at the moment so it may not be correct)
- made zlib-devel require zlib

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
