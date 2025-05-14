from django.shortcuts import render, redirect
from children.forms import ChildForm
from .models import Children
from members.models import Members
from django.core.paginator import Paginator

from django.http import JsonResponse
from .decorators import custom_login_required

@custom_login_required
def add_child(request):
    if request.method == "POST":
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()  # Save the child directly, as father and mother are already set
            return redirect("children_list")
    else:
        form = ChildForm()

    return render(request, "children/add_child.html", {"form": form})
@custom_login_required
def validate_parent(request, unique_id):
    parent = Members.objects.filter(unique_id=unique_id).first()
    
    if parent:
        return JsonResponse({
            "exists": True, 
            "name": f"{parent.first_name} {parent.last_name}",
            "gender": parent.gender
        })
    else:
        return JsonResponse({"exists": False})
@custom_login_required
def all_children(request):
    all_children = Children.objects.all().order_by('-date_of_birth')

    paginator = Paginator(all_children, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'children/all_children.html', {'all_children':all_children, 'page_obj':page_obj})