from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Student, Parent, Teacher, VisitLog, TeacherLog, SystemSetting
from .forms import StudentForm, ParentForm, TeacherForm, SystemSettingForm


# ==================== DASHBOARD ====================
@login_required
def dashboard(request):
    today = timezone.localdate()

    active_visits = VisitLog.objects.filter(
        status='entered', entry_time__date=today
    ).select_related('parent', 'parent__student')

    recent_visits = VisitLog.objects.filter(
        entry_time__date=today
    ).select_related('parent', 'parent__student')[:10]

    context = {
        'today': today,
        'active_visits': active_visits,
        'recent_visits': recent_visits,
        'parents_inside': active_visits.count(),
        'visits_today': VisitLog.objects.filter(entry_time__date=today).count(),
        'teachers_today': TeacherLog.objects.filter(date=today).count(),
        'total_students': Student.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard.html', context)


# ==================== STUDENTS ====================
@login_required
def student_list(request):
    students = Student.objects.all().order_by('class_name', 'name')
    return render(request, 'student_list.html', {'students': students})


@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Add Student', 'cancel_url': '/students/'
    })


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Edit Student', 'cancel_url': '/students/'
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {
        'object': student, 'cancel_url': '/students/'
    })


# ==================== PARENTS ====================
@login_required
def parent_list(request):
    parents = Parent.objects.all().select_related('student').order_by('name')
    return render(request, 'parent_list.html', {'parents': parents})


@login_required
def parent_add(request):
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parent added successfully.')
            return redirect('parent_list')
    else:
        form = ParentForm()
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Add Parent', 'cancel_url': '/parents/'
    })


@login_required
def parent_edit(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parent updated successfully.')
            return redirect('parent_list')
    else:
        form = ParentForm(instance=parent)
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Edit Parent', 'cancel_url': '/parents/'
    })


@login_required
def parent_delete(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        parent.delete()
        messages.success(request, 'Parent deleted.')
        return redirect('parent_list')
    return render(request, 'confirm_delete.html', {
        'object': parent, 'cancel_url': '/parents/'
    })


# ==================== TEACHERS ====================
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'teacher_list.html', {'teachers': teachers})


@login_required
def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Add Teacher', 'cancel_url': '/teachers/'
    })


@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'form_page.html', {
        'form': form, 'page_title': 'Edit Teacher', 'cancel_url': '/teachers/'
    })


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted.')
        return redirect('teacher_list')
    return render(request, 'confirm_delete.html', {
        'object': teacher, 'cancel_url': '/teachers/'
    })


# ==================== VISITS ====================
@login_required
def visit_list(request):
    filter_date = request.GET.get('date', timezone.localdate().strftime('%Y-%m-%d'))
    visits = VisitLog.objects.select_related('parent', 'parent__student')

    if filter_date:
        visits = visits.filter(entry_time__date=filter_date)

    return render(request, 'visit_list.html', {
        'visits': visits.order_by('-entry_time'),
        'filter_date': filter_date,
    })


# ==================== SETTINGS ====================
@login_required
def settings_view(request):
    setting = SystemSetting.objects.first()
    if not setting:
        setting = SystemSetting.objects.create()

    if request.method == 'POST':
        form = SystemSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated.')
            return redirect('settings_view')
    else:
        form = SystemSettingForm(instance=setting)

    return render(request, 'settings.html', {'form': form, 'setting': setting})

# ==================== RFID API FOR ESP32 ====================
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def _get_setting():
    """Return the single SystemSetting row, creating one if missing."""
    setting = SystemSetting.objects.first()
    if not setting:
        setting = SystemSetting.objects.create()
    return setting


def _now_time():
    """Current local time (hours:minutes:seconds)."""
    return timezone.localtime().time()


@csrf_exempt
@require_http_methods(["POST"])
def api_rfid_scan(request):
    """
    Called by ESP32 when a card is tapped.
    Request body: {"card_uid": "A1B2C3D4"}
    Response: {"action": "open"|"deny"|"exit", "message": "...", "announce": "..."}
    """
    # --- Parse JSON ---
    try:
        data = json.loads(request.body)
        card_uid = str(data.get('card_uid', '')).strip().upper()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'action': 'deny', 'message': 'Invalid JSON', 'announce': ''}, status=400)

    if not card_uid:
        return JsonResponse({'action': 'deny', 'message': 'Missing card_uid', 'announce': ''}, status=400)

    now = timezone.localtime()
    today = now.date()
    current_time = now.time()
    setting = _get_setting()

    # ============ 1. TEACHER CARD ============
    teacher = Teacher.objects.filter(card_uid=card_uid, is_active=True).first()
    if teacher:
        # Log attendance (once per day)
        already_today = TeacherLog.objects.filter(teacher=teacher, date=today).exists()
        if not already_today:
            TeacherLog.objects.create(teacher=teacher, date=today)
            return JsonResponse({
                'action': 'open',
                'message': f'Welcome {teacher.name}',
                'announce': '',
                'role': 'teacher',
                'first_today': True,
            })
        return JsonResponse({
            'action': 'open',
            'message': f'Welcome back {teacher.name}',
            'announce': '',
            'role': 'teacher',
            'first_today': False,
        })

    # ============ 2. PARENT CARD ============
    parent = Parent.objects.filter(card_uid=card_uid, is_active=True).select_related('student').first()
    if not parent:
        return JsonResponse({
            'action': 'deny',
            'message': 'Unknown card',
            'announce': '',
        })

    # ============ 2a. Already inside today? → this is an EXIT ============
    active_visit = VisitLog.objects.filter(
        parent=parent, status='entered', entry_time__date=today
    ).first()

    if active_visit:
        active_visit.exit_time = now
        active_visit.status = 'exited'
        active_visit.save()
        return JsonResponse({
            'action': 'exit',
            'message': f'Goodbye, parent of {parent.student.name}',
            'announce': '',
            'role': 'parent',
            'student_name': parent.student.name,
            'parent_name': parent.name,
        })

    # ============ 2b. New entry → check time window ============

    # Before visiting hours start
    if current_time < setting.entry_start:
        return JsonResponse({
            'action': 'deny',
            'message': f'Visiting starts at {setting.entry_start.strftime("%H:%M")}',
            'announce': '',
        })

    # After entry cutoff
    if current_time > setting.entry_deadline:
        # After visiting end time?
        if current_time >= setting.visit_end:
            reason = 'Visiting hours have ended'
        else:
            reason = f'Entry closed at {setting.entry_deadline.strftime("%H:%M")}'
        return JsonResponse({
            'action': 'deny',
            'message': reason,
            'announce': '',
        })

    # ============ 2c. Create entry ============
    visit = VisitLog.objects.create(
        parent=parent,
        entry_time=now,
        status='entered',
        announcement_sent=True,
    )

    announce_text = (
        f"Student {parent.student.name}, your parent has arrived. "
        f"Please come to the entrance."
    )

    return JsonResponse({
        'action': 'open',
        'message': f'Welcome, parent of {parent.student.name}',
        'announce': announce_text,
        'role': 'parent',
        'student_name': parent.student.name,
        'parent_name': parent.name,
        'visit_id': visit.id,
        'entry_time': visit.entry_time.strftime('%H:%M'),
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_check_reminders(request):
    """
    Called by ESP32 every 30 seconds to get pending announcements
    for parents who have been waiting more than N minutes.
    """
    now = timezone.localtime()
    today = now.date()
    setting = _get_setting()
    cutoff = now - timedelta(minutes=setting.reminder_minutes)

    pending = VisitLog.objects.filter(
        status='entered',
        entry_time__date=today,
        entry_time__lte=cutoff,
        reminder_sent=False,
    ).select_related('parent', 'parent__student')

    reminders = []
    for visit in pending:
        reminders.append({
            'visit_id': visit.id,
            'student_name': visit.parent.student.name,
            'parent_name': visit.parent.name,
            'announce': (
                f"Student {visit.parent.student.name}, your parent is still waiting. "
                f"Please come to the entrance."
            ),
            'waiting_minutes': int((now - visit.entry_time).total_seconds() / 60),
        })
        visit.reminder_sent = True
        visit.save()

    return JsonResponse({
        'count': len(reminders),
        'reminders': reminders,
        'server_time': now.strftime('%H:%M:%S'),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_force_end(request):
    """
    Expire all unfinished visits.
    Should be called at visiting end time (e.g., 16:00) by a cron job or manual action.
    """
    now = timezone.localtime()
    today = now.date()
    setting = _get_setting()

    # Optional: only allow after visit_end time (unless ?force=1)
    force = request.GET.get('force') == '1'
    if not force and now.time() < setting.visit_end:
        return JsonResponse({
            'action': 'not_yet',
            'message': f'Visiting hours end at {setting.visit_end.strftime("%H:%M")}',
            'expired_count': 0,
        })

    expired = VisitLog.objects.filter(status='entered', entry_time__date=today)
    count = expired.count()
    expired.update(status='expired', exit_time=now)

    return JsonResponse({
        'action': 'done',
        'expired_count': count,
        'message': f'{count} visit(s) force-expired.',
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_status(request):
    """Health check / status endpoint. Useful for testing connectivity."""
    setting = _get_setting()
    now = timezone.localtime()
    return JsonResponse({
        'status': 'ok',
        'server_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'visiting_hours': {
            'entry_start': setting.entry_start.strftime('%H:%M'),
            'entry_deadline': setting.entry_deadline.strftime('%H:%M'),
            'visit_end': setting.visit_end.strftime('%H:%M'),
            'reminder_minutes': setting.reminder_minutes,
        },
        'counts': {
            'students': Student.objects.filter(is_active=True).count(),
            'parents': Parent.objects.filter(is_active=True).count(),
            'teachers': Teacher.objects.filter(is_active=True).count(),
            'inside_now': VisitLog.objects.filter(status='entered', entry_time__date=now.date()).count(),
        },
    })

@login_required
def api_tester(request):
    """Simple page to test the RFID API without hardware."""
    return render(request, 'api_tester.html')