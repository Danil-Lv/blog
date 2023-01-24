from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse


class NewPost(LoginRequiredMixin, CreateView):
    form_class = NewPostForm
    template_name = 'blog/new_post.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(NewPost, self).form_valid(form)

class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = 'index'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        form.instance.author = User.objects.get(username=self.request.user.username)
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('post', kwargs={'url': self.kwargs['slug']})
        return super().get_success_url()


class ShowPostsList(ListView):
    paginate_by = 10
    model = Post
    template_name = 'blog/index.html'



class RegisterUser(CreateView):
    form_class = UserRegisterForm
    success_url = 'profile'
    template_name = 'blog/register.html'


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'blog/login.html'
    success_url = 'index'

    def get_success_url(self):
        url = self.request.GET.get('next')
        if url:
            return url
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_single.html'
    slug_url_kwarg = 'url'

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(post=kwargs['object'])
        kwargs['form'] = CommentForm
        kwargs['comments'] = comments.order_by('-id')
        return super().get_context_data(**kwargs)


def following(request, username):
    author = User.objects.get(username=username)
    if not request.user.id:
        return redirect('login')
    if Follow.objects.filter(user=request.user, author=author):
        return redirect(reverse_lazy('profile', args=(username, )))
    elif author == request.user:
        return redirect(reverse_lazy('profile', args=(username, )))
    Follow.objects.create(user=request.user, author=author)

    return redirect(reverse_lazy('profile', args=(username, )))


def unfollowing(request, username):
    author = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect(reverse_lazy('profile', args=(username,)))


class ShowProfileView(ListView):
    paginate_by = 10
    template_name = 'blog/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # user = User.objects.get(username=self.kwargs['username'])
        author = User.objects.get(username=self.kwargs['username'])
        kwargs['user'] = self.request.user
        kwargs['author'] = author
        kwargs['followers'] = author.follower.all()
        kwargs['following'] = author.following.all()
        if self.request.user.id:
            if Follow.objects.filter(user=self.request.user, author=author):
                kwargs['is_followed'] = True
            else:
                kwargs['is_followed'] = False
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        self.queryset = user.posts.all()
        return super().get_queryset()


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/profile.html'
    form_class = NewPostForm

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        kwargs['user'] = self.request.user
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        if self.request.user.username != self.kwargs['username']:
            return redirect(reverse('post', args=(self.kwargs['slug'], )))
        else:
            return super(UpdatePostView, self).get(request)



def remove_post(request, slug, username):
    if request.user.username == username:
        Post.objects.get(slug=slug).delete()
        return redirect(reverse('profile', args=(username, )))
    return HttpResponse('Error')
