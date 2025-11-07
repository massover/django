"""Functions for use in URLsconfs."""

from importlib import import_module

from django.core.exceptions import ImproperlyConfigured

from .resolvers import (
    LocalePrefixPattern,
    RegexPattern,
    RoutePattern,
    URLPattern,
    URLResolver,
)


def include(arg, namespace=None):
    app_name = None
    if isinstance(arg, tuple):
        # Callable returning a namespace hint.
        try:
            urlconf_module, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    "Cannot override the namespace for a dynamic module that "
                    "provides a namespace."
                )
            raise ImproperlyConfigured(
                "Passing a %d-tuple to include() is not supported. Pass a "
                "2-tuple containing the list of patterns and app_name, and "
                "provide the namespace argument to include() instead." % len(arg)
            )
    else:
        # No namespace hint - use manually provided namespace.
        urlconf_module = arg

    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)
    patterns = getattr(urlconf_module, "urlpatterns", urlconf_module)
    app_name = getattr(urlconf_module, "app_name", app_name)
    if namespace and not app_name:
        raise ImproperlyConfigured(
            "Specifying a namespace in include() without providing an app_name "
            "is not supported. Set the app_name attribute in the included "
            "module, or pass a 2-tuple containing the list of patterns and "
            "app_name instead.",
        )
    namespace = namespace or app_name
    # Make sure the patterns can be iterated through (without this, some
    # testcases will break).
    if isinstance(patterns, (list, tuple)):
        for url_pattern in patterns:
            pattern = getattr(url_pattern, "pattern", None)
            if isinstance(pattern, LocalePrefixPattern):
                raise ImproperlyConfigured(
                    "Using i18n_patterns in an included URLconf is not allowed."
                )
    return (urlconf_module, app_name, namespace)


def _path(route, view, kwargs=None, name=None, Pattern=None, methods=None):
    from django.views import View

    if kwargs is not None and not isinstance(kwargs, dict):
        raise TypeError(
            f"kwargs argument must be a dict, but got {kwargs.__class__.__name__}."
        )
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        if methods is not None:
            raise TypeError(
                "methods argument must be None when including a url module, "
                f"but got {methods}."
            )
        pattern = Pattern(route, is_endpoint=False)
        urlconf_module, app_name, namespace = view
        return URLResolver(
            pattern,
            urlconf_module,
            kwargs,
            app_name=app_name,
            namespace=namespace,
        )
    elif callable(view):
        pattern = Pattern(route, name=name, is_endpoint=True, methods=methods)
        return URLPattern(pattern, view, kwargs, name)
    elif isinstance(view, View):
        view_cls_name = view.__class__.__name__
        raise TypeError(
            f"view must be a callable, pass {view_cls_name}.as_view(), not "
            f"{view_cls_name}()."
        )
    else:
        raise TypeError(
            "view must be a callable or a list/tuple in the case of include()."
        )


class _Path:
    """
    A callable class for `path()` and `path.get()`
    """

    __slots__ = ("Pattern",)

    def __init__(self, Pattern):
        self.Pattern = Pattern

    def __call__(self, route, view, kwargs=None, name=None, methods=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=methods)

    def get(self, route, view, kwargs=None, name=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=["GET"])

    def post(self, route, view, kwargs=None, name=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=["POST"])

    def put(self, route, view, kwargs=None, name=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=["PUT"])

    def patch(self, route, view, kwargs=None, name=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=["PATCH"])

    def delete(self, route, view, kwargs=None, name=None):
        return _path(
            route, view, kwargs, name, Pattern=self.Pattern, methods=["DELETE"]
        )

    def options(self, route, view, kwargs=None, name=None):
        return _path(
            route, view, kwargs, name, Pattern=self.Pattern, methods=["OPTIONS"]
        )

    def head(self, route, view, kwargs=None, name=None):
        return _path(route, view, kwargs, name, Pattern=self.Pattern, methods=["HEAD"])


path = _Path(Pattern=RoutePattern)
re_path = _Path(Pattern=RegexPattern)
