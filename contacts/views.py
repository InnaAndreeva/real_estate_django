from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Contact

# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_inquery = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_inquery:
                messages.error(request, 'You have already done an inquery')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name,
                          email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Send email
        send_mail(
            'Inquery for property',
            'Your have done inquery for ' + listing + ' . Soon we contact you.',
            'innaandreeva17yo@gmail.com',
            [realtor_email, 'iraegorova214@gmail.com'],
            fail_silently=False

        )

        messages.success(
            request, 'Your request has been already submitted. We contact you soon')

        print(listing_id)
        return redirect('/listings/' + listing_id)
