from django.contrib import admin

from course.models import *


admin.site.register(TeacherProfile)
admin.site.register(AdminProfile)
admin.site.register(StudentProfile)
admin.site.register(Language)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Lesson)
admin.site.register(Mark)
