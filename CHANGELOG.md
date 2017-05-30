# django-publications-bootstrap

## 2.0.3 - 30.05.2017
- Avoid RemovedInDjango20Warnings while testing
- Support of Django 1.11

## 2.0.2 - 29.05.2017
- Fix [#25](https://github.com/mbourqui/django-publications-bootstrap/issues/25)
- Fix [#26](https://github.com/mbourqui/django-publications-bootstrap/issues/26)
- Update tests to better cover citekey generation
- Add tests for Publication.month property
- Set warnings for future refacto of Publication methods to properties

## 2.0.1 - 29.05.2017
- Fix [#23](https://github.com/mbourqui/django-publications-bootstrap/issues/23)

## 2.0.0 - 24.05.2017
- Refacto models
  * Renamed `Custom[Link|File]` to `Publication[Link|File]`
  * Replace Enums with django-echoices
- Drop self-hosted libraries for PyPI dependencies
- Drop support of Python 2.7
- Drop support of Django 1.8 due to django-echoices

## 1.0.2 - 11.04.2017
- Drop usage of self-hoster six.py (See #17)
- Update initial data loading

## 1.0.1 - 07.04.2017
- Merge PR [#34](https://github.com/lucastheis/django-publications/pull/34) from source project

## 1.0.0 - 17.02.2017
- Rename project from `django-publications` to `django-publications-bootstrap`
- Merge new features to `master`
- Use Bootstrap 4.0.0-alpha.6 for the layout

## 0.7.0
- Use Bootstrap 4.0.0-alpha.5 for the layout
  - Refactor file inclusions
  - Integration in project's base layout
- Rename person to author
- Add namespace for urls
- WIP update tests
- Update and extend models
 * Renamed `List.list` to `List.title`
 * Renamed `Type.type` to `Type.title`
 * Publication
   - New NullCharField to support nullable but unique CharFields (Fix for Django<1.11)
   - Updated fields:
     + `citekey ` is unique
     + `doi` is unique
     + `isbn` is unique
     + `volume` is CharField
     + issue `number` is CharField
   - Added new fields, to support references to be cited in common formats like ACM or IEEE:
      + editor
      + edition
      + school
      + organization
      + location
      + country (requires django-counties)
      + series
      + volume
      + number
      + chapter
      + section
      + status
   - Updated admin layout
   - Updated Bibtex import to support new fields
   - (Partially) updated export formats to support new fields

## 0.6.2
- Minor bug fixes
- Added migrations
- Allow non-numerical page entries
- Fixed compatibility issues with Django 1.9

## 0.6.1
- Added support for Zotero/unAPI
- Added support for Endnote/RIS
- Bug fixes in BibTex parsing and rendering
- Improved performance
- Dropped support for Django 1.4

## 0.6.0
- Added the possibility to create lists of publications
- Added support for images (requires Pillow)
- Dropped support for Django 1.3

## 0.5.1
- Restored backwards compatibility with Django 1.3
- Improved BibTex parsing
- Added ISBN field

## 0.5.0
- Fixed compatibility issues with Django 1.5, breaks compatibility with Django 1.3
- Added institution field
- Added support for custom links and files
- Author names can now be written with umlauts or digraphs and still be recognized as belonging to one author
- Long author lists are now by default abbreviated with *et al.*
- Curly braces are automatically removed from titles so that they can be used in BibTex entries
- Added a changelog
