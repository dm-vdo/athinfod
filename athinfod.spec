# Disable auto-generation of debug_package
%global debug_package %{nil}

%define name athinfod
%define version 10.3
%define unmangled_version 10.3
%define release 6

Name:      %{name}
Version:   %{version}
Release:   %{release}
License:   MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
Vendor:    Debathena Project <debathena@mit.edu>
URL:       https://github.com/mit-athena/athinfod
Source0:   https://github.com/dm-vdo/athinfod/archive/refs/heads/main.tar.gz
Summary:   athinfo server

BuildRequires: python3 python3-setuptools
BuildRequires: systemd
Requires:      python3 python3-setuptools
%{?systemd_requires}

%description
Athinfod is a server for providing information to other hosts without
either requiring authentication from the remote host end OR creating
a security hole on the local host.

%prep
%setup -n %{name}-main

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
%{__install} -d $RPM_BUILD_ROOT%{_presetdir} -m 0755
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/athena -m 0755
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/athena/athinfo.defs.d -m 0755
%{__install} -d $RPM_BUILD_ROOT%{_unitdir} -m 0755
%{__install} -m 0644 01-athinfod.preset $RPM_BUILD_ROOT%{_presetdir}/01-athinfod.preset
%{__install} -m 0644 athinfo.access $RPM_BUILD_ROOT%{_sysconfdir}/athena/athinfo.access
%{__install} -m 0644 athinfo.defs $RPM_BUILD_ROOT%{_sysconfdir}/athena/athinfo.defs
%{__install} -m 0644 athinfod.service $RPM_BUILD_ROOT%{_unitdir}/athinfod@.service
%{__install} -m 0644 athinfod.socket $RPM_BUILD_ROOT%{_unitdir}/athinfod.socket

%post
%systemd_post athinfod.socket

%preun
%systemd_preun athinfod.socket

%postun
%systemd_postun_with_restart athinfod.socket

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%dir %{_sysconfdir}/athena
%dir %{_sysconfdir}/athena/athinfo.defs.d
%{_sysconfdir}/athena/athinfo.defs
%{_sysconfdir}/athena/athinfo.access
%{_unitdir}/athinfod.socket
%{_unitdir}/athinfod@.service
%{_presetdir}/01-athinfod.preset

%changelog
* Wed Jan 31 2024 Chung Chung <cchung@redhat.com> - 10.3-6
- Add python3-setuptools to require package since it is
  only installed in RHEL8 by default.

* Wed Jan 31 2024 Chung Chung <cchung@redhat.com> - 10.3-5
- Updated athinfo.defs to add checkReimage support.
- Replace distutils with setuptools in setup.py since distutils is deprecated.

* Wed Jun 28 2023 Joe Shimkus <jshimkus@redhat.com> - 10.3-4
- Updated athinfo.defs to add boot_id query.

* Mon Aug 22 2022 Joe Shimkus <jshimkus@redhat.com> - 10.3-3
- Updated athinfo.defs to add scam data queries.

* Tue Dec 14 2021 Andy Walsh <awalsh@redhat.com> - 10.3-2
- Updated athinfo.defs to add some lsblk queries.

* Tue Dec 14 2021 Andy Walsh <awalsh@redhat.com> - 10.2-2
- Updated to work with systemd on modern systems without xinet.d.

* Thu Dec 09 2021 Andy Walsh <awalsh@redhat.com> - 10.2-1
- Initial build
