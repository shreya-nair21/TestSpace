from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  duration_minutes = models.IntegerField(default=30)

  def __str__(self):
    return self.title
  

class Question(models.Model):
  exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
  text = models.CharField(max_length=500)

  def __str__(self):
    return f"{self.exam.title} - {self.text[:50]}"
  

class Option(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=200)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return self.text
  


class Result(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
  score = models.IntegerField()
  submitted_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.username} - {self.exam.title} - {self.score}"
  


