def tipo_usuario(request):
    if request.user.is_authenticated:
        try:
            return {'tipo_usuario': request.user.userprofile.tipo}
        except:
            return {'tipo_usuario': None}
    return {'tipo_usuario': None}
