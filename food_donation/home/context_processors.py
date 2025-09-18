from .models import Donor  # ← MUST IMPORT THIS

def donor_profile(request):
    if request.user.is_authenticated:
        try:
            return {'profile': Donor.objects.get(user=request.user)}
        except:
            return {}
    return {}