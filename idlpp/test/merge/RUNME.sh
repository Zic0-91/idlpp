#!/bin/sh

this_dir=$(dirname $0)

pushd $this_dir

. ../toolbox.sh

merge_version
merge_help
separator

$MERGE reference/test.c.new reference/test.c.ori
$MERGE reference/test.c.new reference/test.c.ori -o result/test.c

separator

checkResult test.c

popd