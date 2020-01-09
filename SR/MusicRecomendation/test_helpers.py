import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from music import models as music_models


def random_string(length=10):
    # Create a random string of length length
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_User(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_AbstractUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractUser.objects.create(**defaults)


def create_AbstractBaseUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractBaseUser.objects.create(**defaults)


def create_Group(**kwargs):
    defaults = {
        "name": "%s_group" % random_string(5),
    }
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_ContentType(**kwargs):
    defaults = {
    }
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_music_Artista(**kwargs):
    defaults = {}
    defaults["Url"] = ""
    defaults["PictureUrl"] = ""
    defaults["Nombre"] = ""
    defaults["IdArtista"] = ""
    defaults.update(**kwargs)
    return music_models.Artista.objects.create(**defaults)
def create_music_UsuarioEtiquetaArtista(**kwargs):
    defaults = {}
    defaults["Fecha"] = datetime.now()
    if "IdArtista" not in kwargs:
        defaults["IdArtista"] = create_music_Artista()
    if "IdTag" not in kwargs:
        defaults["IdTag"] = create_music_Etiqueta()
    if "IdUsuario" not in kwargs:
        defaults["IdUsuario"] = create_music_Usuario()
    defaults.update(**kwargs)
    return music_models.UsuarioEtiquetaArtista.objects.create(**defaults)
def create_music_Usuario(**kwargs):
    defaults = {}
    defaults["IdUsuario"] = ""
    defaults.update(**kwargs)
    return music_models.Usuario.objects.create(**defaults)
def create_music_UsuarioArtista(**kwargs):
    defaults = {}
    defaults["TiempoEscucha"] = ""
    if "IdArtista" not in kwargs:
        defaults["IdArtista"] = create_music_Artista()
    if "IdUsuario" not in kwargs:
        defaults["IdUsuario"] = create_music_Usuario()
    defaults.update(**kwargs)
    return music_models.UsuarioArtista.objects.create(**defaults)
def create_music_Etiqueta(**kwargs):
    defaults = {}
    defaults["TagValue"] = ""
    defaults["IdTag"] = ""
    defaults.update(**kwargs)
    return music_models.Etiqueta.objects.create(**defaults)
