from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Appointment

# Ito yung magbibigay ng magandang itsura sa lahat ng input fields
BASE_CLASSES = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'service', 'scheduled_at', 'status', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': BASE_CLASSES}),
            'service': forms.Select(attrs={'class': BASE_CLASSES}),
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': BASE_CLASSES}),
            'status': forms.Select(attrs={'class': BASE_CLASSES}),
            'notes': forms.Textarea(attrs={'class': BASE_CLASSES, 'rows': 4}),
        }

    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')

        if scheduled_at and scheduled_at < timezone.now():
            raise ValidationError("Appointment date and time cannot be in the past.")

        if scheduled_at and scheduled_at.minute not in [0, 30]:
            raise ValidationError("Appointments must start on a 30-minute interval (e.g., 2:00 PM, 2:30 PM).")

        return scheduled_at

    def clean(self):
        cleaned_data = super().clean()
        scheduled_at = cleaned_data.get('scheduled_at')
        status = cleaned_data.get('status')

        if scheduled_at and status == 'scheduled':
            conflicts = Appointment.objects.filter(
                scheduled_at=scheduled_at,
                status='scheduled',
                is_archived=False
            )
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if conflicts.exists():
                raise ValidationError("This time slot is already booked. Please select a different time.")

        return cleaned_data