from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView

from .decorators import customers_only, agents_only
from .forms import RequestForm
from .models import Request


class HomeView(TemplateView):
    template_name = "supportdesk/placeholder.html"


@method_decorator(login_required, name='dispatch')
class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    context_object_name = 'requests'
    template_name = 'supportdesk/requests.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Request.objects.filter(user_assigned_to=user)
        else:
            return Request.objects.filter(created_by=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['requests_count'] = Request.objects.filter(
            created_by=user).count()
        if user.is_staff:
            context['users'] = User.objects.filter(is_staff=True)
        return context


@method_decorator([customers_only], name='dispatch')
@method_decorator(login_required, name='dispatch')
class RequestCreateView(LoginRequiredMixin, CreateView):
    form_class = RequestForm
    template_name = "supportdesk/new_request.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.user_assigned_to = User.objects.filter(
            is_staff=True).first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['requests_count'] = Request.objects.filter(
            created_by=user).count()
        return context


@method_decorator([agents_only], name='dispatch')
@method_decorator(login_required, name='dispatch')
class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = "supportdesk/request_detail.html"
    context_object_name = 'request'


@login_required
def mark_request_completed(request, pk):
    data = {}
    try:
        request_instance = Request.objects.get(pk=pk)
        if not request_instance.is_completed:
            request_instance.is_completed = True
            data['response'] = 'completed'
            request_instance.save()
    except Request.DoesNotExist:
        data['response'] = 'error'
    return JsonResponse(data)


@login_required
def reassign_request(request, request_id, agent_id):
    try:
        request_instance = Request.objects.get(pk=request_id)
        request_instance.user_assigned_to = User.objects.get(pk=agent_id)
        request_instance.save()
    except Request.DoesNotExist:
        pass
    return redirect('request_list')
