def nombre_usuario(request):
    if not request.user.is_authenticated:
        return {'nombre_usuario': ''}
    
    # Si @requiere_roles ya lo cargó, usarlo directamente
    if hasattr(request, 'nombre'):
        return {'nombre_usuario': request.nombre}
    
    # Fallback para vistas sin @requiere_roles
    try:
        return {'nombre_usuario': str(request.user.perfil.nombre)}
    except Exception:
        return {'nombre_usuario': ''}