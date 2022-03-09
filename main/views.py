from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self,*args, **kwargs):
        return {"user": self.request.user}
