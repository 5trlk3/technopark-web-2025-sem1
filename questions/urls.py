from django.urls import path
from questions.views import index, question, ask, hot_index, tag, user_profile, signup, login, settings

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
