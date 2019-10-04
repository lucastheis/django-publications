django-publications
===================

A Django app for managing scientific publications.

[![Build Status](https://travis-ci.org/lucastheis/django-publications.svg?branch=develop)](https://travis-ci.org/lucastheis/django-publications)
[![Coverage Status](https://coveralls.io/repos/github/lucastheis/django-publications/badge.svg)](https://coveralls.io/github/lucastheis/django-publications)

Screenshots
-----------

[![frontend][3]][1]
[![backend][4]][2]

[1]: https://raw.githubusercontent.com/lucastheis/django-publications/media/frontend.png
[2]: https://raw.githubusercontent.com/lucastheis/django-publications/media/backend.png
[3]: https://raw.githubusercontent.com/lucastheis/django-publications/media/frontend_small.png
[4]: https://raw.githubusercontent.com/lucastheis/django-publications/media/backend_small.png

Features
--------

* automatically creates lists for individual authors and keywords
* BibTex import/export
* RIS export (EndNote, Reference Manager)
* unAPI support (Zotero)
* customizable publication categories/BibTex entry types
* PDF upload
* RSS feeds
* support for images

Requirements
------------

* Python >= 3.5.0
* Django >= 2.1.0
* Pillow >= 2.3.0

Installation
------------

1) Run `pip install django-publications`.

2) Add `'publications'` to `INSTALLED_APPS` in your project's `settings.py`.

3) Add the following to your project's `urls.py`:

	```python
	url(r'^publications/', include('publications.urls')),
	```

4) Run the following:

	```
	./manage.py makemigrations publications
	./manage.py migrate
	```
