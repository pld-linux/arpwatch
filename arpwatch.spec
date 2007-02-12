Summary:	Arpwatch monitors changes in ethernet/ip address pairings
Summary(pl.UTF-8):   Arpwatch monitoruje zmiany w parach adresów ethernet/ip
Summary(ru.UTF-8):   Инструмент для отслеживания IP адресов в локальной сети
Summary(uk.UTF-8):   Інструмент для відслідковування IP адрес в локальній мережі
Name:		arpwatch
Version:	2.1a14
Release:	0.9
Epoch:		2
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.ee.lbl.gov/%{name}-%{version}.tar.gz
# Source0-md5:	a80f26ba58012755dbb9fd99fb3af660
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	dmassagevendor
Source4:	dmassagevendor.8
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-opt.patch
Patch10:	%{name}-debian_05debian_fhs.patch
Patch11:	%{name}-debian_06debian_manpages.patch
Patch12:	%{name}-debian_10getopt_patchable.patch
Patch13:	%{name}-debian_11opt_sendmail_path.patch
Patch14:	%{name}-debian_12opt_nopromisc.patch
Patch15:	%{name}-debian_13opt_allsubnets.patch
Patch16:	%{name}-debian_14opt_mailto.patch
Patch17:	%{name}-debian_15opt_username.patch
Patch18:	%{name}-debian_16opt_quiet.patch
Patch19:	%{name}-debian_17opt_ignorenet.patch
Patch20:	%{name}-debian_21arp2ethers.patch
Patch21:	%{name}-debian_22secure_tempfile.patch
Patch22:	%{name}-debian_24from_field.patch
Patch23:	%{name}-debian_25ignore_zero_ip.patch
Patch24:	%{name}-debian_26unconf_iface.patch
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
%setup  -q
%patch0 -p1
%patch1 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

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
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_datadir}/%{name}}

%{__make} install install-man \
	DESTDIR=$RPM_BUILD_ROOT

install arp2ethers arpfetch bihourly $RPM_BUILD_ROOT%{_sbindir}
install *.{awk,dat} massagevendor{,-old} %{SOURCE3} $RPM_BUILD_ROOT/var/lib/arpwatch
install *.8 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8
install ethercodes.dat $RPM_BUILD_ROOT%{_datadir}/%{name}

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
%{_datadir}/%{name}
%{_mandir}/man8/*
%attr(750,daemon,root) %dir /var/lib/arpwatch
%attr(644,daemon,root) %config(noreplace) %verify(not md5 mtime size) /var/lib/arpwatch/arp.dat
%attr(755,daemon,root) /var/lib/arpwatch/*.awk
%attr(755,daemon,root) /var/lib/arpwatch/*massagevendor*
