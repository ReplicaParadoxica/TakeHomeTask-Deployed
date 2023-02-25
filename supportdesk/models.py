from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Request(models.Model):
    summary = models.CharField(max_length=200)
    description = models.TextField()
    is_high_priority = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_requests')
    user_assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_requests')
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return self.summary

    def count_days(self):
        today = datetime.now().date()
        date_created = self.date_time.date()
        return (today - date_created).days

    def get_absolute_url(self):
        return reverse("request_detail", kwargs={"pk": self.pk})
