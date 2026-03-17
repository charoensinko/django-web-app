from django import forms
from .models import TrainingRecord

class TrainingRecordForm(forms.ModelForm):
    class Meta:
        model = TrainingRecord
        fields = ["emp_name", "emp_id", "course", "trainer", "train_date", "score", "status"]
        widgets = {
            "emp_name": forms.TextInput(attrs={"placeholder": "ชื่อ-นามสกุล"}),
            "emp_id": forms.TextInput(attrs={"placeholder": "EMP-XXXX"}),
            "course": forms.TextInput(attrs={"placeholder": "ระบุชื่อหลักสูตรการอบรม"}),
            "trainer": forms.TextInput(attrs={"placeholder": "ชื่อวิทยากร (ถ้ามี)"}),
            "train_date": forms.DateInput(attrs={"type": "date"}),
            "score": forms.NumberInput(attrs={"min": "0", "max": "100", "step": "0.5", "placeholder": "0–100"}),
            "status": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_class = "form-control form-control-dark"
        for name, field in self.fields.items():
            if name == "status":
                field.widget.attrs["class"] = "form-select form-select-dark"
            else:
                field.widget.attrs["class"] = base_class
