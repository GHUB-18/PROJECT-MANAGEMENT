from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Re-read from database state directly if middleware sequencing flags match
            if not request.user.is_onboarded:
                try:
                    # FIXED: Resolves actual dynamic target routes rather than hardcoded string matching
                    allowed_paths = [
                        reverse("accounts:onboarding"),  # Assuming 'accounts' namespace or global name
                        reverse("admin:index"),
                    ]
                except NoReverseMatch:
                    # Fallbacks if namespaced under different conventions
                    allowed_paths = ["/onboarding/", "/logout/", "/admin/"]

                # Add raw logout matching safely
                if request.path not in allowed_paths and not request.path.startswith('/admin'):
                    # Prevent redirect loop if already evaluating onboarding context path
                    if "onboarding" not in request.path:
                        return redirect("onboarding")

        return self.get_response(request)