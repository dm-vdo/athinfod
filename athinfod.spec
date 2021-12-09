%define name athinfo
%define version 10.2
%define unmangled_version 10.2
%define release 1

Name:      %{name}
Version:   %{version}
Release:   %{release}
License:   MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
Vendor:    Debathena Project <debathena@mit.edu>
URL:       https://github.com/mit-athena/athinfo
Source0:   https://gitlab.cee.redhat.com/vdo/open-sourcing/tools/third/athinfod/-/archive/master/athinfod-master.tar.gz
Summary:   athinfo server

BuildRequires: python3
Requires:      python3

%description
Athinfod is a server for providing information to other hosts without
either requiring authentication from the remote host end OR creating
a security hole on the local host.

%prep
%setup -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Thu Dec 09 2021 Andy Walsh <awalsh@redhat.com> - 10.2-1
- Initial build
