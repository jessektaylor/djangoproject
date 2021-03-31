
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



class HomeView(generic.TemplateView):
    template_name = "home.html"


    def get_context_data(self, **kwargs):
        context = {'something':'test'}
        return context