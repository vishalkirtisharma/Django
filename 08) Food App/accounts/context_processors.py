from vendor import models
from accounts.models import UserProfile
from foodonline_main import settings
def get_vendor(request):
    try:
        vendor = models.Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID':settings.PAYPAL_CLIENT_ID}