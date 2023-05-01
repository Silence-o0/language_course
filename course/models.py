from django.contrib.auth import admin
from django.db import models
from django.contrib.auth.models import User

__all__ = ['Profile', 'TeacherProfile', 'AdminProfile', 'StudentProfile', 'Group', 'GroupMembership',
           'Language', 'Lesson', 'Mark']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                  help_text='Please use the following format: <em>YYYY-MM-DD</em>.')

    class Meta:
        abstract = True


class TeacherProfile(Profile):
    education = models.CharField(max_length=100, null=True, blank=True)
    years_experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Language(models.Model):
    name = models.CharField(max_length=38, unique=True)

    def __str__(self):
        return str(self.name)


class Group(models.Model):
    LANG_LEVEL = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
    ]
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    lang_level = models.CharField(max_length=2, choices=LANG_LEVEL)

    def __str__(self):
        return f'{self.language} {self.lang_level}'


class Lesson(models.Model):
    DAY_WEEK = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wen", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sut", "Saturday"),
        ("sun", "Sunday"),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day_week = models.CharField(max_length=3, choices=DAY_WEEK)
    time_start = models.TimeField(auto_now=False, auto_now_add=False)
    time_finish = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.group)


class AdminProfile(Profile):
    position = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class StudentProfile(Profile):
    groups = models.ManyToManyField(Group, through="GroupMembership")

    def __str__(self):
        return str(self.user)


class GroupMembership(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Mark(models.Model):
    group_membership = models.ForeignKey(GroupMembership, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField()
    description = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f'{self.group_membership.student} {self.mark}'
