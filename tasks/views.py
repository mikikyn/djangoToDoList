from django.shortcuts import render, redirect
from tasks.models import Task
from django.db.models import Q
from tasks.forms import TaskForm, SearchForm




def main_page_view(request):
    return render(request,  'base.html')

def tasks_view(request):
    if request.method == "GET":
        search = request.GET.get("search", None)
        category = request.GET.getlist("category", None)

        tasks = Task.objects.all()
        if search:
            tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category:
            tasks = tasks.filter(category__id__in=category)
        form = SearchForm()
        return render(request, "tasks/tasks.html",  context={"tasks": tasks, "form": form, })

def task_create_view(request):
    if request.method == "GET":
        form = TaskForm
        return render(request, "tasks/task_create.html", context={"form": form})
    if request.method == "POST":
        form = TaskForm(request.POST)
        if not form.is_valid():
            return render(request, "tasks/task_create.html", context={"form": form})
        form.save()
        return redirect("/tasks/")

def task_detail_view(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, "tasks/task_detail.html", context={"task": task})
