%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-gettext
Version:        0.3.3
Release:        3.5%{?dist}
Summary:        OCaml library for i18n

Group:          Development/Libraries
License:        LGPLv2+ with exceptions
URL:            http://sylvain.le-gall.net/ocaml-gettext.html
Source0:        http://sylvain.le-gall.net/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

Patch0:         ocaml-gettext-0.3.3-disable-tests.patch

BuildRequires:  ocaml >= 3.11.0-1
BuildRequires:  ocaml-findlib-devel >= 1.2.1-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-fileutils-devel >= 0.4.0
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
BuildRequires:  libxml2
BuildRequires:  chrpath
BuildRequires:  autoconf

%global __ocaml_requires_opts -i Asttypes -i Parsetree
%global __ocaml_provides_opts -i Pr_gettext


%description
Ocaml-gettext provides support for internationalization of Ocaml
programs.

Constraints :

* provides a pure Ocaml implementation,
* the API should be as close as possible to GNU gettext,
* provides a way to automatically extract translatable
  strings from Ocaml source code.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

# BZ 446919.
Requires:       ocaml-fileutils-devel >= 0.4.0


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q

%patch0 -p1


%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
  --libdir=%{_libdir} \
  --with-docbook-stylesheet=/usr/share/sgml/docbook/xsl-stylesheets \
  --disable-camomile
make


# Tests require camomile & ounit.
#%check
#pushd test
#../_build/bin/test
#popd


%install
rm -rf $RPM_BUILD_ROOT

# make install in the package is screwed up completely.  Install
# by hand instead.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}

# Remove *.o files - these shouldn't be distributed.
find _build -name '*.o' -exec rm {} \;

ocamlfind install gettext _build/lib/gettext/*
ocamlfind install gettext-stub _build/lib/gettext-stub/*
install -m 0755 _build/bin/ocaml-gettext $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 _build/bin/ocaml-xgettext $RPM_BUILD_ROOT%{_bindir}/

strip $OCAMLFIND_DESTDIR/stublibs/dll*.so
chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
strip $RPM_BUILD_ROOT%{_bindir}/ocaml-gettext


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext-stub
%if %opt
%exclude %{_libdir}/ocaml/gettext/*.a
%exclude %{_libdir}/ocaml/gettext/*.cmxa
%exclude %{_libdir}/ocaml/gettext/*.cmx
%exclude %{_libdir}/ocaml/gettext-stub/*.a
%exclude %{_libdir}/ocaml/gettext-stub/*.cmxa
%exclude %{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%exclude %{_libdir}/ocaml/gettext/*.ml
%exclude %{_libdir}/ocaml/gettext/*.mli
%exclude %{_libdir}/ocaml/gettext-stub/*.ml
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%defattr(-,root,root,-)
%doc README CHANGELOG TODO
# %doc build/share/doc/html/*
%if %opt
%{_libdir}/ocaml/gettext/*.a
%{_libdir}/ocaml/gettext/*.cmxa
%{_libdir}/ocaml/gettext/*.cmx
%{_libdir}/ocaml/gettext-stub/*.a
%{_libdir}/ocaml/gettext-stub/*.cmxa
%{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%{_libdir}/ocaml/gettext/*.ml
%{_libdir}/ocaml/gettext/*.mli
%{_libdir}/ocaml/gettext-stub/*.ml
%{_bindir}/ocaml-gettext
%{_bindir}/ocaml-xgettext


%changelog
* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3.5
- Since tests are disabled, we can drop BR ocaml-ounit.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3.4
- Remove camomile dependency completely.
- Disable tests, since they require camomile.  Also we have to patch
  out the tests in the Makefile since they run anyway (and break).

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3.1
- Import Fedora Rawhide package.
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml dependency generator.

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3
- Remove BR ocaml-camlidl.  No longer required to build this.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-2
- Rebuild for OCaml 3.11.2.

* Mon Nov  2 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-1
- New upstream release 0.3.3 (mainly small bugfixes).
- This requires ocaml-fileutils 0.4.0 and is incompatible with
  any earlier version.
- Fixed a number of rpmlint warnings with *.ml files in the
  non-devel package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-6
- Patch to temporarily fix missing dynlink.cma.
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-4
- Rebuild for OCaml 3.11.0

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-2
- Need to disable tests on ppc64 as well since the tests only work
  with gettext-camomile.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-1
- New upstream release 0.3.2 (fixeds rhbz 446916).

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-3
- Enable tests, add check section.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-2
- Patch to fix BZ 446916.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-1
- New upstream version 0.3.1.
- Extra runtime requirements (BZ 446919).

* Wed Apr 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-1
- New upstream version 0.3.0.
- Big patch no longer required (integrated with upstream).
- findlib < 1.2.1-3 known not to work with this.
- build/ -> _build/
- Re-enable documentation.
- Prevent *.o files from being distributed.
- Distribute *.cmx and *.mli files.

* Sat Apr 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-3.20080321patch
- Change the naming scheme to conform with "Snapshot packages" guideline.
- Don't duplicate all the docs in camomile-devel.
- Disable documentation.  Wants 'fop', but 'fop' throws a giant Java
  exception when present.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-2rwmj20080321
- Build camomile subpackages because the camomile dependency is
  rather large.  However we can't build camomile on ppc64 yet so
  don't build those subpackages there.

* Fri Mar 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-1rwmj20080321
- Initial RPM release.
