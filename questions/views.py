from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from questions import models
from django.shortcuts import get_object_or_404

HAS_AUTH = "guest"


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    questions = models.Question.objects.recent()
    global HAS_AUTH
    if request.GET.get('in') == 'false':
        HAS_AUTH = "guest"
    if request.GET.get('in') == 'true':
        HAS_AUTH = "authenticated"
    return render(request,
                   'questions/index.html',
                     context={"quest_type": "recent",
                               "questions": paginate(questions, request),
                               "has_auth": HAS_AUTH,
                               "popular_tags": models.Tag.objects.popular(),
                               "cur_tag": "Moon",
                               "title": "FAQ AskVindman",
                               "url_name": 'recent',
                               "need_user_link": False,
                               "popular_users": models.User_profile.objects.popular()})

def hot_index(request):
    questions = models.Question.objects.hot()
    return render(request,
                  'questions/index.html',
                  context={"quest_type": "hot",
                           "questions": paginate(questions, request),
                           "has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "cur_tag": "Moon",
                           "title": "Hot Questions",
                           "url_name": 'hot',
                           "need_user_link": False})

def question(request, id):
    cur_question = get_object_or_404(models.Question.objects.with_annotations(), id=id)
    answers = models.Answer.objects.for_question(cur_question)
    return render(request,
                  'questions/question.html',
                  context={"popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "has_auth": HAS_AUTH,
                           "cur_tag": "Moon",
                           "title": "Question",
                           "cur_question": cur_question,
                           "answers": paginate(answers, request),
                           "url_name": 'conc_question',
                           "need_user_link": True})

def ask(request):
    return render(request,
                  'questions/ask.html',
                  context={"popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "has_auth": HAS_AUTH,
                           "cur_tag": "Moon",
                           "title": "Ask",
                           "id": "1",
                           "url_name": "ask"})

def tag(request, name):
    questions = models.Question.objects.by_tag(name)
    return render(request,
                  'questions/tags.html',
                  context={"questions": paginate(questions, request),
                           "has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "chosen_tag": name,
                           "cur_tag": "Moon",
                           "title": "Tag",
                           "id": "4",
                           "url_name": 'tag',
                           "need_user_link": True})

def user_profile(request, user):
    profile = get_object_or_404(models.User_profile, nickname=user)
    questions = models.Question.objects.by_user(profile)

    return render(request,
                  'questions/profile.html',
                  context={"user": profile,
                           "has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "cur_tag": "Moon",
                           "title": "Profile",
                           "questions": paginate(questions, request),
                           "url_name": 'user_profile',
                           "need_user_link": True})

def signup(request):
    return render(request,
                  'questions/signup.html',
                   context={"has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "cur_tag": "Moon",
                           "title": "Sign Up",
                           "url_name": 'signup'})

def login(request):
    return render(request,
                  'questions/login.html',
                  context={"has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "cur_tag": "Moon",
                           "title": "Log In",
                           "url_name": 'login'})

def settings(request):
    return render(request,
                  'questions/settings.html',
                  context={"user": "user1",
                           "has_auth": HAS_AUTH,
                           "popular_tags": models.Tag.objects.popular(),
                           "popular_users": models.User_profile.objects.popular(),
                           "cur_tag": "Moon",
                           "title": "Profile",
                           "url_name": 'settings'})
