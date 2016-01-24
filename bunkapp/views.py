from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView

class LandingView(TemplateView):

    template_name = "landing.html"


def dashboard(request):
	if request.method=="POST":
		print form.cleaned_data

	return  render(request, 'dashboard.html',
           context_instance=RequestContext(request))
# Create your views here.
