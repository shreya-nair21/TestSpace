from django.db import models
from django.contrib.auth.models import User
import json

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
  time_taken = models.IntegerField(default=0)
  answers = models.JSONField(default=dict)  # Store user answers as {question_id: option_id}

  def get_percentage(self):
    total_questions = self.exam.question_set.count()
    if total_questions == 0:
      return 0
    return round((self.score / total_questions) * 100, 2)

  def __str__(self):
    return f"{self.user.username} - {self.exam.title} - {self.score}"
  


