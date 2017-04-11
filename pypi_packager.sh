#!/usr/bin/env bash

# This script generates a package and submits it to the Python Package Index
PROGRAM_NAME="pypi_packager"

# Parse arguments
TEMP=$(getopt -n $PROGRAM_NAME -o s --long submit -- "$@")

eval set -- "$TEMP"
while true; do
    case $1 in
        -s|--submit)
            SUBMIT=1; shift; continue
        ;;
        --)
            # no more arguments to parse
            break
        ;;
        *)
            printf "Unknown option %s\n" "$1"
            exit 1
        ;;
    esac
done
eval set -- "$@"

# Clear previous compilations to prevent potential issues and limit disk space usage
rm -f README.rst
rm -rf dist/ build/ django_publications_bootstrap.egg-info/

# Generate doc as restructured text for nice PyPI rendering
pandoc --from=markdown --to=rst --output=README.rst README.md

# Source distribution
python setup.py sdist

# Wheel
python setup.py bdist_wheel

# Upload to PyPI, if asked to
if [ -n "$SUBMIT" ]; then
    twine register dist/django_publications_bootstrap-*.whl
    twine upload dist/*
fi

# Remove generated files
# rm README.rst
# rm -r dist/  build/ django_publications_bootstrap.egg-info/
