django-publications
===================

A Django app for managing publications.

Screenshots
-----------

[![frontend][3]][1]
[![backend][4]][2]

[1]: http://files.theis.io/django-publications/frontend.png
[2]: http://files.theis.io/django-publications/backend.png
[3]: http://files.theis.io/django-publications/frontend_small.png
[4]: http://files.theis.io/django-publications/backend_small.png

Features
--------

* automatically creates lists for individual authors or keywords
* BibTex import/export
* customizable publication categories/BibTex entry types
* PDF upload
* RSS feeds

Requirements
------------

* Python >= 2.5.0
* Django >= 1.4.0

The app should work with the above versions, but older versions might also work.

Installation
------------

1) Copy the `publications` folder to your project.

2) Add `publications` to `INSTALLED_APPS` in your project's `settings.py`.

3) Add the following to your project's `urls.py`:

	url(r'^publications/', include('publications.urls')),
	url(r'^admin/publications/publication/import_bibtex/$', 'publications.admin_views.import_bibtex'),

The second line has to come before `url(r'^admin/', include(admin.site.urls))`!

4) Run `python <yourproject>/manage.py syncdb`
