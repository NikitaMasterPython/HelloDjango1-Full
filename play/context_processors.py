from .models import UserDate

def user_date(request):
    context = {}
    if request.user.is_authenticated:
        user_date, created = UserDate.objects.get_or_create(user=request.user)
        context['user_date'] = user_date
        context['season'] = user_date.get_season()
    return context
