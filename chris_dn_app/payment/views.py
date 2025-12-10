from django.shortcuts import render

# Create your views here.
import uuid, hmac, hashlib, requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

def initiate_payment(request):
    if request.method == 'POST':
        tx_ref = f"donation-{uuid.uuid4()}"
        payload = {
            "amount": request.POST['amount'],
            "currency": "ETB",
            "email": request.POST['email'],
            "first_name": request.POST['first_name'],
            "last_name": request.POST['last_name'],
            "tx_ref": tx_ref,
            "callback_url": "https://your-site.com/payments/webhook/",
            "return_url": "https://your-site.com/thank-you/",
            "customization[title]": "Donation – Helping Hands",
            "customization[description]": "Thank you for your kindness!"
        }
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        resp = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        data = resp.json()
        if data.get('status') == 'success':
            return redirect(data['data']['checkout_url'])
    return redirect('home')

@csrf_exempt
def webhook(request):
    signature = request.headers.get('Chapa-Signature', '')
    expected = hmac.new(settings.CHAPA_WEBHOOK_SECRET.encode(), request.body, hashlib.sha256).hexdigest()
    if signature != expected:
        return JsonResponse({'status': 'invalid'}, status=400)
    
    payload = request.json()
    if payload.get('status') == 'success':
        send_mail(
            "New Donation!",
            f"Amount: {payload['amount']} ETB from {payload.get('email')}",
            "no-reply@helpinghands.org",
            ["admin@helpinghands.org"],
        )
    return JsonResponse({'status': 'ok'})