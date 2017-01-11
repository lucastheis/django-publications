# django-publications

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
