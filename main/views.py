from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Aqila Zoya Yuwono",
        "npm": "2506620293",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aqila Zoya Yuwono",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
