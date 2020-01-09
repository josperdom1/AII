import pytest
import test_helpers

from django.urls import reverse
from django.test import Client


pytestmark = [pytest.mark.django_db]


def tests_Artista_list_view():
    instance1 = test_helpers.create_music_Artista()
    instance2 = test_helpers.create_music_Artista()
    client = Client()
    url = reverse("music_Artista_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Artista_create_view():
    client = Client()
    url = reverse("music_Artista_create")
    data = {
        "Url": http://127.0.0.1,
        "PictureUrl": http://127.0.0.1,
        "Nombre": "text",
        "IdArtista": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Artista_detail_view():
    client = Client()
    instance = test_helpers.create_music_Artista()
    url = reverse("music_Artista_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Artista_update_view():
    client = Client()
    instance = test_helpers.create_music_Artista()
    url = reverse("music_Artista_update", args=[instance.pk, ])
    data = {
        "Url": http://127.0.0.1,
        "PictureUrl": http://127.0.0.1,
        "Nombre": "text",
        "IdArtista": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_UsuarioEtiquetaArtista_list_view():
    instance1 = test_helpers.create_music_UsuarioEtiquetaArtista()
    instance2 = test_helpers.create_music_UsuarioEtiquetaArtista()
    client = Client()
    url = reverse("music_UsuarioEtiquetaArtista_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_UsuarioEtiquetaArtista_create_view():
    IdArtista = test_helpers.create_music_Artista()
    IdTag = test_helpers.create_music_Etiqueta()
    IdUsuario = test_helpers.create_music_Usuario()
    client = Client()
    url = reverse("music_UsuarioEtiquetaArtista_create")
    data = {
        "Fecha": datetime.now(),
        "IdArtista": IdArtista.pk,
        "IdTag": IdTag.pk,
        "IdUsuario": IdUsuario.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_UsuarioEtiquetaArtista_detail_view():
    client = Client()
    instance = test_helpers.create_music_UsuarioEtiquetaArtista()
    url = reverse("music_UsuarioEtiquetaArtista_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_UsuarioEtiquetaArtista_update_view():
    IdArtista = test_helpers.create_music_Artista()
    IdTag = test_helpers.create_music_Etiqueta()
    IdUsuario = test_helpers.create_music_Usuario()
    client = Client()
    instance = test_helpers.create_music_UsuarioEtiquetaArtista()
    url = reverse("music_UsuarioEtiquetaArtista_update", args=[instance.pk, ])
    data = {
        "Fecha": datetime.now(),
        "IdArtista": IdArtista.pk,
        "IdTag": IdTag.pk,
        "IdUsuario": IdUsuario.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Usuario_list_view():
    instance1 = test_helpers.create_music_Usuario()
    instance2 = test_helpers.create_music_Usuario()
    client = Client()
    url = reverse("music_Usuario_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Usuario_create_view():
    client = Client()
    url = reverse("music_Usuario_create")
    data = {
        "IdUsuario": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Usuario_detail_view():
    client = Client()
    instance = test_helpers.create_music_Usuario()
    url = reverse("music_Usuario_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Usuario_update_view():
    client = Client()
    instance = test_helpers.create_music_Usuario()
    url = reverse("music_Usuario_update", args=[instance.pk, ])
    data = {
        "IdUsuario": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_UsuarioArtista_list_view():
    instance1 = test_helpers.create_music_UsuarioArtista()
    instance2 = test_helpers.create_music_UsuarioArtista()
    client = Client()
    url = reverse("music_UsuarioArtista_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_UsuarioArtista_create_view():
    IdArtista = test_helpers.create_music_Artista()
    IdUsuario = test_helpers.create_music_Usuario()
    client = Client()
    url = reverse("music_UsuarioArtista_create")
    data = {
        "TiempoEscucha": 1,
        "IdArtista": IdArtista.pk,
        "IdUsuario": IdUsuario.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_UsuarioArtista_detail_view():
    client = Client()
    instance = test_helpers.create_music_UsuarioArtista()
    url = reverse("music_UsuarioArtista_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_UsuarioArtista_update_view():
    IdArtista = test_helpers.create_music_Artista()
    IdUsuario = test_helpers.create_music_Usuario()
    client = Client()
    instance = test_helpers.create_music_UsuarioArtista()
    url = reverse("music_UsuarioArtista_update", args=[instance.pk, ])
    data = {
        "TiempoEscucha": 1,
        "IdArtista": IdArtista.pk,
        "IdUsuario": IdUsuario.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Etiqueta_list_view():
    instance1 = test_helpers.create_music_Etiqueta()
    instance2 = test_helpers.create_music_Etiqueta()
    client = Client()
    url = reverse("music_Etiqueta_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Etiqueta_create_view():
    client = Client()
    url = reverse("music_Etiqueta_create")
    data = {
        "TagValue": "text",
        "IdTag": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Etiqueta_detail_view():
    client = Client()
    instance = test_helpers.create_music_Etiqueta()
    url = reverse("music_Etiqueta_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Etiqueta_update_view():
    client = Client()
    instance = test_helpers.create_music_Etiqueta()
    url = reverse("music_Etiqueta_update", args=[instance.pk, ])
    data = {
        "TagValue": "text",
        "IdTag": 1,
    }
    response = client.post(url, data)
    assert response.status_code == 302
