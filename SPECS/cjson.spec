# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

%define lua_cjson_version 2.1.0
%define lua_cjson_xprefix lua-cjson-%{lua_cjson_version}

Name: lua%{luazver}z-cjson
Version: %{lua_cjson_version}
Release: 1%{?dist}.zenetys
Summary: Lua CJSON module
License: MIT
URL: https://github.com/mpx/lua-cjson

Source0: https://github.com/mpx/lua-cjson/archive/refs/tags/%{lua_cjson_version}.tar.gz#/%{lua_cjson_xprefix}.tar.gz

Patch100: lua-cjson-integer-support.patch

BuildRequires: gcc
BuildRequires: lua-devel
BuildRequires: lua-rpm-macros
BuildRequires: make

%description
Lua CJSON is a fast JSON encoding/parsing module for Lua

%prep
%setup -n %{lua_cjson_xprefix}
%patch100 -p1

%build
%make_build \
    CFLAGS='%{build_cflags}' \
    LDFLAGS='%{build_ldflags}'

%install
%make_install \
    LUA_CMODULE_DIR='%{lua_libdir}' \
    LUA_MODULE_DIR='%{lua_pkgdir}'

%files
%defattr(-,root,root,-)
%license LICENSE
%doc manual.txt

%{lua_libdir}/cjson.so
