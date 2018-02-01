from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from papers.form import PaperForm, ProfileUpdateForm, AuthorCreationForm
from papers.models import Paper, Author


@login_required(login_url="http://localhost:8000/login/")
def home(request, base="author/base.html"):
    if request.method == 'POST':
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.ownedBy = get_user(request)
            paper.author = Author.get_author(request)
            if request.FILES.__len__() == 1:
                paper.file = request.FILES['file']
            paper.save()
            redirect_to = "/papers/"+str(paper.id)+"/success"
            return redirect(redirect_to)
    else:
        form = PaperForm()
    token = {}
    token['first_name'] = request.user.first_name
    token['title_right'] = 'Submit a new paper'
    token["user"] = request.user
    token['papers'] = Paper.get_papers(user_id=request.user.id)
    token.update(csrf(request))
    token['form'] = form
    token['base'] = base
    return render_to_response('author/home.html', token)


@login_required(login_url="http://localhost:8000/login/")
def profile_show(request, base="author/base.html"):
    token = {}
    token['first_name'] = request.user.first_name
    token['last_name'] = request.user.last_name
    token['username'] = request.user.username
    token["phone_number"] = request.user.phone_number
    token["address"] = request.user.get_address()
    token['base'] = base
    return render_to_response('user/profile/view.html', token)


def profile_edit(request, base="author/base.html"):
    token = {}
    token['first_name'] = request.user.first_name
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            Author.update_user(request.user.id, new_user)
            return redirect("profile")
    else:
        user = request.user
        form = ProfileUpdateForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'street_line_1': user.street_line_1,
                     'street_line_2': user.street_line_2, 'city': user.city, 'state': user.state,
                     'zip_code': user.zip_code, 'phone_number': user.phone_number})
    token.update(csrf(request))
    token['form'] = form
    token['base'] = base
    token['user'] = request.user
    return render_to_response('user/profile/edit.html', token)


def paper_view(request, paper_id, base="author/base.html"):
    token = {}
    token['first_name'] = request.user.first_name
    papers = Paper.get_papers(user_id=request.user.id)
    paper = Paper.get_paper(paper_id=int(paper_id), papers=papers)
    token['papers'] = papers
    token['paper'] = paper
    token['title_right'] = 'Paper #' + paper_id
    token['base'] = base
    return render_to_response('paper/view.html', token)


def paper_update(request, paper_id, base="author/base.html"):
    token = {}
    token['first_name'] = request.user.first_name
    papers = Paper.get_papers(user_id=request.user.id)
    paper = Paper.get_paper(paper_id=int(paper_id), papers=papers)
    token['papers'] = papers
    token['paper'] = paper

    if request.method == 'POST':
        form = PaperForm(request.POST, request.FILES, initial={'file':paper.file, 'abstract':paper.abstract, 'title':paper.title})
        if form.is_valid():
            new_paper = form.save(commit=False)
            if request.FILES.__len__() == 1:
                new_paper.file = request.FILES['file']
            new_paper.version = str(int(paper.version) + 1)
            Paper.update_paper(paper_id, new_paper)
            redirect_to = "/papers/" + str(paper.id) + "/success"
            return redirect(redirect_to)
    else:
        form = PaperForm()
    token['title_right'] = 'Update Paper #' + paper_id
    token.update(csrf(request))
    token['form'] = form
    token['base'] = base
    return render_to_response('paper/update.html', token)


def register(request):
    if request.method == 'POST':
        form = AuthorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("http://localhost:8000/")
    else:
        form = AuthorCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('registration/registration_form.html', token)