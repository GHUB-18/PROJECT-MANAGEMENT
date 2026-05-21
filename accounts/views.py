# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def onboarding_view(request):

    user = request.user

    # If already onboarded → dashboard
    if user.is_onboarded:
        return redirect("dashboard")

    if request.method == "POST":

        step = int(request.POST.get("step", user.onboarding_step))

        # STEP 1
        if step == 1:

            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.job_title = request.POST.get("job_title", "")

            user.onboarding_step = 2

        # STEP 2
        elif step == 2:

            # Get the profile if it exists, or create a blank one if it doesn't!
            profile, created = Profile.objects.get_or_create(user=user)

            profile.github_username = request.POST.get(
                "github_username", ""
            )

            profile.github_url = request.POST.get(
                "github_url", ""
            )

            profile.save()

            user.onboarding_step = 3

        # STEP 3
        elif step == 3:

            user.is_onboarded = True

        user.save()

        # Finished onboarding
        if user.is_onboarded:
            return redirect("dashboard")

        return redirect("onboarding")

    return render(request, "account/onboarding.html", {
        "step": user.onboarding_step
    })


@login_required
def auth_redirect(request):

    user = request.user

    if not user.is_onboarded:
        return redirect("onboarding")

    return redirect("dashboard")