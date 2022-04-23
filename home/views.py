from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreatForm
from django.utils.text import slugify

class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})

class PostDetailView(View):
    form_class = CommentCreatForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        comments = self.post_instance.pcomments.filter(is_replay = False)
        return render(request,'home/detail.html', {'post':self.post_instance, 'comments':comments, 'form_user':self.form_class})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit =False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'your comment submitted successfully','success')
            return redirect('home:post_detail' ,self.post_instance.id , self.post_instance.slug)

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'post deleted successfully','success')
        else:
            messages.error(request,'you cant post delete','warning')
        return redirect('home:index')

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request,'You cant update this post','danger')
            return redirect('home:index')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request,'home/update.html',{'form':form})

    def post(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,'با موفقیت آپدیت شد.!','success')
            return redirect('home:post_detail',post.id,post.slug)

class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def get(self,request,*args,**kwargs):
        form = self.form_class
        return render(request,'home/create.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request,'You create a new post','success')
            return redirect('home:post_detail', new_post.id, new_post.slug )

