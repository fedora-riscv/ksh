%define       releasedate   2004-12-25
# ExcludeArch:  ia64

Name:         ksh
Summary:      The Original ATT Korn Shell
URL:          http://www.kornshell.com/
Group:        Applications/Shells
License:      Common Public License Version 1.0
Version:      20041225
Release:      1
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.%{releasedate}.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.%{releasedate}.tgz
Source2:      http://www.research.att.com/~gsf/download/tgz/ast-base-locale.%{releasedate}.tgz
Patch0:       ksh-2004-02-29-ppc64.patch

#   build information
BuildRoot:    %{_tmppath}/%{name}-%{version}-root
Provides:     ksh93
Obsoletes:    ksh93
Provides:     pdksh
Obsoletes:    pdksh

%description
KSH-93 is the most recent version of the KornShell by David Korn of 
AT&T Bell Laboratories.
KornShell is a shell programming language, which is upward compatible
with "sh" (the Bourne Shell).

%prep
%setup -q -c
%setup -q -T -D -a 1
%setup -q -T -D -a 2
#%patch0 -p1 -b .ppc64

%build
./bin/package "read" ||:
./bin/package "make"
cp lib/package/LICENSES/ast LICENSE

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,%{_mandir}/man1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/{C,pt,fr,de,it,es}/LC_MESSAGES
install -c -s -m 755 arch/*/bin/ksh $RPM_BUILD_ROOT/bin/ksh
install -c -m 644 arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ksh.1
for i in C pt fr de it es; do
install -m 644 share/lib/locale/$i/LC_MESSAGES/* \
               $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/
done

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
        grep -v '^/bin/ksh$' /etc/shells >/etc/shells.new
        mv /etc/shells.new /etc/shells
        chmod 644 /etc/shells
fi

%verifyscript
echo -n "Looking for ksh in /etc/shells... "
if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from /etc/shells" >&2
else
    echo "found"
fi

%files 
%defattr(-, root, root)
%doc "-- *NOTICE*"
%doc README LICENSE
/bin/*
%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man1/*

%clean
    rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jan 21 2005 Karsten Hopp <karsten@redhat.de> 20041225-1
- rebuild with new ksh tarball (license change)

* Tue Nov 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-11
- disable ia64 for now

* Fri Oct 15 2004 Karsten Hopp <karsten@redhat.de> 20040229-9 
- rebuild

* Thu Sep 02 2004 Nalin Dahyabhai <nalin@redhat.com> 20040229-8
- remove '&' from summary

* Thu Sep 02 2004 Bill Nottingham <notting@redhat.com> 20040229-7
- obsolete pdksh (#131303)

* Mon Aug 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-6
- obsolete ksh93, provide ksh93

* Mon Jul 05 2004 Karsten Hopp <karsten@redhat.de> 20040229-3 
- add /bin/ksh to /etc/shells

* Wed Jun 16 2004 Karsten Hopp <karsten@redhat.de> 20040229-2 
- add ppc64 patch to avoid ppc64 dot symbol problem

* Fri May 28 2004 Karsten Hopp <karsten@redhat.de> 20040229-1 
- initial version

