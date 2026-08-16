#!/bin/sh
set -e
# Regenerate the ethernet vendor table from the current IEEE registry.
#
# The IEEE serves oui.csv rows in a random order, so the raw file hashes
# differently on every fetch and cannot be pinned as a Source. massagevendor
# sorts its output, so the converted table is stable and an unchanged registry
# regenerates byte for byte.

specfile=arpwatch.spec

# Work in package dir
dir=$(dirname "$0")
cd "$dir"

version=$(awk '/^Version:/{print $2}' $specfile)
tarball=arpwatch-$version.tar.gz
[ -f "$tarball" ] || builder -ncs -g $specfile

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# massagevendor.py.in is a configure template, so substitute what it needs
# rather than requiring an installed arpwatch
tar xzf "$tarball" -C "$tmp" arpwatch-$version/massagevendor.py.in
sed -e 's|@PYTHON@|/usr/bin/python3|' -e 's|@ZEROPAD@|0|' \
	"$tmp/arpwatch-$version/massagevendor.py.in" > "$tmp/massagevendor.py"

curl -sSf https://standards-oui.ieee.org/oui/oui.csv \
	| /usr/bin/python3 "$tmp/massagevendor.py" > "$tmp/ethercodes.dat"

# a truncated download or an error page must not become the shipped table
entries=$(wc -l < "$tmp/ethercodes.dat")
if [ "$entries" -lt 30000 ]; then
	echo >&2 "$0: only $entries entries, refusing to publish"
	exit 1
fi

ouidate=$(date -u +%Y%m%d)
out=ethercodes-$ouidate.dat.xz
xz -9 < "$tmp/ethercodes.dat" > "$out"
echo "Updating $specfile: ouidate: $ouidate ($entries entries)"

sed -i -re "s/^[#%](define[ \t]+ouidate[ \t]+)[0-9]+\$/%\1$ouidate/" $specfile

../md5 $specfile
../dropin "$out"
