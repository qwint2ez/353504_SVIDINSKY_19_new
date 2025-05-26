from functools import wraps
from django.http import JsonResponse
import logging

logger = logging.getLogger('pizza')

def api_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.warning(f'Unauthorized API access attempt from IP: {request.META.get("REMOTE_ADDR")}')
            return JsonResponse({
                'error': 'Authentication required',
                'status': 401
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
