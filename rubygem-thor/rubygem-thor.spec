%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from thor-0.12.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name thor
%global rubyabi 1.9.1

# There are not all test dependencies are available in RHEL.
%global enable_test 0%{!?rhel:1}

Summary: Scripting framework that replaces rake, sake and rubigen
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.19.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://whatisthor.com/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix}ruby(rubygems)
Requires: %{?scl_prefix}ruby(abi) = %{rubyabi}
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}ruby(abi) = %{rubyabi}
%if %{enable_test} > 0
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(fakeweb)
BuildRequires: git
%endif
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Thor is a scripting framework that replaces rake, sake and rubigen.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}
%{?scl:"}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%if %{enable_test} > 0
%check
pushd .%{gem_instdir}

# Drop bundler dependency
sed -i "s/require 'bundler'//" Thorfile

# kill simplecov dependency
sed -i '3,10d' spec/helper.rb

# This fixes on test failure due to encoding issues.
# https://github.com/wycats/thor/issues/278
sed -i '177 i\content.force_encoding "UTF-8"' spec/shell/basic_spec.rb

# Fix failing tests
# /components and .empty_directory are present in git under v0.18.1 tag,
# but missing in .gem so the tests are failing
mkdir spec/fixtures/doc/components
touch spec/fixtures/doc/components/.empty_directory

rspec spec
popd
%endif

%files
%{_bindir}/thor
%doc %{gem_instdir}/LICENSE.md
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Thorfile
%{gem_instdir}/spec
%{gem_instdir}/thor.gemspec

%changelog
* Mon Nov 24 2014 Joe Rafaniello <jrafanie@redhat.com> - 0.19.1-1
- Update to upstream 0.19.1
- Update for use with ruby 2.

* Mon Sep 23 2013 John Eckersberg <jeckersb@redhat.com> - 0.18.1-3
- Don't rewrite "/usr/bin/env ruby" shebang to "/usr/bin/ruby"

* Thu Jul 25 2013 Mo Morsi <mmorsi@redhat.com> - 0.18.1-2
- Imported into RHEL

* Thu Jul 25 2013 Josef Stribny <jstribny@redhat.com> - 0.18.1-1
- Update to Thor 0.18.1.

* Mon Mar 04 2013 Josef Stribny <jstribny@redhat.com> - 0.17.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Thor 0.17.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Vít Ondruch <vondruch@redhat.com> - 0.16.0-2
- Disable tests for EL builds.

* Tue Nov 13 2012 Vít Ondruch <vondruch@redhat.com> - 0.16.0-1
- Update to thor 0.16.0.
- Remove rubygem(diff-lcs) dependency, since it is just optional.
- Remove rubygem(ruby2ruby) dependnecy, since it is just optional, to allow
  conversion of Rakefiles to Thorfiles (but it doesnt work withou ParseTree anyway).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-5
- Enable tests.
- Add patches for the failing tests.
- Removed unnecessary ParseTree dependency.

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Mohammed Morsi <mmorsi@redhat.com> - 0.14.6-1
- Updated to latest upstream version

* Wed May 5 2010 Matthew Kent <mkent@magoazul.com> - 0.13.6-1
- New upstream version.

* Fri Dec 18 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-2
- Add Requires for rubygem(rake) (#542559).
- Upstream replaced Source after the gemcutter migration, update to latest
  (#542559).
- Add Requires for rubygem(diff-lcs) as Thor can take advantage of it for
  colourized diff output (#542559).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-1
- Initial package
