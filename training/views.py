from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TrainingRecordForm
from .models import HistoryLog, TrainingRecord

from django.http import HttpResponse
from django.db import connection
from training.models import TrainingRecord
from django.contrib.auth import get_user_model

def debug_db(request):
    User = get_user_model()
    info = connection.settings_dict
    text = f"""
ENGINE: {info.get('ENGINE')}
NAME: {info.get('NAME')}
HOST: {info.get('HOST')}
PORT: {info.get('PORT')}

TrainingRecord count: {TrainingRecord.objects.count()}
User count: {User.objects.count()}
"""
    return HttpResponse(text, content_type="text/plain")

def build_dashboard_context(form=None, edit_obj=None):
    records = TrainingRecord.objects.all()
    histories = HistoryLog.objects.all()[:50]

    return {
        "form": form if form is not None else TrainingRecordForm(instance=edit_obj),
        "edit_obj": edit_obj,
        "records": records,
        "histories": histories,
        "total_count": records.count(),
        "pass_count": records.filter(status=TrainingRecord.STATUS_PASS).count(),
        "fail_count": records.filter(status=TrainingRecord.STATUS_FAIL).count(),
    }


def dashboard(request):
    edit_id = request.GET.get("edit")
    edit_obj = None

    if edit_id:
        edit_obj = get_object_or_404(TrainingRecord, pk=edit_id)

    context = build_dashboard_context(edit_obj=edit_obj)
    return render(request, "training/dashboard.html", context)


def training_add(request):
    if request.method != "POST":
        return redirect("training:dashboard")

    form = TrainingRecordForm(request.POST)
    if form.is_valid():
        obj = form.save()
        HistoryLog.log("เพิ่ม", f"เพิ่มข้อมูล [{obj.emp_name}] หลักสูตร: {obj.course}")
        messages.success(request, "บันทึกข้อมูลเรียบร้อยแล้ว")
        return redirect("training:dashboard")

    messages.error(request, "กรุณาตรวจสอบข้อมูลในฟอร์มอีกครั้ง")
    context = build_dashboard_context(form=form)
    return render(request, "training/dashboard.html", context)


def training_edit(request, pk):
    obj = get_object_or_404(TrainingRecord, pk=pk)

    if request.method != "POST":
        return redirect(f"/?edit={pk}")

    form = TrainingRecordForm(request.POST, instance=obj)
    if form.is_valid():
        updated = form.save()
        HistoryLog.log("แก้ไข", f"แก้ไขข้อมูล [{updated.emp_name}] หลักสูตร: {updated.course}")
        messages.success(request, "บันทึกการแก้ไขเรียบร้อยแล้ว")
        return redirect("training:dashboard")

    messages.error(request, "กรุณาตรวจสอบข้อมูลที่แก้ไขอีกครั้ง")
    context = build_dashboard_context(form=form, edit_obj=obj)
    return render(request, "training/dashboard.html", context)


def training_delete(request, pk):
    obj = get_object_or_404(TrainingRecord, pk=pk)

    if request.method == "POST":
        emp_name = obj.emp_name
        course = obj.course
        obj.delete()
        HistoryLog.log("ลบ", f"ลบข้อมูล [{emp_name}] หลักสูตร: {course}")
        messages.success(request, "ลบข้อมูลเรียบร้อยแล้ว")

    return redirect("training:dashboard")
