from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    Program,
    Course,
    CourseAllocation,
    Upload,
    UploadVideo,
    ElectronicResource,
)
from .forms import ElectronicResourceForm
from modeltranslation.admin import TranslationAdmin

class ProgramAdmin(TranslationAdmin):
    pass
class CourseAdmin(TranslationAdmin):
    pass
class UploadAdmin(TranslationAdmin):
    pass
class ElectronicResourceAdmin(admin.ModelAdmin):
    form = ElectronicResourceForm
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)

admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation)
admin.site.register(Upload, UploadAdmin)
admin.site.register(UploadVideo)
admin.site.register(ElectronicResource, ElectronicResourceAdmin)
