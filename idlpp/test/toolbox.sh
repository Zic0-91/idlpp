#!/bin/sh

this_dir=$(dirname ${BASH_SOURCE[0]})

echo $this_dir

IDPPP="python $this_dir/../idlpp.py"
MERGE="python $this_dir/../merge.py"

function idlpp_version
{
	eval $IDPPP -v
}

function idlpp_help
{
	eval $IDPPP -h
}

function merge_version
{
	eval $IDPPP -v
}

function merge_help
{
	eval $MERGE -h
}


function separator
{
	echo "---"
}

function checkResult
{
	local name=$1
	
	local res=$(diff "result/$name" "reference/$name")
	if [ "$res" == "" ]; then
		echo "ok"
	else
		echo "KO"
	fi
}


