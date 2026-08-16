#
# ethernet vendor table, regenerate with ./update-source.sh
%define		ouidate	20260816
#
Summary:	Arpwatch monitors changes in ethernet/ip address pairings
Summary(pl.UTF-8):	Arpwatch monitoruje zmiany w parach adresów ethernet/ip
Summary(ru.UTF-8):	Инструмент для отслеживания IP адресов в локальной сети
Summary(uk.UTF-8):	Інструмент для відслідковування IP адрес в локальній мережі
Name:		arpwatch
Version:	3.9
Release:	1
Epoch:		2
License:	BSD
Group:		Networking/Daemons
Source0:	https://ee.lbl.gov/downloads/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	2989e0dea96bb28ab24c30efebe55a33
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}@.service
Source4:	ethercodes-%{ouidate}.dat.xz
# Source4-md5:	ee731a1b4a43ed938fcd53f430c1ef6d
Patch0:		%{name}-time.patch
Patch1:		%{name}-c99.patch
Patch2:		%{name}-user.patch
Patch3:		%{name}-exit.patch
Patch4:		%{name}-bogon.patch
Patch5:		%{name}-freebsd.patch
Patch6:		%{name}-man.patch
Patch7:		%{name}-arp2ethers.patch
Patch8:		%{name}-arpfetch.patch
Patch9:		%{name}-path.patch
Patch10:	%{name}-quiet.patch
Patch11:	%{name}-nolocal.patch
URL:		https://ee.lbl.gov/
BuildRequires:	autoconf >= 2.71
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	systemd-units >= 38
Requires:	rc-scripts >= 0.2.0
Requires:	smtpdaemon
Requires:	systemd-units >= 38
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
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1

# the database directory is hardwired in the manuals and scripts
%{__sed} -i -e 's|/usr/local/arpwatch|/var/lib/%{name}|g' *.8.in *.sh.in *.sh

%build
%{__autoconf}
%configure \
	PYTHON=%{__python3} \
	--with-sendmail=/usr/lib/sendmail

%{__make} \
	ARPDIR=/var/lib/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{systemdunitdir}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/var/lib/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# make install uses 555, which keeps debuginfo extraction from writing
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/arp{snmp,watch}

install arp2ethers arpfetch $RPM_BUILD_ROOT%{_sbindir}
install massagevendor.py $RPM_BUILD_ROOT%{_sbindir}/massagevendor
install bihourly.sh $RPM_BUILD_ROOT%{_sbindir}/bihourly
install *.awk $RPM_BUILD_ROOT/var/lib/%{name}
install -m 644 arp.dat $RPM_BUILD_ROOT/var/lib/%{name}
%{__xz} -dc %{SOURCE4} > $RPM_BUILD_ROOT/var/lib/%{name}/ethercodes.dat

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}@.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "arpwatch daemon"
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%systemd_reload
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}@.service
%{_mandir}/man8/*
%attr(750,daemon,root) %dir /var/lib/%{name}
%attr(644,daemon,root) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/arp.dat
%attr(755,daemon,root) /var/lib/%{name}/*.awk
/var/lib/%{name}/ethercodes.dat
