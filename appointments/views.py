from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm

def appointment_list(request):
    # Base Query
    queryset = Appointment.objects.select_related('client', 'service').all()

    # Kunin ang mga filter mula sa URL
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')
    show_archived = request.GET.get('archived') == 'true'

    # Filter Logic
    if show_archived:
        queryset = queryset.filter(is_archived=True)
    else:
        queryset = queryset.filter(is_archived=False)

    # Search by Name or Service
    if search_query:
        queryset = queryset.filter(
            Q(client__full_name__icontains=search_query) | 
            Q(service__name__icontains=search_query)
        )
    
    # Status Filter
    if status_filter and status_filter != 'all':
        queryset = queryset.filter(status=status_filter)

    # Ordering
    queryset = queryset.order_by('scheduled_at')

    # Stats Cards
    total_count = Appointment.objects.filter(is_archived=False).count()
    active_count = Appointment.objects.filter(is_archived=False, status='scheduled').count()

    context = {
        'appointments': queryset,
        'total_appointments': total_count,
        'active_appointments': active_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'show_archived': show_archived,
    }
    return render(request, 'appointments/appointment_list.html', context)


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment created successfully!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/appointment_form.html', {'form': form})


def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 
        'is_update': True, 
        'appointment': appointment
    })


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        # Soft Delete Logic
        appointment.is_archived = True
        appointment.archived_at = timezone.now()
        appointment.save()
        messages.success(request, "Appointment archived successfully.")
        return redirect('appointment_list')
        
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})


# ITO YUNG BAGONG FUNCTION - Tama na ang indentation
def appointment_restore(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.is_archived = False
        appointment.archived_at = None
        appointment.save()
        messages.success(request, "Appointment restored successfully.")
        return redirect('appointment_list')
    
    return render(request, 'appointments/appointment_confirm_restore.html', {'appointment': appointment})