Summary:	Arpwatch monitors changes in ethernet/ip address pairings
Summary(pl.UTF-8):	Arpwatch monitoruje zmiany w parach adresów ethernet/ip
Summary(ru.UTF-8):	Инструмент для отслеживания IP адресов в локальной сети
Summary(uk.UTF-8):	Інструмент для відслідковування IP адрес в локальній мережі
Name:		arpwatch
Version:	2.1a15
Release:	6
Epoch:		2
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.ee.lbl.gov/%{name}-%{version}.tar.gz
# Source0-md5:	cebfeb99c4a7c2a6cee2564770415fe7
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	dmassagevendor
Source4:	dmassagevendor.8
Source5:	https://ftp.debian.org/debian/pool/main/a/arpwatch/arpwatch_2.1a15-8.debian.tar.xz
# Source5-md5:	5e1a6414ae8cb98af3e0691be062a3d5
Patch0:		%{name}-opt.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arpwatch and arpsnmp are tools that monitors ethernet or FDDI activity
and maintain a database of ethernet/IP address pairings.

%description -l pl.UTF-8
Arpwatch i arpsnmp to narzędzia do monitorowania ethernetu i FDDI.
Dodatkowo tworzona jest baza par adresów ethernet/IP.

%description -l ru.UTF-8
Пакет arpwatch содержит утилиты arpwatch и arpsnmp. Они производят
мониторинг траффика в сетях Ethernet или FDDI и строят базы данных
адресных пар Ethernet/IP. Изменения в таких парах могут сообщаться при
помощи e-mail.

%description -l uk.UTF-8
Пакет arpwatch містить утиліти arpwatch та arpsnmp. Вони проводять
моніторинг трафіку в Ethernet чи FDDI мережах та будують бази даних
адресних пар Ethernet/IP. Зміни в таких парах можуть повідомлятись за
допомогою e-mail.

%prep
%setup  -q -a5
for p in $(cat debian/patches/series); do
	patch -p1 < "debian/patches/$p" || exit 1
done
%patch -P0 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure

%{__make} \
	ARPDIR=/var/lib/arpwatch

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/arpwatch,/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_var}/lib/%{name}}

%{__make} install install-man \
	DESTDIR=$RPM_BUILD_ROOT

install arp2ethers arpfetch $RPM_BUILD_ROOT%{_sbindir}
install bihourly.sh $RPM_BUILD_ROOT%{_sbindir}/bihourly
install *.{awk,dat} massagevendor{,-old} %{SOURCE3} $RPM_BUILD_ROOT/var/lib/arpwatch
install *.8 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8
install ethercodes.dat $RPM_BUILD_ROOT%{_var}/lib/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpwatch
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/arpwatch

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add arpwatch
%service arpwatch restart "arpwatch daemon"

%preun
if [ "$1" = "0" ]; then
	%service arpwatch stop
	/sbin/chkconfig --del arpwatch
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(754,root,root) /etc/rc.d/init.d/arpwatch
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/arpwatch
%{_mandir}/man8/*
%attr(750,daemon,root) %dir /var/lib/arpwatch
%attr(644,daemon,root) %config(noreplace) %verify(not md5 mtime size) /var/lib/arpwatch/arp.dat
%attr(755,daemon,root) /var/lib/arpwatch/*.awk
%attr(755,daemon,root) /var/lib/arpwatch/*massagevendor*
/var/lib/arpwatch/ethercodes.dat
