from django.contrib import admin

from .models import Course, Rating

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    exclude = ('name',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Rating)
