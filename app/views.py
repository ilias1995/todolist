from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME, logout as auth_logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import FormView, RedirectView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from .models import TodoList
# Create your views here.


class SignUpView(FormView):
    """
    Регистрация пользователя
    """
    form_class = UserCreationForm
    template_name = 'signup.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return self.render_to_response(self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('/')


class LoginView(FormView):
    """
    Логин
    """
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect('/')


class LogoutView(RedirectView):
    """
    Выход
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class TodoListView(ListView):
    """
    Список задач
    """
    model = TodoList
    template_name = "todolist.html"
    paginate_by = 20  # пагинация

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            return context
        except:
            if self.request.user.is_anonymous:
            	return None

    def render_to_response(self, context, **response_kwargs):
        if context is None:
            return HttpResponseRedirect('login')
        return super(TodoListView, self).render_to_response(
            context, **response_kwargs
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            status_val = self.request.GET.get('status')
            priority_val = self.request.GET.get('priority')
            print(status_val, priority_val)
    
            if self.request.user.is_superuser:
                todoolist = TodoList.objects.all()
            else:
                todoolist = TodoList.objects.filter(owner=self.request.user)
        
            if status_val:
    	        todoolist = todoolist.filter(status=status_val)
    
            if priority_val:
    	        todoolist = todoolist.filter(priority=priority_val)
    
            return todoolist