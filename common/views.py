from django.shortcuts import render
from django.views.generic import TemplateView


class SystemView(TemplateView):
    status = ''
    template_name = 'common/errors/pages_misc_error.html'  # Default template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define the layout for this module
        # _templates/layout/system.html
        context.update(
            {
                'status': self.status,
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, template_name=self.template_name, status=self.status, context=context)
