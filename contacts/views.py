from django.shortcuts import render                                     #type:ignore
from .models import Contact


# Create your views here.

def about_us(request):
    return render(request, 'contacts/biz_barada.html')


def contacts(request):
    our_contacts = Contact.objects.first()
    context = {
        'our_contacts':our_contacts,
    }
    return render(request, 'contacts/contacts.html', context)