#!/usr/bin/env bash
#title          :pypi_packager.sh
#description    :This script will build a source distribution and wheel
#author         :https://github.com/mbourqui
#date           :20170419
#version        :1.0
#usage		    :bash pypi_packager.sh
#notes          :In case of submission to PyPI, ~/.pypirc must be set accordingly
#==============================================================================

# This script generates a package and submits it to the Python Package Index
PROGRAM_NAME=$(basename "$0")
VERSION=1.0
PROJECT_NAME=$(basename $(pwd))
PACKAGE_NAME=${PROJECT_NAME//-/_}  # Replace all - with _

usage() {
echo "Usage: $PROGRAM_NAME [-h,--help,-v,--version] [-s,--submit|-t,--test]

Script to build source distribution and wheel for a python package.

Options:
    -s, --submit    upload the package to PyPI. Requires ~/.pypirc to be set.
    -t, --test      upload the package to TestPyPI. Requires ~/.pypirc to be set.

    -h, --help      display this help and exit
    -v, --version   output version information and exit"
}

# Parse arguments
TEMP=$(getopt -n $PROGRAM_NAME -o sthv --long submit,test,help,version -- "$@")

if [ $? != 0 ] ; then usage >&2 ; exit 1 ; fi

eval set -- "$TEMP"
while true; do
    case $1 in
        -s|--submit)
            SUBMIT=1; shift; continue
        ;;
        -t|--test)
            TEST=1; shift; continue
        ;;
        -h|--help)
            usage
            exit
        ;;
        -v|--version)
            echo $VERSION
            exit
        ;;
        --)
            # no more arguments to parse
            shift
            break
        ;;
        *)
            break
        ;;
    esac
done
eval set -- "$@"

if [ -n "$SUBMIT" -a -n "$TEST" ]; then
    echo "ERROR: Incompatible options"
    echo
    usage
    exit 1
fi

# Clear previous compilations to prevent potential issues and limit disk space usage
rm -f README.rst
rm -rf dist/ build/ ${PACKAGE_NAME}.egg-info/

# Generate doc as restructured text for nice PyPI rendering
pandoc --from=markdown --to=rst --output=README.rst README.md

# Source distribution
python setup.py sdist

# Wheel
python setup.py bdist_wheel

if [ -n "$SUBMIT" ]; then
    # Upload to PyPI
    twine register dist/${PACKAGE_NAME}-*.whl
    twine upload dist/*
elif [ -n "$TEST" ]; then
    # Upload to TestPyPI
    python setup.py register -r https://testpypi.python.org/pypi
    twine upload dist/* -r testpypi
    pip install -i https://testpypi.python.org/pypi $PACKAGE_NAME
fi
