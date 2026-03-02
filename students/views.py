from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Student
from .forms import StudentForm

@login_required
def student_list(request):
    q = request.GET.get("q", "").strip()
    dept = request.GET.get("dept", "").strip()

    qs = Student.objects.all().order_by("-created_at")

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))

    if dept:
        qs = qs.filter(dept__iexact=dept)

    # dept dropdown data
    depts = Student.objects.exclude(dept="").values_list("dept", flat=True).distinct().order_by("dept")

    paginator = Paginator(qs, 5)  # per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "students/list.html", {
        "page_obj": page_obj,
        "q": q,
        "dept": dept,
        "depts": depts,
        "total": qs.count(),
    })

@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
        messages.error(request, "Please fix errors.")
    else:
        form = StudentForm()

    return render(request, "students/form.html", {"form": form, "mode": "create"})

@login_required
def student_edit(request, pk):
    obj = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_list")
        messages.error(request, "Please fix errors.")
    else:
        form = StudentForm(instance=obj)

    return render(request, "students/form.html", {"form": form, "mode": "edit", "item": obj})

@login_required
def student_delete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.info(request, "Student deleted.")
    return redirect("student_list")

@login_required
def student_bulk_delete(request):
    if request.method != "POST":
        return redirect("student_list")

    ids = request.POST.getlist("ids")
    if not ids:
        messages.warning(request, "Select at least one student to delete.")
        return redirect("student_list")

    Student.objects.filter(id__in=ids).delete()
    messages.info(request, f"Deleted {len(ids)} students.")
    return redirect("student_list")