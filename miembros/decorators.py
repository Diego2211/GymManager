from django.contrib.auth.decorators import user_passes_test

def admin_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='admin_gym').exists()
    )(view_decorator)

    return decorated_view

def admin_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='admin_gym').exists()
    )(view_decorator)

    return decorated_view

def staff_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and (
            u.groups.filter(name='Admin_Gym').exists() or
            u.groups.filter(name='profesor').exists()
        )
    )(view_decorator)

    return decorated_view