[![Python](https://img.shields.io/badge/Python-2.7,3.3,3.4,3.5-blue.svg?style=flat-square)](/)
[![Django](https://img.shields.io/badge/Django-1.8,1.9,1.10-blue.svg?style=flat-square)](/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](/LICENSE)
[![Build Status](https://travis-ci.org/mbourqui/django-publications-bootstrap.svg?branch=master)](https://travis-ci.org/mbourqui/django-publications-bootstrap)
<!--[![Coverage Status](https://coveralls.io/repos/github/lucastheis/django-publications/badge.svg)](https://coveralls.io/github/lucastheis/django-publications)-->


# Bootstrap-powered scientific publications for Django

A Django app for managing scientific publications, providing a Bootstrap-powered UI.


## Screenshots

[![frontend][3]][1]
[![backend][4]][2]

[1]: https://raw.githubusercontent.com/mbourqui/django-publications-bootstrap/media/frontend.png
[2]: https://raw.githubusercontent.com/lucastheis/django-publications/media/backend.png
[3]: https://raw.githubusercontent.com/mbourqui/django-publications-bootstrap/media/frontend_small.png
[4]: https://raw.githubusercontent.com/lucastheis/django-publications/media/backend_small.png


## Features

* automatically creates lists for individual authors and keywords
* BibTex import/export
* RIS export (EndNote, Reference Manager)
* unAPI support (Zotero)
* customizable publication categories/BibTex entry types
* PDF upload
* RSS feeds
* support for images


## Requirements

* Python >= 2.7
* Django >= 1.8.17
* Pillow >= 2.4.0
* `django-countries` >= 4.0
* Bootstrap v4.0.0-alpha.6


## Installation

1. Run `pip install django-publications-bootstrap`.

* Add `publications-bootstrap` to the `INSTALLED_APPS` in your project's settings (usually `settings.py`).

* Add the following to your project's `urls.py`:

        url(r'^publications/', include('publications_bootstrap.urls')),

* In your project's base template, make sure the following blocks are available in the `<head>` tag:
  * `head`, to provide xml content
  * `css`, to provide CSS specific to this application
  
  The content itself will be inserted in the `content` block.

* Run `./manage.py syncdb`.


## Credits

This is a fork of [django-publications](https://github.com/lucastheis/django-publications) from
[lucastheis](https://github.com/lucastheis).
