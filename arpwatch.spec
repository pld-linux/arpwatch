#
# TODO:
# - add UID entry in init-script - what UID???

Summary:	Arpwatch monitors changes in ethernet/ip address pairings
Summary(pl):	Arpwatch monitoruje zmiany w parach adresСw ethernet/ip
Summary(ru):	Инструмент для отслеживания IP адресов в локальной сети
Summary(uk):	╤нструмент для в╕дсл╕дковування IP адрес в локальн╕й мереж╕
Name:		arpwatch
Version:	2.1a11
Release:	5
Epoch:		2
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.ee.lbl.gov/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-arp2ethers.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-drop.patch
Patch4:		%{name}-drop-man.patch
BuildRequires:	libpcap-devel
Prereq:		rc-scripts >= 0.2.0
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arpwatch and arpsnmp are tools that monitors ethernet or fddi activity
and maintain a database of ethernet/ip address pairings.

%description -l pl
Arpwatch i arpsnmp to narzЙdzia do monitorowania ethernetu i fddi.
Dodatkowo tworzona jest baza par adresСw ethernet/ip.

%description -l ru
Пакет arpwatch содержит утилиты arpwatch и arpsnmp. Они производят
мониторинг траффика в сетях Ethernet или FDDI и строят базы данных
адресных пар Ethernet/IP. Изменения в таких парах могут сообщаться при
помощи e-mail.

%description -l uk
Пакет arpwatch м╕стить утил╕ти arpwatch та arpsnmp. Вони проводять
мон╕торинг траф╕ку в Ethernet чи FDDI мережах та будують бази даних
адресних пар Ethernet/IP. Зм╕ни в таких парах можуть пов╕домлятись за
допомогою e-mail.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

%build
%configure2_13
%{__make} ARPDIR=/var/lib/arpwatch

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/lib/arpwatch,etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install install-man DESTDIR=$RPM_BUILD_ROOT

install arp2ethers massagevendor $RPM_BUILD_ROOT/var/lib/arpwatch
install *.{awk,dat} $RPM_BUILD_ROOT/var/lib/arpwatch

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpwatch
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/arpwatch

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add arpwatch
if [ -f /var/lock/subsys/arpwatch ]; then
	/etc/rc.d/init.d/arpwatch restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/arpwatch start\" to start arpwatch daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/arpwatch ]; then
		/etc/rc.d/init.d/arpwatch stop 1>&2
	fi
	/sbin/chkconfig --del arpwatch
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES

%attr(754,root,root) /etc/rc.d/init.d/arpwatch
%attr(755,root,root) %{_sbindir}/*

%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/arpwatch

%{_mandir}/man8/*

%attr(750,daemon,root) %dir /var/lib/arpwatch
%attr(644,daemon,root) %config(noreplace) %verify(not size mtime md5) /var/lib/arpwatch/arp.dat
%attr(644,daemon,root) %config %verify(not size mtime md5) /var/lib/arpwatch/ethercodes.dat
%attr(755,daemon,root) /var/lib/arpwatch/*.awk

%attr(755,daemon,root) /var/lib/arpwatch/arp2ethers
%attr(755,daemon,root) /var/lib/arpwatch/massagevendor
