from django.shortcuts import render

from main.models import Experience, Project


def show_main(request):
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
    context = {
        "name": "Aqila Zoya Yuwono",
        "name2": "Zoya",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)