%define		trac_ver	0.11
%define		plugin		componentdependency
Summary:	Allows a component to state dependencies on other plugins
Name:		trac-plugin-%{plugin}
Version:	0.1
Release:	0.6
License:	GPL
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/componentdependencyplugin?old_path=/&filename=%{plugin}-%{version}&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	3330fdc7e1f7f48037089f0a81485fa1
URL:		http://trac-hacks.org/wiki/ComponentDependencyPlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ComponentDependencyPlugin allows a Component to state a dependency on
another Component, via the IRequireComponents interface from
componentdependencies.interface.

%prep
%setup -qc
mv %{plugin}plugin/%{trac_ver}/* .

# do not autoload this
mv componentdependencies/test.py .
sed -i -e '/from test import/d' componentdependencies/__init__.py

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: no post registration needed, plugin not used directly

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/componentdependencies
%{py_sitescriptdir}/*-*.egg-info
