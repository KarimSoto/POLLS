from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from .models import DominoStaff
from django.contrib.contenttypes.models import ContentType

def user_gains_perms(request, user_id):
    # Obtener el objeto de usuario
    user = get_object_or_404(User, pk=user_id)

    # Verificar si el usuario ya tiene el permiso
    perm_name = "polls.sell_pizzas"
    perm_already_exists = user.has_perm(perm_name)

    # Obtener el contenido relacionado con el modelo DominoStaff
    content_type = ContentType.objects.get_for_model(DominoStaff)

    # Obtener el objeto de permiso para vender pizzas
    permission = Permission.objects.get(
        codename="sell_pizzas",
        content_type=content_type,
    )

    if not perm_already_exists:
        # Añadir el permiso al usuario solo si no lo tiene
        user.user_permissions.add(permission)

    # Verificar el conjunto de permisos después de añadir el permiso
    has_perm_after_adding = user.has_perm(perm_name)

    return perm_already_exists, has_perm_after_adding