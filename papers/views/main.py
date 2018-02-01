from SAM2017 import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from papers.views import author, pcc, pcm, admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from papers.models import *

AUTHOR = 0
PCM = 1
PCC = 2
ADMIN = 3


def authorize(users):
    def true_decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                user_type = get_user_type(args[0])
            except:
                return redirect("http://localhost:8000/login/")

            if user_type == AUTHOR & AUTHOR in users:
                return getattr(author, fn.__name__)(*args, **kwargs)
            elif user_type == PCM & PCM in users:
                return getattr(pcm, fn.__name__)(*args, **kwargs)
            elif user_type == PCC & PCC in users:
                return getattr(pcc, fn.__name__)(*args, **kwargs)
            elif user_type == ADMIN & ADMIN in users:
                return getattr(admin, fn.__name__)(*args, **kwargs)
            else:
                raise PermissionDenied()
        return wrapper
    return true_decorator


def get_user_type(request):
    return request.user.user_type


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR, PCM, PCC, ADMIN])
def home(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR, PCM, PCC])
def paper_view(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR, PCM])
def paper_update(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR, PCM])
def profile_show(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR, PCM])
def profile_edit(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([PCM])
def paper_assigned(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([PCM])
def paper_choose(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([PCM])
def paper_review(request, paper_id):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([AUTHOR])
def register(request):
    pass


@login_required(login_url="http://localhost:8000/login/")
@authorize([ADMIN])
def manage_account(request):
    pass


@deprecate_current_app
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            
            """
            Added following if condition to manipulate 
            """
            if form.get_user().is_admin:
                redirect_to = "/admin/login/"

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
