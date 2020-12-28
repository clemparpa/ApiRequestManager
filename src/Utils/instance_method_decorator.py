from functools import wraps

def instance_method_wrapper(func):
    """Decorator which return the same func with a 'self' argument in declaration"""
    @wraps(func)
    def decorated_(self, *args, **kwargs):
        return func(*args, **kwargs)
    return decorated_