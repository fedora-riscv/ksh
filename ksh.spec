Name:         ksh
Summary:      The Original AT&T Korn Shell
URL:          http://www.kornshell.com/
Group:        System Environment/Shells
License:      AT&T
Version:      20020628
Release:      1
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.2002-06-28.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.2002-06-28.tgz
BuildRoot:    %{_tmppath}/%{name}-%{version}.root
Obsoletes:    pdksh

%description
The KornShell language was designed and developed by David G. Korn
at AT&T Bell Laboratories. It is an interactive command language
that provides access to the UNIX system and to many other systems,
on the many different computers and workstations on which it is
implemented. This is Ksh93 which is intended to conform to the Shell
Language Standard developed by the IEEE POSIX 1003.2 Shell and
Utilities Language Committee.

%prep
%setup0 -q -c -n ksh-%{version}
%setup1 -q -T -D -a 1

%build
./bin/package read || true
./bin/package make CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE64_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 \
	$RPM_BUILD_ROOT%{_bindir} \
        $RPM_BUILD_ROOT%{_mandir}/man1
install -c -m 755 \
        arch/*/bin/ksh $RPM_BUILD_ROOT%{_bindir}/ksh
install -c -m 644 \
        arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ksh.1

# rename license file
mv lib/package/LICENSES/ast LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%post 
if [ ! -f /etc/shells ]; then
        echo "/bin/ksh" > /etc/shells
else
        if ! grep -q '^/bin/ksh$' /etc/shells ; then
                echo "/bin/ksh" >> /etc/shells
        fi
fi

%postun 
if [ ! -f /bin/ksh ]; then
        grep -v /bin/ksh /etc/shells > /etc/shells.new
        mv /etc/shells.new /etc/shells
fi

%files
%{_bindir}/ksh
%{_mandir}/man1/*
%doc LICENSE

%changelog
* Wed Jul 17 2002 Preston Brown <pbrown@redhat.com>
- initial Red Hat packaging of ksh93

