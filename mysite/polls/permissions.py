from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

def user_gains_perms(request, user_id):
    # Obtener el objeto de usuario
    user = get_object_or_404(User, pk=user_id)

    # Verificar si el usuario ya tiene el permiso
    perm_name = "polls.sell_pizzas"
    perm_already_exists = user.has_perm(perm_name)

    if perm_already_exists :
        return True
    else: 
        return False

    