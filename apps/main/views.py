from django.views.generic import TemplateView


class MainpageView(TemplateView):
    template_name = 'main/index.html'
