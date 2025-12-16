import uuid
import hmac
import hashlib
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

def initiate_payment(request):
    if request.method == 'POST':
        tx_ref = "chris-dn-" + str(uuid.uuid4())
        payload = {
            "amount": request.POST['amount'],
            "currency": "ETB",
            "email": request.POST['email'],
            "first_name": request.POST['first_name'],
            "last_name": request.POST['last_name'],
            "phone_number": request.POST.get('phone_number', ''),
            "tx_ref": tx_ref,
            "callback_url": request.build_absolute_uri('/webhook/'),
            "return_url": request.build_absolute_uri('/thank-you/'),
            "customization": {
                "title": "Donation to Chris DN App",
                "description": "Helping those in need"
            }
        }
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}", "Content-Type": "application/json"}
        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        data = response.json()
        if data.get('status') == 'success':
            return redirect(data['data']['checkout_url'])
    return redirect('home')

@csrf_exempt
def webhook(request):
    signature = request.headers.get('Chapa-Signature')
    expected = hmac.new(settings.CHAPA_WEBHOOK_SECRET.encode(), request.body, hashlib.sha256).hexdigest()
    if signature != expected:
        return JsonResponse({'status': 'invalid'}, status=400)
    data = request.json()
    if data.get('status') == 'success':
        send_mail(
            'New Donation!',
            f"Amount: {data['amount']} ETB from {data['email']}",
            'no-reply@chrisdnapp.org',
            ['admin@chrisdnapp.org'],
        )
    return JsonResponse({'status': 'success'})