%define debug_package %{nil}
%define product_family LerOS
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Star
%define base_release_version 7
%define full_release_version 7.2
%define dist_release_version 7
%define ler_version 1.0
%define ler_patch_level SP1
%define ler_release 7
%define builtin_release_version 2
 
%define current_arch %{_arch}
%ifarch i386
%define current_arch x86
%endif

Name:		leros-release
Version:	%{ler_version}%{ler_patch_level}
Release:	%{ler_release}%{?dist}
Summary:	%{product_family} release file
Group:		System Environment/Base
License:	GPLv2
Provides:	leros-release = %{version}-%{release}
Provides:	redhat-release = %{full_release_version}
Provides:	centos-release = %{full_release_version}
Provides:	system-release = %{ler_version}%{ler_patch_level} 
Provides:	system-release(releasever) = %{ler_version}%{ler_patch_level} 
Source0:	leros-release-%{builtin_release_version}.tar.gz
Source1:	85-display-manager.preset
Source2:	90-default.preset
Requires:	rpm-embedded
BuildRequires:	python

%description
%{product_family} release files

%prep
%setup -q -n leros-release-%{builtin_release_version}
%ifarch aarch64
echo > LerOS-base.repo
%endif

%build 
echo OK 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
echo "LerOS release %{ler_version} (%{ler_patch_level})" > $RPM_BUILD_ROOT/etc/leros-release
ln -sf leros-release $RPM_BUILD_ROOT/etc/redhat-release
ln -sf leros-release $RPM_BUILD_ROOT/etc/system-release
ln -sf leros-release $RPM_BUILD_ROOT/etc/centos-release

# create /etc/os-release
cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME="LerOS"
VERSION="%{ler_version} (%{ler_patch_level})"
ID="leros"
ID_LIKE="rhel fedora centos"
VERSION_ID="%{ler_version}"
PRETTY_NAME="LerOS %{ler_version} (%{ler_patch_level})"
ANSI_COLOR="0;31"

EOF


# write cpe to /etc/system/release-cpe
echo "cpe:/o:ler:leros:%{version}:ga:server" > $RPM_BUILD_ROOT/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > $RPM_BUILD_ROOT/etc/issue
echo 'Kernel \r on an \m' >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

mkdir -p $RPM_BUILD_ROOT/usr/share/eula
cp eula.[!py]* $RPM_BUILD_ROOT/usr/share/eula

mkdir -p $RPM_BUILD_ROOT/var/lib
cp supportinfo $RPM_BUILD_ROOT/var/lib/supportinfo

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

# set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%centos 7
%%rhel 7
%%dist %%{nil} 
%%el%{base_release_version} 1
%%leros 2
EOF

# use unbranded datadir
mkdir -p -m 755 $RPM_BUILD_ROOT/%{_datadir}/leros-release
install -m 644 EULA $RPM_BUILD_ROOT/%{_datadir}/leros-release

# use unbranded docdir
mkdir -p -m 755 $RPM_BUILD_ROOT/%{_docdir}/leros-release
install -m 644 GPL $RPM_BUILD_ROOT/%{_docdir}/leros-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/

%clean
rm -rf $RPM_BUILD_ROOT

# If this is the first time a package containing /etc/issue
# is installed, we want the new files there. Otherwise, we
# want %config(noreplace) to take precedence.
%triggerpostun  -- redhat-release < 7.1.93-1
if [ -f /etc/issue.rpmnew ] ; then
   mv -f /etc/issue /etc/issue.rpmsave
   mv -f /etc/issue.rpmnew /etc/issue
fi
if [ -f /etc/issue.net.rpmnew ] ; then
   mv -f /etc/issue.net /etc/issue.net.rpmsave
   mv -f /etc/issue.net.rpmnew /etc/issue.net
fi

%post
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-LerOS 

%files
%defattr(0644,root,root,0755)
/etc/system-release
/etc/redhat-release
/etc/leros-release
/etc/centos-release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe 
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
/etc/rpm/macros.dist
%{_docdir}/leros-release/*
%{_datadir}/leros-release/*
%{_prefix}/lib/systemd/system-preset/*
/var/lib/supportinfo
/usr/share/eula/eula.*

%changelog
