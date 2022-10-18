from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class LoginIs_StaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("/register/")
        return super().dispatch(request, *args, **kwargs)
