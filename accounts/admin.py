from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-is_superuser', 'email',)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            if request.user == obj:
                return False
            elif User.objects.filter(is_superuser=True).count() > 1:
                return True
            elif not obj.is_superuser:
                return True
            else:
                return False


admin.site.register(User, UserAdmin)
