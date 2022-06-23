%global major_version 5.3
%global minor_version 6

%define lua_cjson_version 2.1.0
%define lua_cjson_xprefix lua-cjson-%{lua_cjson_version}

%define lua_curl_version 0.3.13
%define lua_curl_xprefix Lua-cURLv3-%{lua_curl_version}
%define lua_curl_makeopts \\\
    LUA_INC=../src/ \\\
    LIBDIR=../src/ \\\
    LUA_CMOD=/opt/lua-%{major_version}/lib/lua \\\
    LUA_LMOD=/opt/lua-%{major_version}/share/lua

%define lua_filesystem_version 1_8_0
%define lua_filesystem_xprefix luafilesystem-%{lua_filesystem_version}

%define lua_socket_version 3.0.0
%define lua_socket_xprefix luasocket-%{lua_socket_version}
%define lua_socket_makeopts \\\
    PLAT=linux \\\
    LUAV=%{major_version} \\\
    LUAINC_linux=../../src \\\
    LUAPREFIX_linux=/opt/lua-%{major_version} \\\
    LDIR_linux=share/lua \\\
    CDIR_linux=lib/lua \\\
    SOCKET_V=%{lua_socket_version}

%define lua_posix_version 35.1
%define lua_posix_xprefix luaposix-%{lua_posix_version}

Name: lua53z
Summary: Powerful light-weight programming language
Version: %{major_version}.%{minor_version}
Release: 2%{?dist}.zenetys
License: MIT
Group: Development/Languages
URL: http://www.lua.org/

Source0: https://www.lua.org/ftp/lua-%{version}.tar.gz
Source1000: https://github.com/mpx/lua-cjson/archive/refs/tags/%{lua_cjson_version}.tar.gz#/%{lua_cjson_xprefix}.tar.gz
Source1100: https://github.com/Lua-cURL/Lua-cURLv3/archive/refs/tags/v%{lua_curl_version}.tar.gz#/%{lua_curl_xprefix}.tar.gz
Source1200: https://github.com/keplerproject/luafilesystem/archive/refs/tags/v%{lua_filesystem_version}.tar.gz#/%{lua_filesystem_xprefix}.tar.gz
Source1300: https://github.com/lunarmodules/luasocket/archive/refs/tags/v%{lua_socket_version}.tar.gz#/%{lua_socket_xprefix}.tar.gz
Source1400: https://github.com/luaposix/luaposix/archive/refs/tags/v%{lua_posix_version}.tar.gz#/%{lua_posix_xprefix}.tar.gz

Patch0: lua-5.3.6-lua-path.patch
Patch1000: lua-cjson-integer-support.patch
Patch1001: lua-cjson-local-cflags.patch

BuildRequires: libcurl-devel
BuildRequires: ncurses-devel
BuildRequires: readline-devel

%description
Lua %{major_version} packaged to be non-intrusive so that is does not replace
the standard package provided by the distribution. This package
installs its files in /opt/lua-5.3 and provides the following Lua
modules:
- lua-cjson (https://github.com/mpx/lua-cjson)
- Lua-cURLv3 (https://github.com/Lua-cURL/Lua-cURLv3)
- luafilesystem (https://github.com/keplerproject/luafilesystem)
- luasocket (https://github.com/lunarmodules/luasocket)
- luaposix (https://github.com/luaposix/luaposix)

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

# luasocket
%setup -n lua-%{version} -T -D -a 1300
sed -i -re 's,(LUASOCKET_VERSION\s+"[^[:space:]]+\s+).*,\1%{lua_socket_version}",' \
    %{lua_socket_xprefix}/src/luasocket.h

# luaposix
%setup -n lua-%{version} -T -D -a 1400

%build
# lua
make linux MYCFLAGS='-g -fPIC'

# Some modules are built using luke, which is a lua script, but the
# standard lua binary of the distro may not be present (eg: el8).
# We could add a BuildRequire on the distro lua, but since we've just
# built it, let's use this one.
export PATH="$PWD/src:$PATH"

# lua-cjson
cd %{lua_cjson_xprefix}
make LUA_INCLUDE_DIR=../src/ LOCAL_CFLAGS='-g'
cd ..

# lua-curl
cd %{lua_curl_xprefix}
make %{lua_curl_makeopts}
cd ..

# luafilesystem
cd %{lua_filesystem_xprefix}
make LUA_INC='-I../src -g'
cd ..

# luasocket
cd %{lua_socket_xprefix}
make %{lua_socket_makeopts} MYCFLAGS='-g'
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke LUA_INCDIR=../src CFLAGS='-g'
cd ..

%install
# Make sure we have a lua binary in $PATH (see comments in build section).
export PATH="$PWD/src:$PATH"

# lua
make install INSTALL_TOP=%{buildroot}/opt/lua-%{major_version}
mkdir -p %{buildroot}/opt/lua-%{major_version}/lib/lua
mkdir -p %{buildroot}/opt/lua-%{major_version}/share/lua

# lua-cjson
cd %{lua_cjson_xprefix}
make install \
    PREFIX=%{buildroot}/opt/lua-%{major_version} \
    LUA_CMODULE_DIR=%{buildroot}/opt/lua-%{major_version}/lib/lua
cd ..

# lua-curl
cd %{lua_curl_xprefix}
make install DESTDIR=%{buildroot} %{lua_curl_makeopts}
cd ..

# luafilesystem
cd %{lua_filesystem_xprefix}
make install \
    DESTDIR=%{buildroot} \
    LUA_LIBDIR=/opt/lua-%{major_version}/lib/lua
cd ..

# luasocket
cd %{lua_socket_xprefix}
make install %{lua_socket_makeopts} DESTDIR=%{buildroot}
cd ..

# luaposix
cd %{lua_posix_xprefix}
./build-aux/luke install \
    PREFIX=%{buildroot}/opt/lua-%{major_version} \
    INST_LUADIR=%{buildroot}/opt/lua-%{major_version}/share/lua \
    INST_LIBDIR=%{buildroot}/opt/lua-%{major_version}/lib/lua
cd ..

%files
%defattr(-,root,root,-)
%dir /opt/lua-%{major_version}
%dir /opt/lua-%{major_version}/bin
/opt/lua-%{major_version}/bin/*
%dir /opt/lua-%{major_version}/man
/opt/lua-%{major_version}/man/*
%dir /opt/lua-%{major_version}/lib
%dir /opt/lua-%{major_version}/lib/lua
/opt/lua-%{major_version}/lib/lua/*
%dir /opt/lua-%{major_version}/share
/opt/lua-%{major_version}/share/*

%files devel
/opt/lua-%{major_version}/lib/liblua.a
%dir /opt/lua-%{major_version}/include
/opt/lua-%{major_version}/include/*
