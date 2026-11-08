from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience

from datetime import date

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from main.models import Education

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class EducationAPITest(APITestCase):
    def setUp(self):
        # Membuat data Education untuk pengujian
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            description="Program studi ilmu komputer.",
            started_at=date(2025, 8, 1),
            ended_at=None,
        )

        # Membuat empat jenis kondisi pengguna
        self.user = User.objects.create_user(
            username="regular",
            password="testpassword123",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="testpassword123",
        )

        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpassword123",
        )

        # Memasukkan Editor ke grup Editor
        self.editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(self.editor_group)

        # URL API
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse(
            "api:education-detail",
            kwargs={"education_id": self.education.id},
        )
        self.star_url = reverse(
            "api:education-star",
            kwargs={"education_id": self.education.id},
        )

        # Data untuk POST dan PUT
        self.valid_payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S1 Informatika",
            "description": "Pendidikan bidang teknologi.",
            "started_at": "2024-08-01",
            "ended_at": None,
        }

    # ==========================================
    # ANONYMOUS USER
    # ==========================================

    def test_anonymous_can_get_education_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_education_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_education(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_anonymous_cannot_star_education(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.starred_by.count(), 0)

    # ==========================================
    # REGULAR AUTHENTICATED USER
    # ==========================================

    def test_regular_user_can_get_education(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_star_education(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.education.starred_by.filter(pk=self.user.pk).exists()
        )

    def test_regular_user_can_unstar_education(self):
        self.education.starred_by.add(self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.education.starred_by.filter(pk=self.user.pk).exists()
        )

    def test_regular_user_cannot_create_education(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_regular_user_cannot_update_education(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.detail_url,
            {"degree": "Updated Degree"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Ilmu Komputer")

    def test_regular_user_cannot_delete_education(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    # ==========================================
    # EDITOR
    # ==========================================

    def test_editor_can_get_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editor_can_patch_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"degree": "S1 Sistem Informasi"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi")

    def test_editor_can_put_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.put(
            self.detail_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.institution,
            "Institut Teknologi Bandung",
        )

    def test_editor_can_star_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.education.starred_by.filter(pk=self.editor.pk).exists()
        )

    def test_editor_cannot_create_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_cannot_delete_education(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    # ==========================================
    # SUPERUSER
    # ==========================================

    def test_superuser_can_create_education(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)

    def test_superuser_can_update_education(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.patch(
            self.detail_url,
            {"degree": "S2 Ilmu Komputer"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S2 Ilmu Komputer")

    def test_superuser_can_delete_education(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    def test_superuser_can_star_education(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.education.starred_by.filter(pk=self.superuser.pk).exists()
        )

    # ==========================================
    # SERIALIZER VALIDATION
    # ==========================================

    def test_serializer_removes_html_tags(self):
        self.client.force_authenticate(user=self.superuser)

        payload = {
            "institution": "<b>Universitas Indonesia</b>",
            "degree": "<i>S1 Ilmu Komputer</i>",
            "description": "<p>Belajar komputer.</p>",
            "started_at": "2025-08-01",
            "ended_at": None,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["institution"],
            "Universitas Indonesia",
        )
        self.assertEqual(
            response.data["degree"],
            "S1 Ilmu Komputer",
        )
        self.assertEqual(
            response.data["description"],
            "Belajar komputer.",
        )

    def test_serializer_rejects_empty_institution_after_strip_tags(self):
        self.client.force_authenticate(user=self.superuser)

        payload = {
            "institution": "<script></script>",
            "degree": "S1 Ilmu Komputer",
            "description": "Deskripsi.",
            "started_at": "2025-08-01",
            "ended_at": None,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 1)

    def test_serializer_rejects_empty_degree_after_strip_tags(self):
        self.client.force_authenticate(user=self.superuser)

        payload = {
            "institution": "Universitas Indonesia",
            "degree": "<b></b>",
            "description": "Deskripsi.",
            "started_at": "2025-08-01",
            "ended_at": None,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 1)

    def test_star_fields_are_read_only(self):
        self.client.force_authenticate(user=self.superuser)

        payload = {
            **self.valid_payload,
            "star_count": 100,
            "is_starred": True,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    # ==========================================
    # NOT FOUND
    # ==========================================

    def test_nonexistent_education_returns_404(self):
        self.client.force_authenticate(user=self.superuser)

        missing_url = reverse(
            "api:education-detail",
            kwargs={
                "education_id": "00000000-0000-0000-0000-000000000000"
            },
        )

        response = self.client.get(missing_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EducationCSRFTTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="csrfuser",
            password="testpassword123",
        )

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            description="Program studi ilmu komputer.",
            started_at=date(2025, 8, 1),
            ended_at=None,
        )

        self.client = APIClient(enforce_csrf_checks=True)

        self.client.login(
            username="csrfuser",
            password="testpassword123",
        )

        self.star_url = reverse(
            "api:education-star",
            kwargs={"education_id": self.education.id},
        )

    def test_authenticated_post_requires_csrf_token(self):
        # POST tanpa CSRF token harus ditolak
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            self.education.starred_by.filter(pk=self.user.pk).exists()
        )

        # Ambil CSRF token dari halaman Education
        self.client.get(reverse("main:show_education"))

        csrf_token = self.client.cookies["csrftoken"].value

        # POST dengan CSRF token harus berhasil
        response = self.client.post(
            self.star_url,
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.education.starred_by.filter(pk=self.user.pk).exists()
        )
