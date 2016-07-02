from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

class LoginView(View):
	def post(self, *args, **kwargs):
		username = self.request.POST.get("username")
		password = self.request.POST.get("password")
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(self.request, user)
			#redirect_url = '/dashboard'
			if user.is_superuser:
			    return HttpResponseRedirect(reverse("stock_balance"))
			
			return HttpResponse("this is error")
		return HttpResponse("Invalid credentials")


class LandingView(TemplateView):

    template_name = "landing.html"

def dashboard(request):
	return  render(request, 'dashboard.html',
           context_instance=RequestContext(request))

# Create your views here.

