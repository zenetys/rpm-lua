# Supported targets: el9

%{!?lua_version:%global lua_version %(lua -e 'print(string.sub(_VERSION, 5))' || echo 0)}
%global luazver %(x=%{lua_version}; echo ${x/.})

%define lua_tz_version 1.0.0
%define lua_tz_xprefix lua-tz-%{lua_tz_version}

Name: lua%{luazver}z-tz
Version: %{lua_tz_version}
Release: 1%{?dist}.zenetys
Summary: Lua date and time functions with time zones
License: MIT
URL: https://github.com/anaef/lua-tz

Source0: https://github.com/anaef/lua-tz/archive/refs/tags/v%{lua_tz_version}.tar.gz#/%{lua_tz_xprefix}.tar.gz

BuildRequires: gcc
BuildRequires: lua-devel
BuildRequires: lua-rpm-macros
BuildRequires: make

%description
Lua TZ provides date and time functions with support for time zones.
The core functions have an interface similar to the standard functions
os.date and os.time, but additionally accept a time zone argument.

%prep
%setup -n %{lua_tz_xprefix}
sed -i -re 's,^(CFLAGS=),\1 $(LOCAL_CFLAGS) ,' Makefile

%build
make %{?_smp_mflags} LUA_INCDIR=%{_includedir} LOCAL_CFLAGS='-g'

%install
mkdir -p -m 755 %{buildroot}/%{lua_libdir}
make install LIBDIR=%{buildroot}/%{lua_libdir}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md doc/

%{lua_libdir}/tz.so
