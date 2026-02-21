from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .serializers import ContactMessageSerializer
import logging

logger = logging.getLogger(__name__)


class ContactView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

            # Save to DB
            message = serializer.save(ip_address=ip)

            # Send email notification (won't fail the response if email fails)
            try:
                send_mail(
                    subject=f'[Portfolio Contact] {message.subject}',
                    message=f'From: {message.name} <{message.email}>\n\n{message.message}',
                    from_email=settings.EMAIL_HOST_USER or 'noreply@portfolio.com',
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f'Email send failed: {e}')

            return Response(
                {'message': 'Your message has been received! I\'ll get back to you soon.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
