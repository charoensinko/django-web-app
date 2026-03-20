from django.db import models

class TrainingRecord(models.Model):
    STATUS_PASS = "ผ่าน"
    STATUS_FAIL = "ไม่ผ่าน"
    STATUS_PENDING = "รอผล"

    STATUS_CHOICES = [
        (STATUS_PASS, "✅ ผ่าน"),
        (STATUS_FAIL, "❌ ไม่ผ่าน"),
        (STATUS_PENDING, "⏳ รอผล"),
    ]

    emp_name = models.CharField(max_length=255, verbose_name="ชื่อพนักงาน")
    emp_id = models.CharField(max_length=50, verbose_name="รหัสพนักงาน")
    course = models.CharField(max_length=255, verbose_name="ชื่อหลักสูตร")
    trainer = models.CharField(max_length=255, blank=True, null=True, verbose_name="วิทยากร / ผู้สอน")
    train_date = models.DateField(verbose_name="วันที่อบรม")
    score = models.FloatField(blank=True, null=True, verbose_name="คะแนน")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PASS,
        verbose_name="สถานะ",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "ข้อมูลการฝึกอบรม"
        verbose_name_plural = "ข้อมูลการฝึกอบรม"

    def __str__(self):
        return f"{self.emp_name} - {self.course}"


class HistoryLog(models.Model):
    action = models.CharField(max_length=50, verbose_name="การกระทำ")
    detail = models.TextField(verbose_name="รายละเอียด")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="เวลา")

    class Meta:
        ordering = ["-id"]
        verbose_name = "ประวัติการดำเนินการ"
        verbose_name_plural = "ประวัติการดำเนินการ"

    def __str__(self):
        return f"{self.action} - {self.timestamp:%Y-%m-%d %H:%M:%S}"

    @classmethod
    def log(cls, action, detail):
        return cls.objects.create(action=action, detail=detail)
