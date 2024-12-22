from django.contrib import admin

from .models import NutritionAnalysis
# Register your models here.
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'age', 'gender','height', 'activity_level', 'registration_date')
    search_fields = ('email', 'name')
    list_filter = ('gender', 'activity_level')

admin.site.register(User, UserAdmin) 


# Register the NutritionAnalysis model with the admin site
admin.site.register(NutritionAnalysis)
