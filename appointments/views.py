from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm

def appointment_list(request):
    # Kukunin lahat ng active appointments
    appointments = Appointment.objects.filter(is_archived=False).select_related('client', 'service')

    # Search logic
    search_query = request.GET.get('q')
    if search_query:
        appointments = appointments.filter(client__full_name__icontains=search_query)

    # Filter logic (Status)
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        appointments = appointments.filter(status=status_filter)

    # Archive logic (Optional: para makita kung gusto i-view ang archived)
    show_archived = request.GET.get('archived')
    if show_archived == 'true':
        appointments = Appointment.objects.filter(is_archived=True).select_related('client', 'service')
        if search_query:
            appointments = appointments.filter(client__full_name__icontains=search_query)

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'search_query': search_query,
        'status_filter': status_filter,
        'show_archived': show_archived
    })

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/appointment_form.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.utils import timezone

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form, 'is_update': True})

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.is_archived = True
        appointment.archived_at = timezone.now()
        appointment.save()
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})