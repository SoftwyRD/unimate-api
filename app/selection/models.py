from __future__ import annotations
from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from subject.models import Subject


class Weekday(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SubjectSection(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    section = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    professor = models.CharField(max_length=60)
    taken = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.subject.code}-{self.section}"


class SectionSchedule(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    section = models.ForeignKey(
        SubjectSection,
        on_delete=models.CASCADE,
        related_name="subject_schedule",
    )
    weekday = models.ForeignKey(Weekday, on_delete=models.SET_NULL, null=True)
    start_time = models.IntegerField(
        default=7, validators=[MinValueValidator(7), MaxValueValidator(20)]
    )
    end_time = models.IntegerField(
        default=9, validators=[MinValueValidator(9), MaxValueValidator(22)]
    )

    def __str__(self) -> str:
        return str(self.id)
