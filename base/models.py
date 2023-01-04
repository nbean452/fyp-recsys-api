from django.conf import settings
from django.db import models

# Create your models here.


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=8, unique=True)
    description = models.TextField()
    semester = models.SmallIntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.code, self.name)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Rating %s: %s" % (self.id, self.rating)
