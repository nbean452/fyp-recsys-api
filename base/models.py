from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class UserDetail(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='detail')
    taken_course = ArrayField(models.CharField(
        max_length=20), blank=True, default=list)

    def __str__(self):
        return "{}'s activities".format(self.user.username)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=210)
    description = models.TextField()
    availability = ArrayField(models.CharField(max_length=20), size=3)
    prerequisites = ArrayField(models.CharField(
        max_length=100), blank=True, default=list)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

    def get_course_name(self):
        return '{} {}'.format(self.code, self.title)

    def save(self, *args, **kwargs):
        self.name = self.get_course_name()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('code',)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='reviews', on_delete=models.CASCADE)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s: %s out of 5" % (self.course.code, self.rating)
