from django.urls import include
from django.views import defaults

__all__ = [
    "handler400",
    "handler403",
    "handler404",
    "handler405",
    "handler500",
    "include",
]

handler400 = defaults.bad_request
handler403 = defaults.permission_denied
handler404 = defaults.page_not_found
handler405 = defaults.method_not_allowed
handler500 = defaults.server_error
