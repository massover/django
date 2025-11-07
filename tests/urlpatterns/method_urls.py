from django.urls import path, re_path

from . import views

urlpatterns = [
    path("no-methods/", views.empty_view, name="no-methods"),
    path.get("no-name/", views.empty_view),
    path("pet/", views.empty_view, methods=["GET"], name="pet-list"),
    path("pet/", views.empty_view, methods=["POST"], name="pet-create"),
    path("pet/<int:year>", views.empty_view, methods=["POST"], name="pet-detail"),
    re_path("^regex/pet/", views.empty_view, methods=["GET"], name="regex-pet-list"),
    re_path("^regex/pet/", views.empty_view, methods=["POST"], name="regex-pet-create"),
    re_path(
        "^regex/pet/<int:year>",
        views.empty_view,
        methods=["GET"],
        name="regex-pet-detail",
    ),
    re_path("^regex/no-methods/", views.empty_view, name="regex-no-methods"),
    re_path.get("^regex/no-name/", views.empty_view),
    path.get("sugar/", views.empty_view, name="sugar-get"),
    path.post("sugar/", views.empty_view, name="sugar-post"),
    path.put("sugar/", views.empty_view, name="sugar-put"),
    path.patch("sugar/", views.empty_view, name="sugar-patch"),
    path.delete("sugar/", views.empty_view, name="sugar-delete"),
    path.head("sugar/", views.empty_view, name="sugar-head"),
    path.options("sugar/", views.empty_view, name="sugar-options"),
    re_path.get("^regex/sugar/", views.empty_view, name="regex-sugar-get"),
    re_path.post("^regex/sugar/", views.empty_view, name="regex-sugar-post"),
    re_path.put("^regex/sugar/", views.empty_view, name="regex-sugar-put"),
    re_path.patch("^regex/sugar/", views.empty_view, name="regex-sugar-patch"),
    re_path.delete("^regex/sugar/", views.empty_view, name="regex-sugar-delete"),
    re_path.head("^regex/sugar/", views.empty_view, name="regex-sugar-head"),
    re_path.options("^regex/sugar/", views.empty_view, name="regex-sugar-options"),
]
