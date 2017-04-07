#!/usr/bin/env bash

# This script generates a package for submission to the Python Package Index

# Clear previous compilations to prevent 'caching' issues
rm README.rst
rm -r dist/  build/ django_publications_bootstrap.egg-info/

# Generate doc as restructured text for nice PyPI rendering
pandoc --from=markdown --to=rst --output=README.rst README.md

# Source distribution
python setup.py sdist

# Wheel
python setup.py bdist_wheel

# Upload to PyPI
twine upload dist/*

# Remove generated files
# rm README.rst
# rm -r dist/  build/ django_publications_bootstrap.egg-info/
