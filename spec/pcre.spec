# This is stable release:
#%%global rcversion RC1
Name: pcre
Version: 8.32
Release: %{?rcversion:0.}17%{?rcversion:.%rcversion}%{?dist}.h6
%global myversion %{version}%{?rcversion:-%rcversion}
Summary: Perl-compatible regular expression library
Group: System Environment/Libraries
License: BSD
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Upstream thinks RPATH is good idea.
Patch0: pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1: pcre-8.32-refused_spelling_terminated.patch
# In upstream after 8.32
Patch2: pcre-8.32-Fix-forward-search-in-JIT-when-link-size-is-3-or-gre.patch
# In upstream after 8.32
Patch3: pcre-8.32-Fix-two-buffer-over-read-issues-in-16-and-32-bit-mod.patch
# Fix pcregrep on empty line, in upstream after 8.33-RC1
Patch4: pcre-8.33-RC1-Fix-pcregrep-so-that-it-can-find-empty-lines.patch
# Grow buffer in pcretest properly, in upstream after 8.33-RC1
Patch5: pcre-8.33-RC1-Fix-pcretest-crash-with-a-data-line-longer-than-6553.patch
# Fix passing too small output vector to pcre_dfa_exec, in upstream after
# 8.33-RC1, bug #963284
Patch6: pcre-8.33-RC1-Fix-segfault-when-pcre_dfa_exec-is-called-with-an-ou.patch
# Fix jitted range check, in upstream after 8.34, bug #1048101
Patch7: pcre-8.34-Fix-range-check-in-JIT-path.patch
# Fix unused memory usage on zero-repeat assertion condition, bug #1169797,
# CVE-2014-8964, in upstream after 8.36
Patch8: pcre-8.32-Fix-zero-repeat-assertion-condition-bug.patch
# Fix compiling expression where start-anchored character with more than one
# other case follows circumflex in multiline UTF mode, bug #1110621,
# in upstream 8.36
Patch9: pcre-8.32-Fix-bad-starting-data-when-char-with-more-than-one-o.patch
# Fix character class with a literal quotation, bug #1111091,
# upstream bug #1494, in upstream after 8.35
Patch10: pcre-8.32-Fix-bad-compile-of-Qx-.-where-x-is-any-character.patch
# Fix empty-matching possessive zero-repeat groups in interpreted mode,
# bug #1119320, upstream bug #1500, in upstream after 8.35
Patch11: pcre-8.33-Fix-empty-matching-possessive-zero-repeat-groups-bug.patch
# Fix compiler crash for zero-repeated groups with a recursive back reference,
# bug #1119356, upstream bug #1503, in upstream after 8.35
Patch12: pcre-8.32-Fix-compiler-crash-misbehaviour-for-zero-repeated-gr.patch
# Reset non-matched groups within capturing group up to forced match,
# bug #1161597, in upstream after 8.36
Patch13: pcre-8.32-Fix-bug-when-there-are-unset-groups-prior-to-ACCEPT-.patch
# Fix static linking, bug #1217111, in upstream after 8.37-RC1
Patch14: pcre-8.37-RC1-Fix-static-linking-issue-with-pkg-config.patch
# Fix checking whether a group could match an empty string, bug #1330509,
# in upstream after 8.33, needed for
# Fix-compile-time-loop-for-recursive-reference-within.patch
Patch15: pcre-8.32-Fix-checking-whether-a-group-could-match-an-empty-st.patch
# Fix CVE-2015-2328 (infinite recursion compiling pattern with recursive
# reference in a group with indefinite repeat), bug #1330509,
# upstream bug #1515, in upstream after 8.35
Patch16: pcre-8.32-Fix-compile-time-loop-for-recursive-reference-within.patch
# Fix duplicate names memory calculation error, bug #1330509,
# in upstream after 8.37,
# needed for Fix-buffer-overflow-for-named-references-in-situatio.patch
Patch17: pcre-8.32-Fix-duplicate-names-memory-calculation-error.patch
# Fix named forward reference to duplicate group number overflow bug,
# bug #1330509, in upstream after 8.37,
# needed for Fix-buffer-overflow-for-named-references-in-situatio.patch
Patch18: pcre-8.32-Fix-named-forward-reference-to-duplicate-group-numbe.patch
# Fix CVE-2015-8385 (buffer overflow caused by named forward reference to
# duplicate group number), bug #1330509, in upstream after 8.37
Patch19: pcre-8.32-Fix-buffer-overflow-for-named-references-in-situatio.patch
# Fix CVE-2015-8386 (buffer overflow caused by lookbehind assertion),
# bug #1330509, in upstream after 8.37
Patch20: pcre-8.32-Fix-buffer-overflow-for-lookbehind-within-mutually-r.patch
# Fix CVE-2015-3217 (stack overflow caused by mishandled group empty match),
# bug #1330509, in upstream after 8.37
Patch21: pcre-8.32-Fix-group-empty-match-bug.patch
# Fix CVE-2015-5073 and CVE-2015-8388 (buffer overflow for forward reference
# within backward assertion with excess closing parenthesis), bug #1330509,
# in upstream after 8.37
Patch22: pcre-8.32-Fix-buffer-overflow-for-forward-reference-within-bac.patch
# Fix CVE-2015-8391 (inefficient posix character class syntax check),
# bug #1330509, in upstream after 8.37
Patch23: pcre-8.32-Fix-run-for-ever-bug-for-deeply-nested-sequences.patch
# Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
# parentheses), bug #1330509, in upstream after 8.38
Patch24: pcre-8.32-Fix-workspace-overflow-for-ACCEPT-with-deeply-nested.patch
# 1/3 Let [:graph:], [:print:], and [:punct:] POSIX classes to handle Unicode
# characters in UCP mode to match Perl behavior, bug #1400267,
# in upstream 8.34
Patch25: pcre-8.32-Update-POSIX-class-handling-in-UCP-mode.patch
# 2/3 Let [:graph:], [:print:], and [:punct:] POSIX classes to handle Unicode
# characters in UCP mode with JIT, bug #1400267, in upstream 8.34
Patch26: pcre-8.32-Add-support-for-PT_PXGRAPH-PT_PXPRINT-and-PT_PXPUNCT.patch
# 3/3 Fix XCLASS POSIX JIT compilation, tests failed on 32-bit PowerPC,
# bug #1400267, in upstream 8.34
Patch27: pcre-8.34-RC1-Fix-XCLASS-POSIX-types-in-JIT.patch
# Fix matching Unicode ranges in JIT mode, bug #1402288, in upstream 8.35
Patch28: pcre-8.32-A-new-flag-is-set-when-property-checks-are-present-i.patch

Patch1001: pcre-upstream-CVE-2015-8380.patch
Patch1002: pcre-upstream-CVE-2015-8387.patch
Patch1003: pcre-upstream-CVE-2015-8390.patch
Patch1004: pcre-upstream-CVE-2015-8394.patch
# pcre-8.32 fails test with GCC 4.9
Patch1005: pcre-8.32-Do-not-rely-on-wrapping-signed-integer-while-parsein.patch

# git required for A-new-flag-is-set-when-property-checks-are-present-i.patch
BuildRequires: git
BuildRequires: readline-devel
# New libtool to get rid of rpath
BuildRequires: autoconf, automake, libtool
BuildRequires: gcc-c++

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package embedded
Summary: Perl-compatible regular expression library
Group: System Environment/Libraries

%description embedded
pcre library

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary: Static library for %{name}
Group: Development/Libraries
Requires: %{name}-devel%{_isa} = %{version}-%{release}

%description static
Library for static linking for %{name}.

%package tools
Summary: Auxiliary utilities for %{name}
Group: Development/Tools
Requires: %{name}%{_isa} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%prep
%setup -q -n %{name}-%{myversion}
# Get rid of rpath
%patch0 -p1 -b .multilib
%patch1 -p1 -b .terminated_typos
%patch2 -p1 -b .forward_jit
%patch3 -p1 -b .buffer_over_read
%patch4 -p1 -b .pcregrep_empty_line
%patch5 -p1 -b .pcretest_grow_buffer
%patch6 -p1 -b .vector_size
%patch7 -p1 -b .jitted_range_check
%patch8 -p1 -b .zero_repeat_assertion
%patch9 -p1 -b .starting_data
%patch10 -p1 -b .class_with_literal
%patch11 -p1 -b .empty_zero_repeat_group
%patch12 -p1 -b .compiler_crash_zero_group
%patch13 -p1 -b .reset_groups
%patch14 -p1 -b .static_linking
%patch15 -p1 -b .group_match_empty
%patch16 -p1 -b .compiler_loop_recursive_reference
%patch17 -p1 -b .duplicate_names_memory_calculation
%patch18 -p1 -b .forward_reference_to_duplicate_group_number
%patch19 -p1 -b .named_references_in_pqp
%patch20 -p1 -b .lookbehind_within_mutally_recusive_subroutines
%patch21 -p1 -b .group_empty_match
%patch22 -p1 -b .CVE-2015-5073
%patch23 -p1 -b .deeply_nested_bracket_colon
%patch24 -p1 -b .accept_with_nested_parentheses
%patch25 -p1 -b .posix_classes_in_ucp
%patch26 -p1 -b .posix_classes_in_ucp_jit
%patch27 -p1 -b .posix_classes_in_ucp_jit_types
# Apply a Git binary patch
git --work-tree=. apply %{PATCH28}
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%ifarch aarch64
%patch1005 -p1
%endif

# Because of rpath patch
libtoolize --copy --force && autoreconf -vif
# One contributor's name is non-UTF-8
#for F in ChangeLog; do
#    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
#    touch --reference "$F" "${F}.utf8"
#    mv "${F}.utf8" "$F"
#done

%build
# There is an explicit request to optimize PCRE more, bugs #1051072, #1123498
%global _performance_build 1
%ifarch ppc64
# There is a strict-aliasing problem on PPC64, bug #881232
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch aarch64 ppc64le s390 s390x sparc64 sparcv9
    --disable-jit \
%else
    --enable-jit \
%endif
    --enable-pcretest-libreadline --enable-utf --enable-unicode-properties \
    --enable-pcre8 --enable-pcre16 --enable-pcre32
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%check
%ifarch s390 ppc
# larger stack is needed on s390, ppc
ulimit -s 10240
%endif
make check VERBOSE=yes

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libpcre16.so.*
%{_libdir}/libpcre32.so.*
%{_libdir}/libpcrecpp.so.*
%{_libdir}/libpcreposix.so.*
%doc AUTHORS COPYING LICENCE NEWS README ChangeLog

%files embedded
%{_libdir}/libpcre.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre-config.*
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc HACKING pcredemo.c

%files static
%{_libdir}/*.a
%doc COPYING LICENCE 

%files tools
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.*
%{_mandir}/man1/pcretest.*

%changelog
* Tue Dec 06 2016 Petr Pisar <ppisar@redhat.com> - 8.32-17
- Let [:graph:], [:print:], and [:punct:] POSIX classes to handle Unicode
  characters in UCP mode to match Perl behavior (bug #1400267)
- Fix matching Unicode ranges in JIT mode (bug #1402288)

* Wed Apr 27 2016 Petr Pisar <ppisar@redhat.com> - 8.32-16
- Fix CVE-2015-2328 (infinite recursion compiling pattern with recursive
  reference in a group with indefinite repeat) (bug #1330509)
- Fix CVE-2015-8385 (buffer overflow caused by named forward reference to
  duplicate group number) (bug #1330509)
- Fix CVE-2015-8386 (buffer overflow caused by lookbehind assertion)
  (bug #1330509)
- Fix CVE-2015-3217 (stack overflow caused by mishandled group empty match)
  (bug #1330509)
- Fix CVE-2015-5073 and CVE-2015-8388 (buffer overflow for forward reference
  within backward assertion with excess closing parenthesis) (bug #1330509)
- Fix CVE-2015-8391 (inefficient posix character class syntax check)
  (bug #1330509)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (bug #1330509)

* Wed Apr 29 2015 Petr Pisar <ppisar@redhat.com> - 8.32-15
- Fix compiling expression where start-anchored character with more than one
  other case follows circumflex in multiline UTF mode (bug #1110621)
- Fix character class with a literal quotation (bug #1111091)
- Fix empty-matching possessive zero-repeat groups in interpreted mode
  (bug #1119320)
- Fix compiler crash for zero-repeated groups with a recursive back reference
  (bug #1119356)
- Reset non-matched groups within capturing group up to forced match
  (bug #1161597)
- Fix static linking (bug #1217111)
- Package pcredemo.c as a documentation for pcre-devel (bug #1217118)

* Tue Dec 02 2014 Petr Pisar <ppisar@redhat.com> - 8.32-14
- Fix CVE-2014-8964 (unused memory usage on zero-repeat assertion condition)
  (bug #1169797)

* Fri Aug 01 2014 Petr Pisar <ppisar@redhat.com> - 8.32-13
- Disable unsupported JIT mode on little-endian 64-bit PowerPC platform
  (bug #1125642)
- Raise optimization level to 3 on little-endian 64-bit PowerPC (bug #1123498)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 8.32-12
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Petr Pisar <ppisar@redhat.com> - 8.32-11
- Raise optimization to level 3 on 64-bit PowerPC (bug #1051072)

* Thu Jan 09 2014 Petr Pisar <ppisar@redhat.com> - 8.32-10
- Fix jitted range check (bug #1048101)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 8.32-9
- Mass rebuild 2013-12-27

* Wed Oct 16 2013 Petr Pisar <ppisar@redhat.com> - 8.33-8
- Disable strict-aliasing on PPC64 (bug #881232)

* Mon Jun 03 2013 Petr Pisar <ppisar@redhat.com> - 8.32-7
- Disable unsupported JIT on aarch64 (bug #969693)

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 8.32-6
- Fix passing too small output vector to pcre_dfa_exec (bug #963284)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 8.32-5
- Fix bad handling of empty lines in pcregrep tool (bug #961789)
- Fix possible pcretest crash with a data line longer than 65536 bytes

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 8.32-4
- Fix forward search in JIT when link size is 3 or greater
- Fix buffer over-read in UTF-16 and UTF-32 modes with JIT

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 8.32-3
- Adjust autoreconf to fix FTBFS on F-19

* Mon Jan 07 2013 Petr Pisar <ppisar@redhat.com> - 8.32-2
- Make inter-subpackage dependencies architecture specific (bug #892187)

* Fri Nov 30 2012 Petr Pisar <ppisar@redhat.com> - 8.32-1
- 8.32 bump

* Thu Nov 29 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.2.RC1
- Inter-depend sub-packages to prevent from mixing different versions

* Tue Nov 13 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.1.RC1
- 8.32-RC1 bump

* Mon Sep 03 2012 Petr Pisar <ppisar@redhat.com> - 8.31-2
- Set re_nsub in regcomp() properly (bug #853990)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.31-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Petr Pisar <ppisar@redhat.com> - 8.31-1
- 8.31 bump

* Tue Jun 05 2012 Petr Pisar <ppisar@redhat.com> - 8.31-0.1.RC1
- 8.31-RC1 bump

* Sat May 12 2012 Tom Callaway <spot@fedoraproject.org> - 8.30-7
- disable jit for sparcv9 and sparc64

* Fri May 11 2012 Petr Pisar <ppisar@redhat.com> - 8.30-6
- Fix spelling in manual pages (bug #820978)

* Mon Apr 23 2012 Petr Pisar <ppisar@redhat.com> - 8.30-5
- Possessify high ASCII (bug #815217)
- Fix ovector overflow (bug #815214)

* Fri Apr 20 2012 Petr Pisar <ppisar@redhat.com> - 8.30-4
- Possesify \s*\R (bug #813237)

* Thu Apr 05 2012 Petr Pisar <ppisar@redhat.com> - 8.30-3
- Fix look-behind assertion in UTF-8 JIT mode (bug #810314)

* Tue Feb 28 2012 Petr Pisar <ppisar@redhat.com> - 8.30-2
- Remove old libpcre.so.0 from distribution
- Move library to /usr

* Thu Feb 09 2012 Petr Pisar <ppisar@redhat.com> - 8.30-1
- 8.30 bump
- Add old libpcre.so.0 to preserve compatibility temporarily

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 8.30-0.1.RC1
- 8.30 Relase candidate 1 with UTF-16 support and *API change*
- Enable UTF-16 variant of PCRE library
- The pcre_info() function has been removed from pcre library.
- Loading compiled pattern does not fix endianity anymore. Instead an errror
  is returned and the application can use pcre_pattern_to_host_byte_order() to
  convert the pattern.
- Surrogates (0xD800---0xDFFF) are forbidden in UTF-8 mode now.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.21-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Petr Pisar <ppisar@redhat.com> - 8.21-2
- Fix unmatched subpattern to not become wildcard (bug #769597)
- Fix NULL pointer derefernce in pcre_free_study() (upstream bug #1186)

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 8.21-1
- 8.21 bump

* Thu Dec 08 2011 Karsten Hopp <karsten@redhat.com> 8.21-0.2.RC1
- ppc needs a larger stack similar to s390

* Tue Dec 06 2011 Petr Pisar <ppisar@redhat.com> - 8.21-0.1.RC1
- 8.21-RC1 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 8.20-7
- Fix case-less match if cases differ in encoding length (bug #756675)

* Fri Nov 25 2011 Petr Pisar <ppisar@redhat.com> - 8.20-6
- Fix cache-flush in JIT on PPC

* Tue Nov 22 2011 Petr Pisar <ppisar@redhat.com> - 8.20-5
- Fix repeated forward reference (bug #755969)

* Wed Nov 16 2011 Petr Pisar <ppisar@redhat.com> - 8.20-4
- Fix other look-behind regressions

* Tue Nov 15 2011 Petr Pisar <ppisar@redhat.com> - 8.20-3
- Fix look-behind regression in 8.20

* Tue Nov 15 2011 Dan Horák <dan[at]danny.cz> - 8.20-2
- fix build on s390(x) - disable jit and use larger stack for tests

* Fri Oct 21 2011 Petr Pisar <ppisar@redhat.com> - 8.20-1
- 8.20 bump

* Tue Oct 11 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC3
- 8.20-RC3 bump

* Fri Sep 23 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC2
- 8.20-RC2 bump

* Mon Sep 12 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC1
- 8.20-RC1 bump with JIT

* Tue Sep 06 2011 Petr Pisar <ppisar@redhat.com> - 8.13-4
- Fix infinite matching PRUNE (bug #735720)

* Mon Aug 22 2011 Petr Pisar <ppisar@redhat.com> - 8.13-3
- Fix parsing named class in expression (bug #732368)

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-2
- Separate utilities from libraries
- Move pcre-config(1) manual to pcre-devel sub-package
- Remove explicit defattr from spec code
- Compile pcretest with readline support

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-1
- 8.13 bump: Bug-fix version, Unicode tables updated to 6.0.0, new pcregrep
  option --buffer-size to adjust to long lines, new feature is passing of
  *MARK information to callouts.
- Should fix crash back-tracking over unicode sequence (bug #691319)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-4
- Fix caseless reference matching in UTF-8 mode when the upper/lower case
  characters have different lengths (bug #702623)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-3
- Fix typos in manual pages (bugs #675476, #675477)
- Clean spec file up

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Petr Pisar <ppisar@redhat.com> - 8.12-1
- 8.12 bump
- Remove accepted pcre-8.11-Fix-typo-in-pcreprecompile-3.patch

* Mon Dec 13 2010 Petr Pisar <ppisar@redhat.com> - 8.11-1
- 8.11 bump
- See ChangeLog for changes. Namely changes have been made to the way
  PCRE_PARTIAL_HARD affects the matching of $, \z, \Z, \b, and \B.
- Fix typo in pcreprecompile(3) manual
- Document why shared library is not under /usr

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 8.10-1
- 8.10 bump (bug #612635)
- Add LICENCE to static subpackage because COPYING refers to it
- Remove useless rpath by using new libtool (simple sed does not work anymore
  because tests need to link against just-compiled library in %%check phase)

* Thu Jul 08 2010 Petr Pisar <ppisar@redhat.com> - 7.8-4
- Add COPYING to static subpackage
- Remove useless rpath

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> - 7.8-1
- Update to 7.8, drop upstreamed patches
- Fix destination of documentation (#427763)
- Use buildroot macro consistently
- Separate the static library, as per current Guidelines
- Satisfy rpmlint

* Fri Jul  4 2008 Tomas Hoger <thoger@redhat.com> - 7.3-4
- Apply Tavis Ormandy's patch for CVE-2008-2371.

* Tue Feb 12 2008 Tomas Hoger <thoger@redhat.com> - 7.3-3
- Backport patch from upstream pcre 7.6 to address buffer overflow
  caused by "a character class containing a very large number of
  characters with codepoints greater than 255 (in UTF-8 mode)"
  CVE-2008-0674, #431660
- Try re-enabling make check again.

* Fri Nov 16 2007 Stepan Kasal <skasal@redhat.com> - 7.3-2
- Remove obsolete ``reqs''
- add dist tag
- update BuildRoot

* Mon Sep 17 2007 Than Ngo <than@redhat.com> - 7.3-1
- bz292501, update to 7.3

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 7.0-1
- 7.0

* Mon Nov 27 2006 Than Ngo <than@redhat.com> - 6.7-1
- update to 6.7
- fix #217303, enable-unicode-properties
- sane stack limit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Tue May 09 2006 Than Ngo <than@redhat.com> 6.6-1
- update to 6.6
- fix multilib problem

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Than Ngo <than@redhat.com> 6.3-1
- update to 6.3

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 5.0-4
- rebuild

* Fri Feb 11 2005 Joe Orton <jorton@redhat.com> 5.0-3
- don't print $libdir in 'pcre-config --libs' output

* Thu Nov 18 2004 Joe Orton <jorton@redhat.com> 5.0-2
- include LICENCE, AUTHORS in docdir
- run make check
- move %%configure to %%build

* Thu Nov 18 2004 Than Ngo <than@redhat.com> 5.0-1
- update to 5.0
- change License: BSD
- fix header location #64248

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 4.5-2
- add the correct pcre license, #118781

* Fri Mar 12 2004 Than Ngo <than@redhat.com> 4.5-1
- update to 4.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 4.4-1
- 4.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Than Ngo <than@redhat.com> 4.2-1
- update to 4.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 3.9-9
- build with utf8, bug #81504

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 3.9-8
- Really remove .la files

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 3.9-7
- remove .la

* Thu Oct 10 2002 Than Ngo <than@redhat.com> 3.9-7
- Typo bug

* Wed Oct  9 2002 Than Ngo <than@redhat.com> 3.9-6
- Added missing so symlink

* Thu Sep 19 2002 Than Ngo <than@redhat.com> 3.9-5.1
- Fixed to build s390/s390x/x86_64

* Thu Jun 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-5
- Fix #65009

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-2
- rebuild

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-1
- Update to 3.9

* Wed Nov 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.7-1
- Update to 3.7

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.4-2
- Move libpcre to /lib, grep uses it these days (#41104)

* Wed Apr 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Move this to a separate package, used to be in kdesupport, but it's
  generally useful...
