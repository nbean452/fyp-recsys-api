from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(primary_key=True, max_length=8, unique=True)
    description = models.TextField()
    semester = models.SmallIntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s" % (self.code, self.name)

    class Meta:
        ordering = ('code',)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        get_user_model(), related_name='ratings', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='ratings', on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s: %s out of 5" % (self.course.code, self.rating)
