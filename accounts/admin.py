from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birth_date', 'phone_number')}),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'address')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
