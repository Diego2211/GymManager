from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Perfil_usuario


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):

    if created:
        Perfil_usuario.objects.create(usuario=instance)