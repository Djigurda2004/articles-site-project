from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from arts.models import Articles
from .models import Comment
from django.http import HttpResponseForbidden,HttpResponse

@login_required
def add_comment(request,article_id):
    article = get_object_or_404(Articles,id=article_id)
    if request.method == "POST":
        text = request.POST.get("text")
        parent_id = request.POST.get("parent")
        parent = get_object_or_404(Comment,id=parent_id) if parent_id else None
        comment = Comment.objects.create(article=article,author=request.user,text=text,parent=parent)
        if request.headers.get('HX-Request'):
            return render(request,'comments/comment_node.html',{'node': comment})
    return redirect('arts:detail',article.id)

@login_required
def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    if request.user == comment.author:
        comment.delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("")
    return HttpResponseForbidden()

@login_required
def edit_comment(request,comment_id):
    comment =  get_object_or_404(Comment,id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    if request.method == "GET" and request.headers.get('HX-Request'):
        return render(request,'comments/edit_form.html',{'node':comment})
    if request.method == "POST":
        comment.text = request.POST.get("text")
        comment.save()
        if request.headers.get('HX-Request'):
            return render(request,'comments/comment_node.html',{'node':comment})
    return redirect("arts:detail",comment.article.id)

@login_required
def like_comment(request,comment_id):
    comment = get_object_or_404(Comment,id = comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    if request.headers.get('HX-Request'):
        return render(request, 'comments/like_area.html', {'node': comment})
    return redirect('arts:detail',comment.article.id)