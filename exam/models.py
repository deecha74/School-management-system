from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from school.models import Subject

class Exam(models.Model):
    """
    Model representing an exam.
    """
    CATEGORY_CHOICES = [
        ('theory', 'theory'),
        ('practical', 'practical'),

    ]
    EXAM_TYPE=[
        ('midterm', 'Midterm'),
        ('final', 'Final'),

    ]
    class_room = models.ForeignKey('school.ClassRoom', verbose_name=_("Class"), on_delete=models.CASCADE)
    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE,
        default='midterm',
        verbose_name="Exam Type"
    )
    subject =models.ForeignKey(Subject, verbose_name=_("Subject"), on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    Category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='theory',
        verbose_name="Exam Category"
    )
    date = models.DateTimeField(verbose_name="Exam Date")
    duration = models.DurationField(verbose_name="Duration")
    max_marks = models.PositiveIntegerField(verbose_name="Maximum Marks")

    def __str__(self):
        return self.name if hasattr(self, 'name') else f"Exam on {self.subject} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ['-date']



class Result(models.Model):
    """
    Model representing a student's result in an exam.
    """
    exam = models.ForeignKey(Exam, verbose_name=_("Exam"), on_delete=models.CASCADE , related_name='results' )
    student = models.OneToOneField('student.Student', verbose_name=_("Student"), on_delete=models.CASCADE)
    marks_obtained = models.FloatField(verbose_name="Marks Obtained")
    gpa=models.CharField( verbose_name="GPA" ,null=True ,blank=True , choices=[
        ('A+', 'A+'),
        ('A', 'A'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F')
    ])
    grade = models.CharField(max_length=2, blank=True, null=True, verbose_name="Grade")

    def __str__(self):
        return f"{self.student} - {self.exam.subject} - {self.marks_obtained} marks"

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        unique_together = ('exam', 'student')
        ordering = ['exam__date']


