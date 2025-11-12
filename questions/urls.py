from django.urls import path

from questions.views import (
    ask,
    hot_index,
    index,
    login,
    question,
    settings,
    signup,
    tag,
    user_profile,
)

urlpatterns = [
    path("", index, name="recent"),
    path("hot/", hot_index, name="hot"),
    path("question/<int:id>/", question, name="conc_question"),
    path("ask/", ask, name="ask"),
    path("tag/<str:name>/", tag, name="tag"),
    path("profile/<str:user>/", user_profile, name="user_profile"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("settings/", settings, name="settings"),
]
