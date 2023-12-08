%global lua_major_version 5.3
%global lua_minor_version 6

%define libssl_version 1_1_1w
%define libssl_xprefix openssl-OpenSSL_%{libssl_version}

%define lua_cjson_version 2.1.0
%define lua_cjson_xprefix lua-cjson-%{lua_cjson_version}

%define lua_curl_version 0.3.13
%define lua_curl_xprefix Lua-cURLv3-%{lua_curl_version}
%define lua_curl_makeopts \\\
    LUA_INC=../src/ \\\
    LIBDIR=../src/ \\\
    LUA_CMOD=/opt/lua-%{lua_major_version}/lib/lua \\\
    LUA_LMOD=/opt/lua-%{lua_major_version}/share/lua

%define lua_filesystem_version 1_8_0
%define lua_filesystem_xprefix luafilesystem-%{lua_filesystem_version}

%define lua_socket_version 3.1.0
%define lua_socket_xprefix luasocket-%{lua_socket_version}
%define lua_socket_makeopts \\\
    PLAT=linux \\\
    LUAV=%{lua_major_version} \\\
    LUAINC_linux=../../src \\\
    LUAPREFIX_linux=/opt/lua-%{lua_major_version} \\\
    LDIR_linux=share/lua \\\
    CDIR_linux=lib/lua \\\
    SOCKET_V=%{lua_socket_version}

%define lua_posix_version 36.2.1
%define lua_posix_xprefix luaposix-%{lua_posix_version}

%define lua_ossl_version 20220711
%define lua_ossl_xprefix luaossl-rel-%{lua_ossl_version}

# luasnmp version 1.0.8
# luasnmp does not provide release tarballs not version tags
%define lua_snmp_version a369ad9a1271d9c6327d0c3548b08d63c250ab74
%define lua_snmp_xprefix luasnmp-%{lua_snmp_version}

Name: lua53z
Summary: Powerful light-weight programming language
Version: %{lua_major_version}.%{lua_minor_version}
Release: 16%{?dist}.zenetys
License: MIT
Group: Development/Languages
URL: http://www.lua.org/

Source0: https://www.lua.org/ftp/lua-%{version}.tar.gz
Source100: https://github.com/openssl/openssl/archive/refs/tags/%(x=%{libssl_xprefix}; echo ${x#*-}).tar.gz
Source1000: https://github.com/mpx/lua-cjson/archive/refs/tags/%{lua_cjson_version}.tar.gz#/%{lua_cjson_xprefix}.tar.gz
Source1001: lua-json-compat.lua
Source1100: https://github.com/Lua-cURL/Lua-cURLv3/archive/refs/tags/v%{lua_curl_version}.tar.gz#/%{lua_curl_xprefix}.tar.gz
Source1200: https://github.com/keplerproject/luafilesystem/archive/refs/tags/v%{lua_filesystem_version}.tar.gz#/%{lua_filesystem_xprefix}.tar.gz
Source1300: https://github.com/lunarmodules/luasocket/archive/refs/tags/v%{lua_socket_version}.tar.gz#/%{lua_socket_xprefix}.tar.gz
Source1400: https://github.com/luaposix/luaposix/archive/refs/tags/v%{lua_posix_version}.tar.gz#/%{lua_posix_xprefix}.tar.gz
Source1500: https://github.com/wahern/luaossl/archive/refs/tags/rel-%{lua_ossl_version}.tar.gz#/%{lua_ossl_xprefix}.tar.gz
Source1600: http://www.arpalert.org/src/lua/print_r.lua
Source1700: https://github.com/hleuwer/luasnmp/archive/%{lua_snmp_version}.tar.gz#/%{lua_snmp_xprefix}.tar.gz

Patch0: lua-5.3.6-lua-path.patch
Patch1000: lua-cjson-integer-support.patch
Patch1001: lua-cjson-local-cflags.patch
Patch1700: luasnmp-no-des.patch

BuildRequires: libcurl-devel
BuildRequires: ncurses-devel
BuildRequires: net-snmp-devel
BuildRequires: perl-Data-Dumper
%if 0%{?rhel} >= 9
BuildRequires: perl-FindBin
%endif
BuildRequires: perl-IPC-Cmd
BuildRequires: readline-devel

%description
Lua %{lua_major_version} packaged to be non-intrusive so that is does not replace
the standard package provided by the distribution. This package
installs its files in /opt/lua-5.3 and provides the following Lua
modules:
- lua-cjson (https://github.com/mpx/lua-cjson)
- json.lua, incomplete lua-json compatibility layer using lua-cjson
- Lua-cURLv3 (https://github.com/Lua-cURL/Lua-cURLv3)
- luafilesystem (https://github.com/keplerproject/luafilesystem)
- luasocket (https://github.com/lunarmodules/luasocket)
- luaposix (https://github.com/luaposix/luaposix)
- luaossl (https://github.com/wahern/luaossl), static link with %{libssl_xprefix}
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

# libssl
%setup -n lua-%{version} -T -D -a 100

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

# luasocket
%setup -n lua-%{version} -T -D -a 1300
sed -i -re 's,(LUASOCKET_VERSION\s+"[^[:space:]]+\s+).*,\1%{lua_socket_version}",' \
    %{lua_socket_xprefix}/src/luasocket.h

# luaposix
%setup -n lua-%{version} -T -D -a 1400

# luaossl
%setup -n lua-%{version} -T -D -a 1500

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
# standard lua binary of the distro may not be present (eg: el8).
# We could add a BuildRequire on the distro lua, but since we've just
# built it, let's use this one.
export PATH="$PWD/src:$PATH"

# libssl
cd %{libssl_xprefix}
./config no-shared
make %{?_smp_mflags}
ssl_inc="$PWD/include"
ssl_lib="$PWD"
cd ..
[[ -e $ssl_inc/openssl/ssl.h ]] || exit 1
[[ -e $ssl_lib/libssl.a ]] || exit 1
[[ -e $ssl_lib/libcrypto.a ]] || exit 1

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

# luasocket
cd %{lua_socket_xprefix}
make %{?_smp_mflags} %{lua_socket_makeopts} MYCFLAGS='-g'
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke LUA_INCDIR=../src CFLAGS='-g'
cd ..

# luaossl
cd %{lua_ossl_xprefix}
make %{?_smp_mflags} \
    LUA_APIS='%{lua_major_version}' \
    CFLAGS="-g -I$ssl_inc -I$lua_inc" \
    LDFLAGS="-L$ssl_lib"
cd ..

# luasnmp
cd %{lua_snmp_xprefix}
make %{?_smp_mflags} LUAINC="$lua_inc" LOCAL_CFLAGS='-g'
cd ..

%install
# Make sure we have a lua binary in $PATH (see comments in build section).
export PATH="$PWD/src:$PATH"

# lua
make install INSTALL_TOP=%{buildroot}/opt/lua-%{lua_major_version}
mkdir -p %{buildroot}/opt/lua-%{lua_major_version}/lib/lua
mkdir -p %{buildroot}/opt/lua-%{lua_major_version}/share/lua

# lua-cjson
cd %{lua_cjson_xprefix}
make install \
    PREFIX=%{buildroot}/opt/lua-%{lua_major_version} \
    LUA_CMODULE_DIR=%{buildroot}/opt/lua-%{lua_major_version}/lib/lua
cd ..
install -D -p -m 644 %{SOURCE1001} \
    %{buildroot}/opt/lua-%{lua_major_version}/share/lua/json.lua

# lua-curl
cd %{lua_curl_xprefix}
make install DESTDIR=%{buildroot} %{lua_curl_makeopts}
cd ..

# luafilesystem
cd %{lua_filesystem_xprefix}
make install \
    DESTDIR=%{buildroot} \
    LUA_LIBDIR=/opt/lua-%{lua_major_version}/lib/lua
cd ..

# luasocket
cd %{lua_socket_xprefix}
make install %{lua_socket_makeopts} DESTDIR=%{buildroot}
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke install \
    PREFIX=%{buildroot}/opt/lua-%{lua_major_version} \
    INST_LUADIR=%{buildroot}/opt/lua-%{lua_major_version}/share/lua \
    INST_LIBDIR=%{buildroot}/opt/lua-%{lua_major_version}/lib/lua
cd ..

# luaossl
cd %{lua_ossl_xprefix}
vshort=$(echo '%{lua_major_version}' |tr -d .)
make install%{lua_major_version} \
    prefix=%{buildroot}/opt/lua-%{lua_major_version} \
    lua${vshort}path=%{buildroot}/opt/lua-%{lua_major_version}/share/lua \
    lua${vshort}cpath=%{buildroot}/opt/lua-%{lua_major_version}/lib/lua
cd ..
%if 0%{?rhel} == 7
# On el7, find-debuginfo.sh from RPM macro __debug_install_post fails
# when extracting debug info from luaossl's _openssl.so because of
# /usr/lib/rpm/debugedit failing with message "Failed to write file:
# invalid section alignment". This trick allows to skip processing
# the file while still creating a debuginfo package.
eu-strip --remove-comment %{buildroot}/opt/lua-5.3/lib/lua/_openssl.so
%endif

# print_r
install -D -p -m 644 %{SOURCE1600} \
    %{buildroot}/opt/lua-%{lua_major_version}/share/lua/

# luasnmp
cd %{lua_snmp_xprefix}
make install \
    INSTALL_SHARE=%{buildroot}/opt/lua-%{lua_major_version}/share/lua \
    INSTALL_LIB=%{buildroot}/opt/lua-%{lua_major_version}/lib/lua
cd ..
%if 0%{?rhel} == 7
# el7 find-debuginfo.sh issue (same as above)
eu-strip --remove-comment %{buildroot}/opt/lua-5.3/lib/lua/snmp/core.so
%endif

%files
%defattr(-,root,root,-)
%dir /opt/lua-%{lua_major_version}
%dir /opt/lua-%{lua_major_version}/bin
/opt/lua-%{lua_major_version}/bin/*
%dir /opt/lua-%{lua_major_version}/man
/opt/lua-%{lua_major_version}/man/*
%dir /opt/lua-%{lua_major_version}/lib
%dir /opt/lua-%{lua_major_version}/lib/lua
/opt/lua-%{lua_major_version}/lib/lua/*
%dir /opt/lua-%{lua_major_version}/share
%dir /opt/lua-%{lua_major_version}/share/lua
/opt/lua-%{lua_major_version}/share/lua/*

%files devel
/opt/lua-%{lua_major_version}/lib/liblua.a
%dir /opt/lua-%{lua_major_version}/include
/opt/lua-%{lua_major_version}/include/*
