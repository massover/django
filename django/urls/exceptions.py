from django.http import Http404, Http405


class Resolver404(Http404):
    pass


class Resolver405(Http405):
    pass


class NoReverseMatch(Exception):
    pass
