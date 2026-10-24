from django import forms
from .models import Student, Parent, Teacher, SystemSetting


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'class_name', 'admission_number', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'class_name': forms.TextInput(attrs={'placeholder': 'e.g. P5'}),
            'admission_number': forms.TextInput(attrs={'placeholder': 'e.g. ADM001'}),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['name', 'phone_number', 'national_id', 'relationship', 'student', 'card_uid', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Parent full name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+250788123456'}),
            'national_id': forms.TextInput(attrs={'placeholder': 'National ID number'}),
            'card_uid': forms.TextInput(attrs={'placeholder': 'RFID card UID'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone_number', 'card_uid', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Teacher full name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+250788123456'}),
            'card_uid': forms.TextInput(attrs={'placeholder': 'RFID card UID'}),
        }


class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['entry_start', 'entry_deadline', 'visit_end', 'reminder_minutes']
        widgets = {
            'entry_start': forms.TimeInput(attrs={'type': 'time'}),
            'entry_deadline': forms.TimeInput(attrs={'type': 'time'}),
            'visit_end': forms.TimeInput(attrs={'type': 'time'}),
            'reminder_minutes': forms.NumberInput(attrs={'min': 1, 'max': 60}),
        }