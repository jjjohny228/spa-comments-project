from django.shortcuts import render, get_object_or_404, redirect
from comments.models import Comment
from .forms import CommentForm


def post_detail(request):
    comments = Comment.objects.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            new_comment = comment_form.save(commit=False)
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()
            return redirect('comments:all')
    else:
        comment_form = CommentForm()

    return render(request, 'comments/all_comments.html', {
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment
    })
