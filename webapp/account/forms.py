from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# 프로필 수정
class UserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']