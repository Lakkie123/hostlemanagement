from django.contrib import admin
from .models import *

admin.site.site_header = "sahil"
admin.site.site_title = "sahil"
admin.site.index_title = "Admin Dashboard"
admin.site.register(StudentProfile)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomAllocation)
admin.site.register(FeePayment)
admin.site.register(Complaint)
admin.site.register(Notice)
admin.site.register(Visitor)
admin.site.register(HostelFacility)
