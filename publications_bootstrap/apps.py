from django.apps import AppConfig
from django.conf import settings


class PublicationsBootstrapConfig(AppConfig):
    name = 'publications_bootstrap'
    verbose_name = "Bootstrap-powered scientific publications for Django"
    settings_prefix = name.upper()

    defaults = {}
    for param in ['biliography', 'citation', 'marker', 'sorting']:
        try:
            defaults[param] = getattr(settings, '{}_{}'.format(settings_prefix, param.upper()))
        except AttributeError:
            pass
    # TODO: check if dependencies are met
