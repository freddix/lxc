Summary:	LXC - Userspace tools for the Linux kernel containers
Name:		lxc
Version:	0.9.0
Release:	2
License:	LGPL
Group:		Applications/System
Source0:	http://linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	8552a4479090616f4bc04d8473765fc9
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glibc-devel
BuildRequires:	libcap-devel
BuildRequires:	libseccomp-devel
BuildRequires:	pkg-config
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXC is a userspace interface for the Linux kernel containment features.
Through a powerful API and simple tools, it lets Linux users easily
create and manage system or application containers.

%package libs
Summary:	LXC library
Group:		Libraries

%description libs
LXC library.

%package devel
Summary:	Header files for LXC library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for LXC library.

%prep
%setup -q

# be mercyful
%{__sed} -i 's|-Werror ||' configure.ac

%build
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
    --enable-seccomp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/log/lxc

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%doc doc/examples/*.conf doc/FAQ.txt
%attr(755,root,root) %{_bindir}/lxc-attach
%attr(755,root,root) %{_bindir}/lxc-cgroup
%attr(755,root,root) %{_bindir}/lxc-checkconfig
%attr(755,root,root) %{_bindir}/lxc-checkpoint
%attr(755,root,root) %{_bindir}/lxc-clone
%attr(755,root,root) %{_bindir}/lxc-console
%attr(755,root,root) %{_bindir}/lxc-create
%attr(755,root,root) %{_bindir}/lxc-destroy
%attr(755,root,root) %{_bindir}/lxc-execute
%attr(755,root,root) %{_bindir}/lxc-freeze
%attr(755,root,root) %{_bindir}/lxc-info
%attr(755,root,root) %{_bindir}/lxc-kill
%attr(755,root,root) %{_bindir}/lxc-ls
%attr(755,root,root) %{_bindir}/lxc-monitor
%attr(755,root,root) %{_bindir}/lxc-netstat
%attr(755,root,root) %{_bindir}/lxc-ps
%attr(755,root,root) %{_bindir}/lxc-restart
%attr(755,root,root) %{_bindir}/lxc-shutdown
%attr(755,root,root) %{_bindir}/lxc-start
%attr(755,root,root) %{_bindir}/lxc-stop
%attr(755,root,root) %{_bindir}/lxc-unfreeze
%attr(755,root,root) %{_bindir}/lxc-unshare
%attr(755,root,root) %{_bindir}/lxc-version
%attr(755,root,root) %{_bindir}/lxc-wait

%dir %{_sysconfdir}/lxc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxc/default.conf

%dir %{_datadir}/lxc
%{_datadir}/lxc/lxc.functions

%dir %{_datadir}/lxc/hooks
%dir %{_datadir}/lxc/templates
%attr(755,root,root) %{_datadir}/lxc/hooks/mount*
%attr(755,root,root) %{_datadir}/lxc/templates/lxc-*

%dir %{_libdir}/lxc
%dir %{_libdir}/lxc/rootfs
%{_libdir}/lxc/rootfs/README
%attr(755,root,root) %{_libdir}/lxc/lxc-init

%dir %attr(750,root,root) /var/cache/lxc
%dir %attr(750,root,root) /var/log/lxc
%dir /var/lib/lxc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.0
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblxc.so
%{_includedir}/lxc
%{_pkgconfigdir}/lxc.pc

