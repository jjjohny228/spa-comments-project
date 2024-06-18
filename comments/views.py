from typing import Any

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.edit import FormMixin
from comments.models import Comment
from .forms import CommentForm
from django.utils.translation import gettext_lazy as _


class CommentListView(ListView):
    model = Comment
    template_name = 'comments/all_comments.html'
    context_object_name = 'comments'
    paginate_by = 5  # Adjust the number of comments per page

    def get_queryset(self):
        order_by_element = self.request.GET.get('order_by')
        order_by_element = 'created_at' if not order_by_element else order_by_element
        order_dir_element = self.request.GET.get('order_dir')

        # Default order is ascending, add '-' prefix for descending
        if order_dir_element == 'asc':
            order_by_element = order_by_element
        else:
            order_by_element = f'-{order_by_element}'

        return Comment.objects.filter(level=0).order_by(order_by_element).prefetch_related('children')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to be passed to the template.
        """
        context = super().get_context_data(**kwargs)
        context['comments_form'] = CommentForm()
        return context


class CommentFormView(FormMixin, View):
    form_class = CommentForm

    def get_success_url(self) -> str:
        """
        Defines the success URL after successfully adding the comment.
        """
        return reverse_lazy('comments:all')

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        print(self.request.POST)
        form = self.get_form()
        print(f'Is form valid: {form.is_valid()}')
        print(form.errors)
        if form.is_valid():
            return self.form_valid(form)
        messages.error(self.request, _("Invalid data in 'text' field"))
        return redirect(self.get_success_url())

    def form_valid(self, form):
        parent_id = self.request.POST.get('parent_id')
        new_comment = form.save(commit=False)
        if parent_id:
            new_comment.parent = get_object_or_404(Comment, id=parent_id)
        new_comment.save()
        print('comment was saved')
        return super().form_valid(form)

