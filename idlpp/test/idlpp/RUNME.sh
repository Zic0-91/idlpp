#!/bin/sh

this_dir=$(dirname $0)

pushd $this_dir

. ../toolbox.sh

idlpp_version
idlpp_help
separator

function runTest
{
	local idl=$1
	local name=$(basename $idl .idl)
	
	$IDPPP -t $idl -o result/$name.hpp	
	
	echo -n "Test $name "
	checkResult "$name.hpp"
}

for idl in $(ls -1 *.idl); do
	runTest $idl
	echo "---"
done

popd
