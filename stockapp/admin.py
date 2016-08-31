from django.contrib import admin
from .models import stock,users,index
# Register your models here.
admin.site.register(users)
admin.site.register(stock)
admin.site.register(index)