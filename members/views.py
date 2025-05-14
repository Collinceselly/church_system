from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from . models import Members
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from children.models import Children


def home(request):
    context = {
        'members_list':Members.objects.all()
    }
    return render(request, 'members/all_members.html', context)

class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        
        return super().dispatch(request, *args, **kwargs)

class MembersListView(CustomLoginRequiredMixin, ListView):
    model = Members
    template_name = 'members/all_members.html'
    context_object_name = 'members_list'
    paginate_by = 2
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Members.objects.filter(
                Q(first_name__icontains=query) | Q(unique_id__icontains=query) | Q(last_name__icontains=query) | Q(middle_name__icontains=query)
            )
        return Members.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class MembersDetailView(CustomLoginRequiredMixin, DetailView):
    model = Members
    template_name = 'members/members_detail.html'

    def get_object(self, queryset = None):
        try:
            return self.request.user.members
        except Members.DoesNotExist:
            raise Http404('No member account found for this user.')
    
    def get_queryset(self):
        return Members.objects.filter(user = self.request.user)
    
class IndividualMemberDetailView(CustomLoginRequiredMixin, DetailView):
    model = Members
    template_name = 'members/individual_member.html'

    def get_queryset(self):
        return Members.objects.filter(user = self.request.user)

class IndividualMemberMoreDetailView(CustomLoginRequiredMixin, DetailView):
    model = Members
    template_name = 'members/individual_member_more.html'

    def get_queryset(self):
        return Members.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()

        children_as_father = Children.objects.filter(father=member)
        children_as_mother = Children.objects.filter(mother=member)

        context['children_as_father'] = children_as_father
        context['children_as_mother'] = children_as_mother

        return context

class MoreMembersDetailView(CustomLoginRequiredMixin, DetailView):
    model = Members
    template_name = 'members/member_more_details.html'
    context_object_name = 'member'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()

        children_as_father = Children.objects.filter(father=member)
        children_as_mother = Children.objects.filter(mother=member)

        context['children_as_father'] = children_as_father
        context['children_as_mother'] = children_as_mother

        return context

class MembersCreateView(CustomLoginRequiredMixin, CreateView): # capturing members details and sending an email with a unique ID
    model = Members
    fields = ['first_name', 'last_name', 'middle_name', 'gender', 'phone_number', 'email_address', 'marital_status', 'membership_by', 'occupation', 'residence_address']

    def form_valid(self, form):
        response = super().form_valid(form)
        member = self.object
        subject = 'Your Membership ID'
        message = (
            f'Dear {member.first_name}, \n\n'
            f'You have been registered with our church, Your unique ID is {member.unique_id} \n\n'
            f'Kindly use the unique ID as a username to create an account at: '
            f"http://127.0.0.1:9090/member/register/\n"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [member.email_address])
        return response

    def get_context_data(self, **kwargs): # Printing the appropriate header when the page is loaded
        context = super().get_context_data(**kwargs)
        context['header'] = 'Register a Member'
        return context

class MembersUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Members
    fields = ['first_name', 'last_name', 'middle_name', 'gender', 'phone_number', 'email_address', 'marital_status', 'membership_by', 'occupation', 'residence_address']

    def get_context_data(self, **kwargs): # Printing the appropriate header when the page is loaded
        context = super().get_context_data(**kwargs)
        context['header'] = "Update Member's Information"
        return context

class MembersDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Members
    success_url = reverse_lazy('members_all')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Member successfully deleted.")
        return super().delete(request, *args, **kwargs)

def about(request):
    return render(request, 'members/about.html')

def home_page(request):
    return render(request, 'members/home_page.html')
