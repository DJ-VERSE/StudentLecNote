from django.db import models

# Create your models here.
class AttandanceData(models.Model):
    LECTURE_CHOICES = [
        ('ADA', 'ADA'),
        ('CN', 'CN'),
        ('WD', 'WD'),
        ('IPDC', 'IPDC'),
        ('PE', 'PE'),
        ('DE', 'DE'),
    ]

    FACULTY_CHOICES = [
        ('SJA', 'SJA'),
        ('HHM', 'HHM'),
        ('PMC', 'PMC'),
        ('CHM', 'CHM'),
        ('NSS', 'NSS'),
        ('NBN', 'NBN'),
        ('DDS', 'DDS'),
        ('BKB', 'BKB'),
    ]
    lecture = models.CharField(max_length=10, choices=LECTURE_CHOICES)
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES)
    lecture_notes = models.TextField()
    file = models.CharField(max_length=200)
    enrollment = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
