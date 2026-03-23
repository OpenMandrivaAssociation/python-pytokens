%define module pytokens
%bcond tests 1

Name:		python-pytokens
Version:	0.4.1
Release:	1
Summary:	A Fast, spec compliant Python 3.14+ tokenizer that runs on older Pythons
License:	MIT License
Group:		Development/Python
URL:		https://github.com/tusharsadhwani/pytokens
Source0:	%{URL}/archive/%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(build)
BuildRequires:	python%{pyver}dist(installer)
BuildRequires:	python%{pyver}dist(mypy)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
A Fast, spec compliant Python 3.14+ tokenizer that runs on older Pythons.

%prep -a
# Remove bundled egg-info
rm -rf src/%{module}.egg-info
# We dont need to run upstream coverage tests
sed -i 's/--cov --cov-report=term-missing//g' pyproject.toml

%build -p
# disable building with mypyc librt
export PYTOKENS_USE_MYPYC=0

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest
%endif

%files
%doc README.md
%license LICENSE
# only produced when building with mypyc
#%%{python_sitearch}/*__mypyc.cpython-*.so
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
