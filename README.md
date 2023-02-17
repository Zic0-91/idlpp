# README

## overview

This idlpp is an idl parser written in python.

## install

```sh
python -m venv .env
. .env/bin/activate
pip install arpeggio
pip freeze > requierements.txt
```

## dependancies 

- python `arpeggio` http://textx.github.io/Arpeggio/2.0/

## How to use

Put those alias in your .bashrc file
```sh
alias idlpp='python idlpp/idlpp.py'
alias merge='python idlpp/merge.py'
```

```sh
$ idlpp -h
usage: idlpp [-h] [-d] [-v] [-o OUTPUT] [-t] file

positional arguments:
  file                  .idl file to compile

options:
  -h, --help            show this help message and exit
  -d, --debug           enable debugging
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        output file
  -t, --types           enable CPP types/component generators
```

## run unit test

```sh
idlpp/test/idlpp/RUNME.sh 
idlpp/test/merge/RUNME.sh 
```
