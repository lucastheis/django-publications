from django.apps import AppConfig
from django.conf import settings


class PublicationsBootstrapConfig(AppConfig):
    name = 'publications_bootstrap'
    verbose_name = "Bootstrap-powered scientific publications for Django"

    # TODO: check if dependencies are met

    defaults = {}
    for param in ['bibliography', 'citation', 'marker', 'sorting']:
        try:
            defaults[param] = getattr(settings, '{}_{}'.format(name.upper(), param.upper()))
        except AttributeError:
            pass
