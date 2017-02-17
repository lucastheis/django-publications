from publications.models import CustomLink, CustomFile

def populate(publications):
	"""
	Load custom links and files from database and attach to publications.
	"""

	customlinks = CustomLink.objects.filter(publication__in=publications)
	customfiles = CustomFile.objects.filter(publication__in=publications)

	publications_ = {}
	for publication in publications:
		publication.links = []
		publication.files = []
		publications_[publication.id] = publication

	for link in customlinks:
		publications_[link.publication_id].links.append(link)
	for file in customfiles:
		publications_[file.publication_id].files.append(file)
