from django.db.models.signals import pre_delete
from django.dispatch import receiver

from ..models import SyllabusSubjectModel


@receiver(pre_delete, sender=SyllabusSubjectModel)
def pre_delete_syllabus_subject(sender, instance, **kwargs):
    instance.syllabus.credits -= instance.subject.credits
    instance.syllabus.subjects_count -= 1

    syllabus = (
        sender.objects.filter(syllabus=instance.syllabus)
        .exclude(id=instance.id)
        .order_by("-cycle")
        .first()
    )

    instance.syllabus.cycles_count = 0 if syllabus is None else syllabus.cycle
    instance.syllabus.save()
