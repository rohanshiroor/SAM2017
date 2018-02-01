from django.contrib import admin
from papers.models import Author, PCM, PCC, Admin

# Register your models here.
admin.site.register(Author)
admin.site.register(PCM)
admin.site.register(PCC)
admin.site.register(Admin)