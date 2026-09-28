import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project, Education
from main.forms import EducationForm


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "npm": "2506620293",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Currently pursuing Computer Science at UI who's "
            "into creative projects, event management, and research. "
            "Powered by curiosity and a drive to build cool things."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "form": form,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def edit_project(request, project_id):
    # Superuser atau user yang punya permission change_project boleh edit
    if not (
        request.user.is_superuser
        or request.user.has_perm("main.change_project")
    ):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "form": form,
        "page_title": "Edit Project",
        "project": project,
    }

    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def show_education(request):
    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "education_list": Education.objects.all().order_by("-started_at"),
    }

    return render(request, "education.html", context)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        form = EducationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Education berhasil ditambahkan."
            )
            return redirect("main:show_education")
    else:
        form = EducationForm()

    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "form": form,
        "page_title": "Add Education",
    }

    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def edit_education(request, education_id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("main.change_education")
    ):
        raise PermissionDenied

    education = get_object_or_404(
        Education,
        id=education_id
    )

    if request.method == "POST":
        form = EducationForm(
            request.POST,
            instance=education
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Education berhasil diperbarui."
            )
            return redirect("main:show_education")
    else:
        form = EducationForm(instance=education)

    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "form": form,
        "page_title": "Edit Education",
    }

    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(
        Education,
        id=education_id
    )

    if request.method == "POST":
        education.delete()
        messages.success(
            request,
            "Education berhasil dihapus."
        )

    return redirect("main:show_education")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name2": "Zoya",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name2": "Zoya",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")