
def nombre_usuario(request):
    if request.user.is_authenticated and hasattr(request, 'nombre'):
        return {'nombre_usuario': request.nombre}
    return {'nombre_usuario': ''}