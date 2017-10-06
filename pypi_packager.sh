#!/usr/bin/env bash
#    This script generates a package and submits it to the Python Package Index
#    Copyright (C) 2017  Marc Bourqui
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
#title          :pypi_packager.sh
#description    :This script will build a source distribution and wheel. It
#                converts a README.md to README.rst for nice rendering on PyPI.
#author         :https://github.com/mbourqui
#licence        :GNU GPL-3.0
#date           :20170526
#version        :1.1
#usage          :bash pypi_packager.sh
#requires       :pandoc
#notes          :In case of submission to PyPI, ~/.pypirc must be set
#                accordingly
#==============================================================================

PROGRAM_NAME=$(basename "$0")
VERSION=1.1
PROJECT_NAME=$(basename $(pwd))
PACKAGE_NAME=${PROJECT_NAME//-/_}  # Replace all - with _

usage() {
echo "$PROGRAM_NAME  Copyright (C) 2017  Marc Bourqui
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain
conditions, see <http://www.gnu.org/licenses/> for details.

Script to build source distribution and wheel for a python package. Also
converts a README.md to README.rst thanks to pandoc for nice rendering on PyPI.

Usage: $PROGRAM_NAME [-h,--help,-v,--version] [-s,--submit|-t,--test]

Options:
    -s, --submit    upload the package to PyPI. Requires ~/.pypirc to be set.
    -t, --test      upload the package to TestPyPI. Requires ~/.pypirc to be
                    set.

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

# Clear previous compilations to prevent potential issues and limit disk space
# usage
rm -f README.rst
rm -rf dist/ build/ ${PACKAGE_NAME}.egg-info/

# Generate doc as restructured text for nice PyPI rendering
pandoc --from=markdown --to=rst --output=README.rst README.md

# Source distribution
python setup.py sdist

# Wheel
python setup.py bdist_wheel

if [ -n "$SUBMIT" ]; then
    # Pre-registration to PyPI is no longer required or supported, upload
    # directly
    twine upload dist/*
elif [ -n "$TEST" ]; then
    # Upload to TestPyPI
    python setup.py register -r https://testpypi.python.org/pypi
    twine upload dist/* -r testpypi
    pip install -i https://testpypi.python.org/pypi $PACKAGE_NAME
fi
