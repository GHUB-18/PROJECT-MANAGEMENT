from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@login_required
def auth_redirect(request):
    """
    Routes users right after authentication based on onboarding status.
    """
    user = request.user

    # Scenario A: Returning User (Login)
    if user.is_onboarded:
        return redirect("dashboard")

    # Scenario B: Brand New User (Signup)
    return redirect("onboarding")


@login_required
def onboarding_view(request):
    """
    Multi-step onboarding wizard for collecting initial profile details.
    """
    user = request.user

    # If already onboarded → don't let them re-run onboarding
    if user.is_onboarded:
        return redirect("dashboard")

    if request.method == "POST":
        # Fallback to the current user step if it isn't passed in the POST payload
        step = int(request.POST.get("step", user.onboarding_step))

        # STEP 1: Personal Details
        if step == 1:
            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.job_title = request.POST.get("job_title", "").strip()
            user.onboarding_step = 2

        # STEP 2: Developer Profiles
        elif step == 2:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.github_username = request.POST.get("github_username", "").strip()
            profile.github_url = request.POST.get("github_url", "").strip()
            profile.save()
            user.onboarding_step = 3

        # STEP 3: Finalize and complete
        elif step == 3:
            user.is_onboarded = True

        user.save()

        # Check if the process finished during this request cycle
        if user.is_onboarded:
            return redirect("dashboard")

        return redirect("onboarding")

    # GET Request: Render the current wizard step
    return render(request, "account/onboarding.html", {
        "step": user.onboarding_step
    })


@login_required
def profile_view(request):
    """
    Renders the authenticated user's profile view layout.
    """
    return render(request, "profile.html")