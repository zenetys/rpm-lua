# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

%define lua_curl_version 0.3.13
%define lua_curl_xprefix Lua-cURLv3-%{lua_curl_version}

Name: lua%{luazver}z-curl
Version: %{lua_curl_version}
Release: 1%{?dist}.zenetys
Summary: Lua binding to libcurl
License: MIT
URL: https://github.com/Lua-cURL

Source0: https://github.com/Lua-cURL/Lua-cURLv3/archive/refs/tags/v%{lua_curl_version}.tar.gz#/%{lua_curl_xprefix}.tar.gz

BuildRequires: gcc
BuildRequires: libcurl-devel
BuildRequires: lua-devel
BuildRequires: lua-rpm-macros
BuildRequires: make

%description
Lua binding to libcurl

%prep
%setup -n %{lua_curl_xprefix}

%build
%make_build \
    CFLAGS='%{build_cflags}' \
    LDFLAGS='%{build_ldflags}'

%install
%make_install \
    LUA_CMOD='%{lua_libdir}' \
    LUA_LMOD='%{lua_pkgdir}'

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md

%{lua_libdir}/lcurl.so
%{lua_pkgdir}/cURL.lua
%{lua_pkgdir}/cURL/
