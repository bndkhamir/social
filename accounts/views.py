from django.shortcuts import render,redirect
from django.views import View
from . forms import AccountsForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post

class UserRegisterView(View):
    form_class = AccountsForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request,*args,**kwargs)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password1'])
            messages.success(request,'registerd account successfully','success')
            return redirect('home:index')
        return render(request,self.template_name,{'forms':form})

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'forms':form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/Login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'forms':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username = cd['username'], password = cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                return redirect("home:index")
            messages.error(request,'username or password is wrong','warning')
        return render(request,self.template_name,{'forms':form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'You logout successfully', 'success')
        return redirect('home:index')

class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user = user)
        return render(request,'accounts/profile.html', {'user':user,'posts':posts})