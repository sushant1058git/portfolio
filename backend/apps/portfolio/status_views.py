"""
System Health Dashboard
/status/ — public read-only health page
/api/status/ — JSON endpoint
"""
import os
import time
import platform
import django
from django.utils import timezone
from django.db import connection
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response


START_TIME = time.time()


def check_database():
    try:
        t0 = time.monotonic()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        ms = round((time.monotonic() - t0) * 1000, 2)
        return {"status": "ok", "latency_ms": ms, "engine": connection.vendor}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_cache():
    try:
        t0 = time.monotonic()
        cache.set("_health_check", "ok", 10)
        val = cache.get("_health_check")
        ms = round((time.monotonic() - t0) * 1000, 2)
        if val == "ok":
            return {"status": "ok", "latency_ms": ms}
        return {"status": "error", "error": "Cache read/write mismatch"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_disk():
    try:
        stat = os.statvfs("/")
        total  = stat.f_frsize * stat.f_blocks
        free   = stat.f_frsize * stat.f_bavail
        used   = total - free
        pct    = round(used / total * 100, 1) if total else 0
        return {
            "status": "ok" if pct < 90 else "warn",
            "total_gb":  round(total / 1e9, 1),
            "used_gb":   round(used  / 1e9, 1),
            "free_gb":   round(free  / 1e9, 1),
            "used_pct":  pct,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_memory():
    try:
        with open("/proc/meminfo") as f:
            data = {}
            for line in f:
                k, v = line.split(":")
                data[k.strip()] = int(v.strip().split()[0])  # kB
        total     = data.get("MemTotal", 0)
        available = data.get("MemAvailable", 0)
        used      = total - available
        pct       = round(used / total * 100, 1) if total else 0
        return {
            "status": "ok" if pct < 90 else "warn",
            "total_mb":    round(total     / 1024, 1),
            "used_mb":     round(used      / 1024, 1),
            "available_mb":round(available / 1024, 1),
            "used_pct":    pct,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_app_counts():
    """Count records from key models."""
    try:
        from apps.blog.models import Post
        from apps.portfolio.models import Profile, Project
        from apps.contact.models import ContactMessage
        return {
            "status":    "ok",
            "posts":     Post.objects.count(),
            "published": Post.objects.filter(status="published").count(),
            "projects":  Project.objects.count() if hasattr(Project, "objects") else 0,
            "messages":  ContactMessage.objects.count(),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_uptime():
    secs = int(time.time() - START_TIME)
    h, rem = divmod(secs, 3600)
    m, s   = divmod(rem, 60)
    return {"seconds": secs, "human": f"{h}h {m}m {s}s"}


class StatusAPIView(APIView):
    """GET /api/status/ — full JSON health payload."""

    def get(self, request):
        db     = check_database()
        ch     = check_cache()
        disk   = check_disk()
        mem    = check_memory()
        counts = check_app_counts()
        uptime = get_uptime()

        checks  = [db, ch, disk, mem, counts]
        overall = "ok"
        for c in checks:
            if c.get("status") == "error":
                overall = "error"
                break
            if c.get("status") == "warn" and overall == "ok":
                overall = "warn"

        return Response({
            "overall":   overall,
            "timestamp": timezone.now().isoformat(),
            "uptime":    uptime,
            "python":    platform.python_version(),
            "django":    django.get_version(),
            "platform":  platform.system(),
            "checks": {
                "database": db,
                "cache":    ch,
                "disk":     disk,
                "memory":   mem,
                "app":      counts,
            },
        })