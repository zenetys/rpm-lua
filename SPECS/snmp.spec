# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

%define lua_snmp_version 1.1.1-1
%define lua_snmp_xprefix luasnmp-%{lua_snmp_version}
%define lua_snmp_rpm_version %(x=%{lua_snmp_version}; echo ${x%%-*})
%define lua_snmp_rpm_release %(x=%{lua_snmp_version}; echo ${x##*-})

Name: lua%{luazver}z-snmp
Version: %{lua_snmp_rpm_version}
Release: %{lua_snmp_rpm_release}.2%{?dist}.zenetys
Summary: Lua binding to net-snmp library
License: MIT
URL: https://github.com/hleuwer/luasnmp

Source0: https://github.com/hleuwer/luasnmp/archive/%{lua_snmp_version}.tar.gz#/%{lua_snmp_xprefix}.tar.gz

Patch100: luasnmp-local-flags.patch
Patch101: luasnmp-env-home.patch

BuildRequires: gcc
BuildRequires: lua-devel
BuildRequires: lua-rpm-macros
BuildRequires: make
BuildRequires: net-snmp-devel

%description
LuaSNMP is a binding to the netsnmp library.

%prep
%setup -n %{lua_snmp_xprefix}
%patch100 -p1
%patch101 -p1

%build
%make_build \
    LOCAL_CFLAGS='%{build_cflags}' \
    LOCAL_LDFLAGS='%{build_ldflags}' \
    LUAINC='%{_includedir}'

%install
%make_install \
    INSTALL_LIB='%{buildroot}/%{lua_libdir}' \
    INSTALL_SHARE='%{buildroot}/%{lua_pkgdir}'

%files
%defattr(-,root,root,-)
%license LICENSE
%doc FAQ README

%{lua_libdir}/snmp
%{lua_pkgdir}/snmp.lua
%{lua_pkgdir}/trapd.lua
