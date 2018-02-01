from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from papers.form import PostForm, ReviewForm
from papers.models import Paper, PaperRequests, Reviews
from papers.views import author


@login_required(login_url="http://localhost:8000/login/")
def home(request):
    return author.home(request, base="pcm/base.html")


def profile_show(request):
    return author.profile_show(request, base="pcm/base.html")


def profile_edit(request):
    return author.profile_edit(request, base="pcm/base.html")


def paper_view(request, paper_id):
    return author.paper_view(request, paper_id, base="pcm/base.html")


def paper_update(request, paper_id):
    return author.paper_update(request, paper_id, base="pcm/base.html")


def paper_assigned(request, paper_id=None):
    token = {}
    token['first_name'] = request.user.first_name
    papers = Paper.get_assigned_papers(request.user)
    token['papers'] = papers
    if paper_id:
        token['paper'] = Paper.get_paper(paper_id, papers)
        token['title_right'] = "Paper #" + paper_id
    return render_to_response("pcm/assigned_papers.html", token)


def paper_review(request, paper_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            p = Paper.objects.get(id=paper_id)
            Reviews.objects.filter(paper=p, reviewer=request.user).delete()
            Reviews.objects.update_or_create(paper=p, reviewer=request.user, comment=review.comment, rate=review.rate)
            return redirect("paper_assigned")
    form = ReviewForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['first_name'] = request.user.first_name
    token["paper"] = Paper.get_paper_for_review(request.user, paper_id)
    token['base'] = "pcm/base.html"
    return render_to_response("paper/review.html", token)


def paper_choose(request, paper_id=None):
    token = {}
    token['first_name'] = request.user.first_name
    papers = Paper.other_papers(request.user)
    if paper_id:
        paper = Paper.choosing_paper(paper_id, papers)
        token['title_right'] = 'Paper #' + paper_id
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_request():
                PaperRequests.objects.update_or_create(paper=paper, pcm=request.user)
            elif form.is_cancel():
                PaperRequests.objects.filter(paper=paper, pcm=request.user).delete()
        else:
            form = PostForm()
        token['form'] = form
        paper.is_requested = PaperRequests.is_paper_requested(paper, request.user)
        token['paper'] = paper
    token.update(csrf(request))
    token['papers'] = papers
    return render_to_response('pcm/choose_papers.html', token)
