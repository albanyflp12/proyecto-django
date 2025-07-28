from django.shortcuts import redirect
from functools import wraps

def user_tipo_requerido(tipo_permitido):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                perfil = request.user.userprofile
            except Exception:
                return redirect('login')
            if perfil.tipo != tipo_permitido:
                # Podés redirigir a home o a una página de error o dashboard genérico
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
