from django.contrib import admin
from .models import TrainingRecord, HistoryLog

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "emp_name", "emp_id", "course", "trainer", "train_date", "score", "status")
    search_fields = ("emp_name", "emp_id", "course", "trainer")
    list_filter = ("status", "train_date")
    ordering = ("-id",)


@admin.register(HistoryLog)
class HistoryLogAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "detail", "timestamp")
    search_fields = ("action", "detail")
    ordering = ("-id",)
