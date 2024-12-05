from .models import Contact

def contact_info(request):
    return {
        'contacts':Contact.objects.first(),
    }