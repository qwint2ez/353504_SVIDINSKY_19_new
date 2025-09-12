from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
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

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.groups.filter(name='Employees').exists()):
            return view_func(request, *args, **kwargs)
        logger.warning(f'Unauthorized access attempt by {request.user} to employee-only view')
        raise PermissionDenied
    return wrapper
