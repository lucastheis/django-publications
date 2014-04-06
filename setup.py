#!/usr/bin/env python

from setuptools import setup, find_packages
from publications import __version__

setup(
	name='django-publications',
	version=__version__,
	author='Lucas Theis',
	author_email='lucas@theis.io',
	description='A Django app for managing publications.',
	url='https://github.com/lucastheis/django-publications',
	packages=find_packages(),
	include_package_data=True,
	install_requires=('Python>=2.5.0', 'Django>=1.4.0', 'Pillow>=2.3.0'),
	zip_safe=False,
	license='MIT',
	classifiers=(
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python'),
)
