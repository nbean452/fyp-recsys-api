from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Course, Review, UserDetail

# Register your models here.


class UserActivityInline(admin.StackedInline):
    model = UserDetail
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserActivityInline]


class CourseAdmin(admin.ModelAdmin):
    exclude = ('name',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(Review)
admin.site.register(UserDetail)
