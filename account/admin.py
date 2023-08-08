from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from account.models import UserBase

@admin.register(UserBase)
class AccountAdmin(auth_admin.UserAdmin):

    list_display = ('user_name', 'id' ,'first_name','email', 'is_superuser', )
    search_fields = ("user_name", "first_name", "email")
    fieldsets = (
         (None, {'fields': ( 'user_name', 'first_name' , 'password', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    ordering = ("user_name",)