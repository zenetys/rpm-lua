| Package&nbsp;name | Supported&nbsp;targets | Includes |
| :--- | :--- | :--- |
| lua53z | <nobr>el8, el9</nobr> | <nobr>lua-cjson, json.lua, Lua-cURLv3, luafilesystem, </nobr><br/><nobr>luasocket, luaposix, luaossl, print_r.lua, luasnmp</nobr> |
<br/>


## Build:

The package can be built easily using the script rpmbuild-docker provided in this repository. In order to use this script, _**a functional Docker environment is needed**_, with ability to pull Rocky Linux (el8, el9) images from internet if not already downloaded.

```
## run from this git base tree
$ ./rpmbuild-docker -d el8
$ ./rpmbuild-docker -d el9
```

## Prebuilt packages:

Builds of these packages are available on ZENETYS yum repositories:<br/>
https://packages.zenetys.com/latest/redhat/
