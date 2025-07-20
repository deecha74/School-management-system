from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from exam.models import Result


@receiver(post_save, sender='exam.Exam')
def create_blank_result(sender, instance, created, **kwargs):
    if not created:
        return

    class_room = instance.class_room
    students = class_room.students.all()

    for student in students:
        Result.objects.get_or_create(
            exam=instance,
            student=student,
            defaults={'marks_obtained': 0, 'gpa': None}
        )