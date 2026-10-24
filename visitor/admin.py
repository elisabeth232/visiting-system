from django.contrib import admin
from .models import (
    Student, Parent, Teacher, VisitLog, TeacherLog, SystemSetting
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'admission_number', 'is_active')
    list_filter = ('class_name', 'is_active')
    search_fields = ('name', 'admission_number')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'relationship', 'student', 'phone_number',
        'national_id', 'card_uid', 'is_active'
    )
    list_filter = ('relationship', 'is_active')
    search_fields = ('name', 'phone_number', 'national_id', 'card_uid')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'card_uid', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'card_uid')


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = (
        'parent', 'entry_time', 'exit_time', 'status', 'reminder_sent'
    )
    list_filter = ('status', 'entry_time')
    search_fields = ('parent__name', 'parent__student__name')
    readonly_fields = ('entry_time',)


@admin.register(TeacherLog)
class TeacherLogAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'entry_time')
    list_filter = ('date',)
    search_fields = ('teacher__name',)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('entry_start', 'entry_deadline', 'visit_end', 'reminder_minutes')

    def has_add_permission(self, request):
        # Only allow one SystemSetting row
        return not SystemSetting.objects.exists()