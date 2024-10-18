from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile,Feedback
from django.utils.timesince import timesince
from django.utils.timezone import now


class ProfileAdmin(UserAdmin):
    # Display these fields in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender', 'profile_image', 'city', 'bio')}),
    )

# Register the custom user model

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback

    list_display = ["text","comment","like","real","user","Create_At"]

    fieldsets =(
        (None, {'fields': ('user', 'text', 'comment', 'like','real')}),
    )

    def Create_At(self,obj):

        return timesince(obj.created_date,now())

    Create_At.short_description = 'Time Since Created'



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Feedback, FeedbackAdmin)

