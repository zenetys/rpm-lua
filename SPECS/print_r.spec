# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

Name: lua%{luazver}z-print_r
Version: 1.0.0
Release: 1%{?dist}.zenetys
Summary: Lua print_r function
License: MIT
URL: https://www.arpalert.org/haproxy-scripts.html

# Original file at https://www.arpalert.org/src/lua/print_r.lua
Source0: print_r.lua

BuildArch: noarch

BuildRequires: lua-rpm-macros

%description
Lua function that tries to copy the famous PHP's "print_r".

%install
install -d -m 755 %{buildroot}/%{lua_pkgdir}
install -p -m 644 %{SOURCE0} %{buildroot}/%{lua_pkgdir}/

%files
%defattr(-,root,root,-)
%{lua_pkgdir}/print_r.lua
