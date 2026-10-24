from django.db import models
from django.utils import timezone


class Student(models.Model):
    """A student enrolled at the school."""
    name = models.CharField(max_length=100, verbose_name="Full Name")
    class_name = models.CharField(max_length=50, verbose_name="Class")
    admission_number = models.CharField(
        max_length=30, unique=True, verbose_name="Admission Number"
    )
    is_active = models.BooleanField(default=True, verbose_name="Currently Enrolled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['class_name', 'name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.name} ({self.class_name})"


class Parent(models.Model):
    """A parent/guardian who can visit their student."""
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, verbose_name="Parent Full Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    national_id = models.CharField(
        max_length=30, unique=True, verbose_name="National ID"
    )
    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES,
        default='guardian',
        verbose_name="Relationship to Student"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='parents'
    )
    card_uid = models.CharField(
        max_length=50, unique=True, verbose_name="RFID Card UID"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Parent"
        verbose_name_plural = "Parents"

    def __str__(self):
        return f"{self.name} ({self.get_relationship_display()}) of {self.student.name}"


class Teacher(models.Model):
    """A teacher who uses a card to open the door daily."""
    name = models.CharField(max_length=100, verbose_name="Full Name")
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name="Phone Number"
    )
    card_uid = models.CharField(
        max_length=50, unique=True, verbose_name="RFID Card UID"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.name


class VisitLog(models.Model):
    """One record per parent visit (entry → exit)."""
    STATUS_CHOICES = [
        ('entered', 'Entered'),
        ('exited', 'Exited'),
        ('expired', 'Forced Expired'),
    ]

    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='visits')
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='entered')
    announcement_sent = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-entry_time']
        verbose_name = "Visit Log"
        verbose_name_plural = "Visit Logs"

    def __str__(self):
        return f"{self.parent.name} - {self.entry_time.strftime('%Y-%m-%d %H:%M')} ({self.status})"


class TeacherLog(models.Model):
    """One record per teacher per day (only first swipe counts)."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='logs')
    entry_time = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-entry_time']
        verbose_name = "Teacher Log"
        verbose_name_plural = "Teacher Logs"

    def __str__(self):
        return f"{self.teacher.name} - {self.date}"


class SystemSetting(models.Model):
    """Global settings for visiting hours & reminder."""
    entry_start = models.TimeField(default='10:00', verbose_name="Visiting Start Time")
    entry_deadline = models.TimeField(default='12:30', verbose_name="Entry Cutoff Time")
    visit_end = models.TimeField(default='16:00', verbose_name="Visiting End Time")
    reminder_minutes = models.IntegerField(
        default=5, verbose_name="Reminder After (minutes)"
    )

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return f"Visiting {self.entry_start.strftime('%H:%M')}–{self.entry_deadline.strftime('%H:%M')}, ends {self.visit_end.strftime('%H:%M')}"