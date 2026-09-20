from django.urls import path


from main.views import (show_main, show_experience, show_projects, 
                        create_project, get_projects_json, delete_project, show_education,
    create_education,
    edit_education,
    delete_education,)


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path(
    "education/<uuid:education_id>/edit/",
    edit_education,
    name="edit_education",
),
    path(
    "education/<uuid:education_id>/delete/",
    delete_education,
    name="delete_education",
),
]