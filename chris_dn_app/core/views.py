from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from .models import GalleryPhoto, Volunteer

def home(request):
    photos = GalleryPhoto.objects.all().order_by('-created_at')[:12]

    if request.method == 'POST':
        Volunteer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            message=request.POST.get('message', '')
        )
        messages.success(request, 'Thank you! We will contact you soon.')
    
    return render(request, 'index.html', {'photos': photos})

def thank_you(request):
    return render(request, 'thank_you.html')