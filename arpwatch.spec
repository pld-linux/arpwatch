Summary:	Arpwatch monitors changes in ethernet/ip address pairings.
Summary(pl):	Arpwatch monitoruje zmiany w parach adresów ethernet/ip
Name:		arpwatch
Version:	2.1a4
Release:	8
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Copyright:	GPL
Source0:	ftp://ftp.ee.lbl.gov/%{name}-%{version}.tar.Z
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		arpwatch-arp2ethers.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
BuildRequires:	libpcap-devel
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Arpwatch and arpsnmp are tools that monitors ethernet or fddi activity and
maintain a database of ethernet/ip address pairings.

%description -l pl
Arpwatch i arpsnmp to narzêdzia do monitorowania ethernetu i fddi.
Dodatkowo tworzona jest baza par adresów ethernet/ip.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure
make ARPDIR=/var/state/arpwatch

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/state/arpwatch,etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT%{_sbindir},%{_mandir}/man8}

make install install-man DESTDIR=$RPM_BUILD_ROOT

install {arp2ethers,massagevendor} $RPM_BUILD_ROOT/var/state/arpwatch
install *.{awk,dat} $RPM_BUILD_ROOT/var/state/arpwatch

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpwatch
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/arpwatch

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README CHANGES

%post
/sbin/chkconfig --add arpwatch
if test -r /var/lock/subsys/arpwatch; then
	/etc/rc.d/init.d/arpwatch restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/arpwatch start\" to start arpwatch daemon."
fi

%preun
/sbin/chkconfig --del arpwatch
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del arpwatch
	/etc/rc.d/init.d/arpwatch stop 1>&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz CHANGES.gz

%attr(754,root,root) /etc/rc.d/init.d/arpwatch
%attr(755,root,root) %{_sbindir}/*

%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/arpwatch

%{_mandir}/man8/*

%dir    /var/state/arpwatch
%config(noreplace) %verify(not size mtime md5) /var/state/arpwatch/arp.dat
%config %verify(not size mtime md5) /var/state/arpwatch/ethercodes.dat
/var/state/arpwatch/*.awk

%attr(755,root,root) /var/state/arpwatch/arp2ethers
%attr(755,root,root) /var/state/arpwatch/massagevendor
