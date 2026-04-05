from django.shortcuts import render,redirect,get_object_or_404
from .models import Articles
from .forms import ArticlesForm
from comments.models import Comment
from django.views.generic import DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

def arts(request):
    query = request.GET.get("q", "")
    articles = Articles.objects.all()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(author__username__icontains=query))
    articles = articles.order_by("-date")
    paginator = Paginator(articles, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "arts/articles.html", {"page_obj": page_obj,"query": query,})


class ArtDetailView(DetailView):
    model = Articles
    template_name = "arts/details_view.html"
    context_object_name = 'article'
    def get_object(self,queryset=None):
        article = super().get_object(queryset)
        article.views += 1
        article.save(update_fields=["views"])
        return article
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None).order_by('-created_at')
        return context


class ArtEditView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Articles
    template_name = "arts/addart.html"
    form_class = ArticlesForm
    raise_exception = True
    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


class ArtDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Articles
    success_url = '/arts/'
    raise_exception = True
    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


@login_required
def add_art (request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
        else:
            error = 'The form is incorrect'
    form = ArticlesForm()
    data = {'form' : form,'error' : error}
    return render(request,'arts/addart.html',data)


@login_required
def like_article(request,pk):
    article = get_object_or_404(Articles,pk=pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    if request.headers.get('HX-Request'):
        return render(request,'arts/like_area.html',{'article':article})
    return redirect("arts:detail",pk=pk)


@login_required
def liked_articles(request):
    articles = request.user.liked_articles.all()
    return render(request,'arts/liked_arts.html',{'articles':articles})
    