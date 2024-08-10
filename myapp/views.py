from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .models import Customer, Tests, Phlabo, Booking
from rest_framework import generics
from .serializers import CustomerSerializer, PhlaboSerializer, BookingSerializer, TestsSerializer
from rest_framework import viewsets


class TestsViewSet(viewsets.ModelViewSet):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer



class PhlaboViewSet(viewsets.ModelViewSet):
    queryset = Phlabo.objects.all()
    serializer_class = PhlaboSerializer

class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def send_email(self, phlabo_email, subject, body):
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = phlabo_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, phlabo_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        booking = response.data
        phlabo = Phlabo.objects.get(id=booking['phlabo'])
        subject = "New Booking Created"
        body = f"A new booking has been created with ID: {booking['id']}"
        self.send_email(phlabo.email, subject, body)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        booking = response.data
        phlabo = Phlabo.objects.get(id=booking['phlabo'])
        subject = "Booking Updated"
        body = f"Booking with ID: {booking['id']} has been updated"
        self.send_email(phlabo.email, subject, body)
        return response

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        phlabo = Phlabo.objects.get(id=booking.phlabo.id)
        response = super().destroy(request, *args, **kwargs)
        subject = "Booking Cancelled"
        body = f"Booking with ID: {booking.id} has been cancelled"
        self.send_email(phlabo.email, subject, body)
        return response