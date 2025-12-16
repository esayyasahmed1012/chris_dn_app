from django.shortcuts import render
from django.contrib import messages
from .models import Photo  # Make sure it's Photo (or GalleryPhoto if you named it that)
from .models import Volunteer

def home(request):
    photos = Photo.objects.all()  # This line is crucial!

    if request.method == 'POST':
        # Volunteer form handling
        volunteer = Volunteer(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            message=request.POST.get('message', '')
        )
        volunteer.save()
        messages.success(request, 'Thank you! We will contact you soon.')
    return render(request, 'core/index.html', {'photos': photos})
def thank_you(request):
    return render(request, 'thank_you.html')