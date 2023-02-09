from django.contrib import admin

from .models import Course, Review

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    exclude = ('name',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Review)
