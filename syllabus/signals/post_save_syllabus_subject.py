from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SyllabusSubjectModel


@receiver(post_save, sender=SyllabusSubjectModel)
def post_save_syllabus_subject(sender, instance, created, **kwargs):
    credits_count = 0
    cycles_count = instance.cycle

    if created:
        instance.syllabus.subjects_count += 1

    syllabuses = sender.objects.filter(syllabus=instance.syllabus)
    for syllabus in syllabuses:
        credits_count += syllabus.subject.credits
        if syllabus.cycle > cycles_count:
            cycles_count = syllabus.cycle

    instance.syllabus.cycles_count = cycles_count
    instance.syllabus.credits = credits_count
    instance.syllabus.save()
