# Supported targets: el9

%global lua_major_version 5.4
%global lua_minor_version 7

%define lua_cjson_version 2.1.0
%define lua_cjson_xprefix lua-cjson-%{lua_cjson_version}

%define lua_curl_version 0.3.13
%define lua_curl_xprefix Lua-cURLv3-%{lua_curl_version}
%define lua_curl_makeopts \\\
    LUA_INC=../src/ \\\
    LIBDIR=../src/ \\\
    LUA_CMOD=/opt/%{name}/lib/lua \\\
    LUA_LMOD=/opt/%{name}/share/lua

%define lua_filesystem_version 1_8_0
%define lua_filesystem_xprefix luafilesystem-%{lua_filesystem_version}

%define lua_posix_version 36.2.1
%define lua_posix_xprefix luaposix-%{lua_posix_version}

# luasnmp version 1.0.8
# luasnmp does not provide release tarballs not version tags
%define lua_snmp_version a369ad9a1271d9c6327d0c3548b08d63c250ab74
%define lua_snmp_xprefix luasnmp-%{lua_snmp_version}

Name: lua54z
Summary: Powerful light-weight programming language
Version: %{lua_major_version}.%{lua_minor_version}
Release: 1%{?dist}.zenetys
License: MIT
Group: Development/Languages
URL: http://www.lua.org/

Source0: https://www.lua.org/ftp/lua-%{version}.tar.gz
Source1000: https://github.com/mpx/lua-cjson/archive/refs/tags/%{lua_cjson_version}.tar.gz#/%{lua_cjson_xprefix}.tar.gz
Source1001: lua-json-compat.lua
Source1100: https://github.com/Lua-cURL/Lua-cURLv3/archive/refs/tags/v%{lua_curl_version}.tar.gz#/%{lua_curl_xprefix}.tar.gz
Source1200: https://github.com/keplerproject/luafilesystem/archive/refs/tags/v%{lua_filesystem_version}.tar.gz#/%{lua_filesystem_xprefix}.tar.gz
Source1400: https://github.com/luaposix/luaposix/archive/refs/tags/v%{lua_posix_version}.tar.gz#/%{lua_posix_xprefix}.tar.gz
Source1600: http://www.arpalert.org/src/lua/print_r.lua
Source1700: https://github.com/hleuwer/luasnmp/archive/%{lua_snmp_version}.tar.gz#/%{lua_snmp_xprefix}.tar.gz

Patch0: lua-path.patch
Patch1000: lua-cjson-integer-support.patch
Patch1001: lua-cjson-local-cflags.patch
Patch1700: luasnmp-no-des.patch

BuildRequires: libcurl-devel
BuildRequires: ncurses-devel
BuildRequires: net-snmp-devel
BuildRequires: readline-devel

%description
Lua %{lua_major_version} packaged to be non-intrusive so that is does not replace
the standard package provided by the distribution. This package
installs its files in /opt/%{name} and provides the following Lua
modules:
- lua-cjson (https://github.com/mpx/lua-cjson)
- json.lua, incomplete lua-json compatibility layer using lua-cjson
- Lua-cURLv3 (https://github.com/Lua-cURL/Lua-cURLv3)
- luafilesystem (https://github.com/keplerproject/luafilesystem)
- luaposix (https://github.com/luaposix/luaposix)
- print_r.lua (http://www.arpalert.org/haproxy-scripts.html)
- luasnmp (https://github.com/hleuwer/luasnmp)

%package devel
Summary: Development files for %{name}
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
# lua
%setup -n lua-%{version}
%patch0 -p1

# lua-cjson
%setup -n lua-%{version} -T -D -a 1000
cd %{lua_cjson_xprefix}
%patch1000 -p1
%patch1001 -p1
cd ..

# lua-curl
%setup -n lua-%{version} -T -D -a 1100

# luafilesystem
%setup -n lua-%{version} -T -D -a 1200

# luaposix
%setup -n lua-%{version} -T -D -a 1400

# luasnmp
%setup -n lua-%{version} -T -D -a 1700
cd %{lua_snmp_xprefix}
%patch1700 -p1
sed -i -re 's,^(DEF =),\1 $(LOCAL_CFLAGS),' config
cd ..

%build
# lua
make linux %{?_smp_mflags} MYCFLAGS='-g -fPIC'
lua_inc="$PWD/src"
[[ -e $lua_inc/lua.h ]] || exit 1

# Some modules are built using luke, which is a lua script, but the
# standard lua binary of the distro may not be present.
# We could add a BuildRequire on the distro lua, but since we've just
# built it, let's use this one.
export PATH="$PWD/src:$PATH"

# lua-cjson
cd %{lua_cjson_xprefix}
make %{?_smp_mflags} LUA_INCLUDE_DIR=../src/ LOCAL_CFLAGS='-g'
cd ..

# lua-curl
cd %{lua_curl_xprefix}
make %{?_smp_mflags} %{lua_curl_makeopts}
cd ..

# luafilesystem
cd %{lua_filesystem_xprefix}
make %{?_smp_mflags} LUA_INC='-I../src -g'
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke LUA_INCDIR=../src CFLAGS='-g'
cd ..

# luasnmp
cd %{lua_snmp_xprefix}
make %{?_smp_mflags} LUAINC="$lua_inc" LOCAL_CFLAGS='-g'
cd ..

%install
# Make sure we have a lua binary in $PATH (see comments in build section).
export PATH="$PWD/src:$PATH"

# lua
make install \
    INSTALL_TOP='%{buildroot}/opt/%{name}' \
    INSTALL_LMOD='$(INSTALL_TOP)/share/lua' \
    INSTALL_CMOD='$(INSTALL_TOP)/lib/lua'

# lua-cjson
cd %{lua_cjson_xprefix}
make install \
    PREFIX=%{buildroot}/opt/%{name} \
    LUA_CMODULE_DIR=%{buildroot}/opt/%{name}/lib/lua
cd ..
install -D -p -m 644 %{SOURCE1001} \
    %{buildroot}/opt/%{name}/share/lua/json.lua

# lua-curl
cd %{lua_curl_xprefix}
make install DESTDIR=%{buildroot} %{lua_curl_makeopts}
cd ..

# luafilesystem
cd %{lua_filesystem_xprefix}
make install \
    DESTDIR=%{buildroot} \
    LUA_LIBDIR=/opt/%{name}/lib/lua
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke install \
    PREFIX=%{buildroot}/opt/%{name} \
    INST_LUADIR=%{buildroot}/opt/%{name}/share/lua \
    INST_LIBDIR=%{buildroot}/opt/%{name}/lib/lua
cd ..

# print_r
install -D -p -m 644 %{SOURCE1600} \
    %{buildroot}/opt/%{name}/share/lua/

# luasnmp
cd %{lua_snmp_xprefix}
make install \
    INSTALL_SHARE=%{buildroot}/opt/%{name}/share/lua \
    INSTALL_LIB=%{buildroot}/opt/%{name}/lib/lua
cd ..

%files
%defattr(-,root,root,-)
%dir /opt/%{name}
%dir /opt/%{name}/bin
/opt/%{name}/bin/*
%dir /opt/%{name}/man
/opt/%{name}/man/*
%dir /opt/%{name}/lib
%dir /opt/%{name}/lib/lua
/opt/%{name}/lib/lua/*
%dir /opt/%{name}/share
%dir /opt/%{name}/share/lua
/opt/%{name}/share/lua/*

%files devel
/opt/%{name}/lib/liblua.a
%dir /opt/%{name}/include
/opt/%{name}/include/*
