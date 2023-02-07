from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=210)
    description = models.TextField()
    availability = ArrayField(models.CharField(max_length=20), size=3)
    prerequisites = ArrayField(models.CharField(max_length=100))
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_course_name(self):
        return '{} {}'.format(self.code, self.title)

    def save(self, *args, **kwargs):
        self.name = self.get_course_name()
        super().save(*args, **kwargs)

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
