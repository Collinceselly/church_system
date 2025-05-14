from django.shortcuts import render, redirect, get_object_or_404
from members.models import Members
from .forms import ContributionForm
from .models import Contribution
import json
from children.decorators import custom_login_required
from django.core.paginator import Paginator

@custom_login_required
def add_contribution(request, member_id):
    member = get_object_or_404(Members, id=member_id)
    
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        
        print("POST Data:", request.POST)  # Debug: See what data is being submitted
        print("Form Valid:", form.is_valid())
        print("Form Errors:", form.errors)
        
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.member = member
            if contribution.mode_of_payment == 'cash':
                contribution.reference_code = None
            contribution.save()
            print("Saved Contribution:", contribution)
            print("Saved Categories:", contribution.categories)
            return redirect('member_contributions', member_id=member_id)

        else:
            print("Form validation failed")
    else:
        form = ContributionForm()
    
    return render(request, 'contributions/add_contribution.html', {
        'member': member,
        'form': form,
    })

@custom_login_required
def member_contributions(request, member_id):
    member = Members.objects.get(id=member_id)
    contributions = Contribution.objects.filter(member=member).order_by('-date')

    paginator = Paginator(contributions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'contributions/member_contributions.html', {'contributions':contributions, 'member':member, 'page_obj':page_obj})

@custom_login_required
def individual_contributions(request, member_id):
    member = Members.objects.get(id=member_id)
    contributions = Contribution.objects.filter(member=member).order_by('-date')

    paginator = Paginator(contributions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contributions/individual_contributions.html', {'contributions':contributions, 'member':member, 'page_obj':page_obj})

@custom_login_required
def all_contributions(request):
    all_contributions = Contribution.objects.select_related('member').order_by('-date')
    
    paginator = Paginator(all_contributions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contributions/all_contributions.html', {'all_contributions':all_contributions, 'page_obj':page_obj})
