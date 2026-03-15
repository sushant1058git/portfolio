"""
Contact app views — with IP-based rate limiting.
Max 3 submissions per IP per hour using Django cache.
"""
import hashlib
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def get_client_ip(request):
    """Extract real IP, respecting X-Forwarded-For."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limit_check(ip, limit=3, window=3600):
    """
    Returns (allowed: bool, remaining: int, retry_after: int seconds).
    Uses a sliding window stored in cache.
    """
    key = "rl_contact_" + hashlib.md5(ip.encode()).hexdigest()[:16]
    data = cache.get(key, {"count": 0, "reset_at": None})

    import time
    now = int(time.time())

    # Reset window if expired
    if data["reset_at"] is None or now >= data["reset_at"]:
        data = {"count": 0, "reset_at": now + window}

    if data["count"] >= limit:
        retry_after = data["reset_at"] - now
        return False, 0, retry_after

    data["count"] += 1
    remaining = limit - data["count"]
    cache.set(key, data, window + 10)
    return True, remaining, 0


class ContactView(APIView):
    def post(self, request):
        ip = get_client_ip(request)
        allowed, remaining, retry_after = rate_limit_check(ip)

        if not allowed:
            mins = round(retry_after / 60)
            return Response(
                {
                    "error": f"Too many submissions. Please try again in {mins} minute{'s' if mins != 1 else ''}.",
                    "retry_after": retry_after,
                    "rate_limited": True,
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Validate
        name    = request.data.get("name",    "").strip()
        email   = request.data.get("email",   "").strip()
        subject = request.data.get("subject", "").strip()
        message = request.data.get("message", "").strip()

        errors = {}
        if not name:    errors["name"]    = "Name is required."
        if not email:   errors["email"]   = "Email is required."
        if not subject: errors["subject"] = "Subject is required."
        if not message: errors["message"] = "Message is required."
        if len(message) < 10:
            errors["message"] = "Message must be at least 10 characters."

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Save to DB
        try:
            from .models import ContactMessage
            ContactMessage.objects.create(
                name=name, email=email, subject=subject, message=message
            )
        except Exception:
            pass

        # Send email notification (best-effort)
        try:
            send_mail(
                subject=f"[Portfolio] {subject}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        return Response(
            {
                "message": "Message sent successfully!",
                "remaining_submissions": remaining,
            },
            status=status.HTTP_201_CREATED,
        )