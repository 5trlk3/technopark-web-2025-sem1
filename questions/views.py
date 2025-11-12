import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

QUESTIONS = []
for i in range(1,60):
  QUESTIONS.append({
    "question": "title " + str(i),
    "id": i,
    "concrete_question": "text" + str(i),
    "answer_count": 5,
    "tags": [{"name": "black-jack"}, {"name": "blender"}],
    "rating": i,
    "user": "user" + str(i),
  })

ANSWERS = []
for i in range(1,60):
  ANSWERS.append({
    "id": i,
    "answer": "Answer is pretty easy! You should ...Answer is pretty easy! You should ..." + str(i),
    "rating": 3,
    "user": "user" + str(i),
  })

TAGS = ["item" + str(i) for i in range(1, 30)]

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

def index(request, *args, **kwargs):
    global HAS_AUTH
    if request.GET.get('in') == 'false':
        HAS_AUTH = "guest"
    if request.GET.get('in') == 'true':
        HAS_AUTH = "authenticated"
    return render(request,
                   'questions/index.html',
                     context={"quest_type": "recent",
                               "questions": paginate(QUESTIONS, request),
                               "has_auth": HAS_AUTH,
                               "tags": TAGS,
                               "cur_tag": "Moon",
                               "title": "FAQ AskVindman",
                               "url_name": 'recent',
                               "need_user_link": False,
                               "popular_questions": QUESTIONS})

def hot_index(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/index.html',
                  context={"quest_type": "hot",
                           "questions": paginate(QUESTIONS, request),
                           "has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "cur_tag": "Moon",
                           "title": "Hot Questions",
                           "url_name": 'hot',
                           "need_user_link": False,
                           "popular_questions": QUESTIONS})

def question(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/question.html',
                  context={"tags": TAGS,
                           "has_auth": HAS_AUTH,
                           "cur_tag": "Moon",
                           "title": "Question",
                           "cur_question": QUESTIONS[kwargs.get('id') - 1],
                           "answers": paginate(ANSWERS, request),
                           "url_name": 'conc_question',
                           "need_user_link": True,
                           "popular_questions": QUESTIONS})

def ask(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/ask.html',
                  context={"tags": TAGS,
                           "popular_questions": QUESTIONS,
                           "has_auth": HAS_AUTH,
                           "cur_tag": "Moon",
                           "title": "Ask",
                           "id": "1",
                           "url_name": 'ask'})

def tag(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/tags.html',
                  context={"questions": paginate(QUESTIONS, request),
                           "has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "chosen_tag": kwargs.get('name'),
                           "cur_tag": "Moon",
                           "title": "Tag",
                           "id": "4",
                           "url_name": 'tag',
                           "need_user_link": True,
                           "popular_questions": QUESTIONS})

def user_profile(request, *args, **kwargs):
    usr = kwargs.get('user')
    if "{" in usr or "}" in usr:
        usr = json.loads(str(usr).replace("\'", "\""))
        usr = usr.get("name")

    return render(request,
                  'questions/profile.html',
                  context={"user": {"name": usr , "about": "Hello, my name is Salvatore. Im glad to see you on my page!"},
                           "has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "cur_tag": "Moon",
                           "title": "Profile",
                           "questions": paginate(QUESTIONS, request),
                           "url_name": 'user_profile',
                           "need_user_link": True,
                           "popular_questions": QUESTIONS})

def signup(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/signup.html',
                   context={"has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "cur_tag": "Moon",
                           "title": "Sign Up",
                           "popular_questions": QUESTIONS,
                           "url_name": 'signup'})

def login(request, *args, **kwargs):
    return render(request,
                  'questions/login.html',
                  context={"has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "cur_tag": "Moon",
                           "title": "Log In",
                           "url_name": 'login',
                           "popular_questions": QUESTIONS})

def settings(request, *args, **kwargs):
    print(kwargs)
    return render(request,
                  'questions/settings.html',
                  context={"user": "user1",
                           "has_auth": HAS_AUTH,
                           "tags": TAGS,
                           "cur_tag": "Moon",
                           "title": "Profile",
                           "popular_questions": QUESTIONS,
                           "url_name": 'settings'})
