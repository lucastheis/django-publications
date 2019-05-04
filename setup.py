#!/usr/bin/env python

from setuptools import setup, find_packages
from publications import __version__

setup(
	name='django-publications',
	version=__version__,
	author='Lucas Theis',
	author_email='lucas@theis.io',
	description='A Django app for managing scientific publications.',
	url='https://github.com/lucastheis/django-publications',
	packages=find_packages(),
	include_package_data=True,
	install_requires=('Django>=2.1.0', 'Pillow>=2.3.0'),
	zip_safe=False,
	license='MIT',
	classifiers=(
		'Development Status :: 3 - Alpha',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7',
	),
)
