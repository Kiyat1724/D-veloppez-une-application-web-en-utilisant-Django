from django.contrib import admin
from .models import CustomUser, Ticket, Review, UserFollows


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
