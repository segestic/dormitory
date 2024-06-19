from django.contrib import admin
from .models import Student, Room, Hostel, Course, User, Warden
# Register your models here.


admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Warden)