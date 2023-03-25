from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=10)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'question'
