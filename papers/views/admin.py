# ADMIN Methods
from django.contrib.auth.decorators import login_required
from papers.models import Paper, Admin,PCM,PCC
from django.shortcuts import render_to_response
from django.views.generic.edit import UpdateView


'''pcc_home_buttons = [{'title': 'ASSIGN', 'link': 'pcc/paper/assign_list'},
                    {'title': 'REVIEW', 'link': '#'}]
nav_links = [{'title': 'NOTIFICATION', 'link': '#'},
             {'title': 'SETTINGS', 'link': '#'},
             {'title': 'LOGOUT', 'link': 'logout'}]
user = {
    'nav_links': nav_links,
}'''


@login_required(login_url="http://localhost:8000/login/")
def home(request):
    token = {}
    token["user"] = request.user
    token['papers'] = Paper.objects.all().order_by('submission_date')
    return render_to_response("admin/home.html", token)

def remind(request):
    token = user
    token['buttons'] = admin_home_buttons
    token["user"] = request.user
    return render_to_response("admin/home.html", token)


def manage_account(request):
    token = Admin.objects.all()
    return render_to_response("admin/manageAccount.html", token)


class ADMINPaperUpdate(UpdateView):
    model = Paper
    fields = ['title', 'pcm_one', 'pcm_two', 'pcm_three']
    template_name = "paper/read.html"
    success_url = "/admin/paper/assign_list"

    def get_context_data(self, **kwargs):
        #         paper = Paper.objects.filter(pk)
        kwargs['buttons'] = admin_home_buttons
        kwargs['nav_links'] = nav_links
        kwargs['username'] = self.request.user.first_name
        return UpdateView.get_context_data(self, **kwargs)