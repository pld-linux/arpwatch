Summary:	Arpwatch monitors changes in ethernet/ip address pairings.
Summary(pl):	Arpwatch monitoruje zmiany w parach adresów ethernet/ip
Name:		arpwatch
Version:	2.1a4
Release:	6
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Copyright:	GPL
Vendor:		PLD
Source0:	ftp://ftp.ee.lbl.gov/%{name}-%{version}.tar.Z	
Source1:	%{name}.init
Patch0:		%{name}-makefile.patch
BuildPrereq:	libpcap-devel
Prereq:		chkconfig
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

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
%configure
make ARPDIR=/var/db/arpwatch

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{var/db/arpwatch,etc/rc.d/init.d,usr/{sbin,share/man/man8}}

make install \
	DESTDIR=$RPM_BUILD_ROOT \
	install-man

for n in arp2ethers massagevendor; do
        install -m755 $n $RPM_BUILD_ROOT/var/db/arpwatch
done
for n in *.awk *.dat; do
        install -m644 $n $RPM_BUILD_ROOT/var/db/arpwatch
done

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpwatch

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/*
gzip -9nf README CHANGES

%post 
chkconfig --add arpwatch

%preun 
chkconfig --del arpwatch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc    README.gz CHANGES.gz

%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man8/*

%attr(750,root,root) /etc/rc.d/init.d/arpwatch

%dir    /var/db/arpwatch
%config(noreplace) %verify(not size mtime md5) /var/db/arpwatch/arp.dat
%config %verify(not size mtime md5) /var/db/arpwatch/ethercodes.dat
/var/db/arpwatch/*.awk

%attr(755,root,root) /var/db/arpwatch/arp2ethers
%attr(755,root,root) /var/db/arpwatch/massagevendor

%changelog
* Mon Jun 07 1999 Jan Rêkorajski <baggins@pld.org.pl>
  [2.1a4-6]
- spec cleanup

* Tue Feb 16 1999 Artur Frysiak <wiget@usa.net>
  [2.1a4-5d]
- initial release for PLD
