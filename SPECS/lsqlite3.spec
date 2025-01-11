# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

%define lua_lsqlite3_version 0.9.6
%define lua_lsqlite3_xprefix lsqlite3-%{lua_lsqlite3_version}

Name: lua%{luazver}z-lsqlite3
Version: %{lua_lsqlite3_version}
Release: 1%{?dist}.zenetys
Summary: Lua binding to the SQLite3 database library
License: MIT
URL: http://lua.sqlite.org

Source0: http://lua.sqlite.org/index.cgi/tarball/lsqlite3-%{lua_lsqlite3_version}.tar.gz?uuid=v%{lua_lsqlite3_version}#/%{lua_lsqlite3_xprefix}.tar.gz

BuildRequires: gcc
BuildRequires: lua-devel
BuildRequires: lua-rpm-macros
BuildRequires: make
BuildRequires: sqlite-devel

%description
LuaSQLite 3 is a thin wrapper around the public domain SQLite3
database engine.

%prep
%setup -n %{lua_lsqlite3_xprefix}

%build
gcc -fPIC -I%{_includedir} %{build_cflags} -c lsqlite3.c -o lsqlite3.o -DLSQLITE_VERSION='"%{lua_lsqlite3_version}"'
gcc -shared -o lsqlite3.so lsqlite3.o %{build_ldflags} -lsqlite3

%install
install -d -m 0755 %{buildroot}/%{lua_libdir}
install -D -m 0755 lsqlite3.so %{buildroot}/%{lua_libdir}/

%files
%defattr(-,root,root,-)
%doc README examples/

%{lua_libdir}/lsqlite3.so
