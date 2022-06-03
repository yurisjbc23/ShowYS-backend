from users.models import *

def checkFriendship(current_user, other_user):
    return bool(Follow.objects.filter(user_from=current_user,user_to=other_user).count())

