import random
from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .forms import ContactForm
from .models import ContactMessage, DepartmentContact
from .serializers import ContactMessageSerializer, DepartmentContactSerializer


def contact_view(request):
    """
    Public Contact & Support page with enquiry submission, unique reference code,
    and direct department contact directory.
    """
    department_contacts = DepartmentContact.objects.all().order_by('department')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            ref_code = f"PTVTI-MSG-{random.randint(1000, 9999)}"
            msg.subject = f"[{ref_code}] {msg.subject}"
            msg.save()

            messages.success(
                request,
                f"Thank you, {msg.name}! Your enquiry has been received. Your reference number is {ref_code}. Our team will contact you shortly."
            )
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'department_contacts': department_contacts,
    }
    return render(request, 'pages/contact.html', context)



class ContactMessageListCreateAPIView(generics.ListCreateAPIView):
    """
    Publicly allows anyone to POST/submit contact messages.
    Requires authentication to GET/list messages (protecting visitor data).
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class ContactMessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Only authenticated users (admins/staff) can view, update, or delete submitted messages.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]


class DepartmentContactListCreateAPIView(generics.ListCreateAPIView):
    """
    Public GET access for department contacts; authentication required to POST.
    """
    queryset = DepartmentContact.objects.all()
    serializer_class = DepartmentContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DepartmentContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Public GET access for department contact details; authentication required to PUT/PATCH/DELETE.
    """
    queryset = DepartmentContact.objects.all()
    serializer_class = DepartmentContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]