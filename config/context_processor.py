from django.conf import settings
from django.contrib.sites.models import Site


def site_common_settings(request):
    current_site = Site.objects.get_current()
    return {
        'site_title': current_site.name,
        'show_terms_of_use': getattr(settings, 'SHOW_TERMS_OF_USE', True),
        'show_privacy_policy': getattr(settings, 'SHOW_PRIVACY_POLICY', True),
        'open_user_registration': getattr(settings, 'OPEN_USER_REGISTRATION', True),
    }
