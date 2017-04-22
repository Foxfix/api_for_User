from django.contrib import admin
from django import forms 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _ 
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password','username')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    # add_form = UserCreationForm
    list_display = ('id','username', 'email', 'first_name', 'last_name','is_active'
        ,'balance', 'accaunt')
    list_filter = ('is_active', 'groups')
    readonly_fields = ('date_joined','last_login')
    actions = ['activate']


    def get_fieldsets(self, request, obj=None):
        """ 
        Set the permission field for managers only is_active, 
        for superuser the extended permission. 
        """
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions', 'password')
        else:
            perm_fields = ('is_active',)

        return [(None, {'fields': ('username',)}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 
                    'email', 'balance', 'passport_number', 'balance', 'password')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})] 


    def activate(self, request, queryset):        
        """Specific activities for approve user."""        
        queryset.update(is_active=True)
    activate.short_description = "Activate selected Users" 

    def get_queryset(self, request):
        """ 
        Permission for managers to see only clients profile. 
        Deny viewing superuser and managers profile. 
        """
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False).filter(is_staff=False) 


admin.site.register(User, CustomUserAdmin)
