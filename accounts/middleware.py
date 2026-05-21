from django.shortcuts import redirect


class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if not request.user.is_onboarded:
                allowed_paths = ["/onboarding/", "/logout/", "/admin/"]

                if request.path not in allowed_paths:
                    return redirect("onboarding")

        return self.get_response(request)