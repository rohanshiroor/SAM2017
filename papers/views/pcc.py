# PCC Methods
from django.contrib.auth.decorators import login_required
from papers.models import Paper,PaperRequests,PCM, Reviews
from django.shortcuts import render_to_response,render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.db.models.query_utils import Q
from papers.form import AssignForm,RateForm
from django.template.context_processors import csrf

pcc_home_buttons = [{'title' : 'ASSIGN', 'link' : 'pcc/paper/assign_list'},
                    {'title' : 'REVIEW', 'link' : '#'}]
nav_links = [{'title': 'NOTIFICATION', 'link' : '#'},
    {'title': 'SETTINGS', 'link' : '#'},
    {'title': 'LOGOUT', 'link' : 'logout'}]
user = {
    'nav_links' : nav_links,
    }

@login_required(login_url="http://localhost:8000/login/")
def home(request):
    token = {}
    token["user"] = request.user
    token['papers'] = Paper.objects.all().order_by('submission_date')
    return render_to_response("pcc/home.html", token)

def pcc_paper_list(request):
    token = user
    token['buttons'] = pcc_home_buttons
    token["user"] = request.user
    token['papers'] = Paper.objects.all()
    return render_to_response("pcc/assign_papers.html", token)


def assign_papers(request, paper_id):
    error = ''
    msg = ''
    paper = Paper.objects.get(id=paper_id)
    if request.method == 'POST':
        form = AssignForm(request.POST,instance=paper)
        if form.is_valid():
            paper_assign = form.save(commit=False)
            paper_assign.paper = Paper.objects.get(id=paper_id)
            paper_assign.save()
            msg = 'Paper Assigned'
            return render(request, 'pcc/home.html', {
                'AssignForm': form,
                'msg': msg,
            })
        else:
            error = 'An error occurred, please try again.'
    form = AssignForm()
    Requests = PaperRequests.objects.filter(paper=paper)
    token = {}
    token['form'] = AssignForm()
    token['Requests'] = Requests
    token['paper'] = paper
    token.update(csrf(request))
    # return render(request, 'pcc/assign_paper.html', {
    #         'AssignForm': form,
    #         'error': msg,
    #         'Requests':Requests,
    #         'paper':paper,
    #     })
    return render_to_response('pcc/assign_paper.html', token)

def pcc_paper_read(request, paper_id):
    token = user
    token['buttons'] = pcc_home_buttons
    token["user"] = request.user
    token['paper'] = Paper.objects.filter(id=paper_id)[0]
    return render_to_response("paper/read.html", token)

def ratepaperhome(request):
    paper=Paper.objects.all()
    return render_to_response("pcc/ratepaperhome.html",{
        'papers':paper,
    })
def assignpaperhome(request):
    paper=Paper.objects.all()
    return render_to_response("pcc/assignpaperhome.html",{
        'papers':paper,
    })

def ratepaper(request,paper_id):
    paper = Paper.objects.get(id=paper_id)
    reviews = Reviews.objects.filter(paper_id=paper_id)
    if request.method == 'POST':
        form = RateForm(request.POST,instance=paper)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.save()
            return render(request, 'pcc/home.html', {
                'form': form,
            })
    form = RateForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['reviews'] = reviews
    token["paper"] = paper
    return render_to_response("pcc/ratepaper.html",token)



def remind(request):
    token = user
    token['buttons'] = pcc_home_buttons
    token["user"] = request.user
    return render_to_response("pcc/home.html", token)
     
class PCCPaperUpdate(UpdateView):
    model = Paper
    fields = ['title', 'pcm_one', 'pcm_two', 'pcm_three']
    template_name = "paper/read.html"
    success_url = "/pcc/paper/assign_list"

    def get_context_data(self, **kwargs):
#         paper = Paper.objects.filter(pk)
        kwargs['buttons'] = pcc_home_buttons
        kwargs['nav_links'] = nav_links
        kwargs['username'] = self.request.user.first_name
        return UpdateView.get_context_data(self, **kwargs)