| Package&nbsp;name | Supported&nbsp;targets |
| :--- | :--- |
| <nobr>lua54z-cjson</nobr> | <nobr>el9, el10</nobr> |
| <nobr>lua54z-curl</nobr> | <nobr>el9, el10</nobr> |
| <nobr>lua54z-print_r</nobr> | <nobr>el9, el10</nobr> |
| <nobr>lua54z-snmp</nobr> | <nobr>el9, el10</nobr> |
<br/>


## Build:

The package can be built easily using the script rpmbuild-docker provided
in this repository. In order to use this script, _**a functional Docker
environment is needed**_, with ability to pull Rocky Linux images from
internet if not already downloaded.

```
## run from this git base tree
for i in SPECS/*.spec; do ./rpmbuild-docker -d el9 "$i"; done
for i in SPECS/*.spec; do ./rpmbuild-docker -d el10 "$i"; done
```

## Prebuilt packages:

Builds of these packages are available on ZENETYS yum repositories:<br/>
https://packages.zenetys.com/latest/redhat/
