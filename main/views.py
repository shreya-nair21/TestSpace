from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Option, Result
from django.contrib.auth.models import User

def home(request):
  exams = Exam.objects.all()
  return render(request, 'home.html', {'exams': exams})


@login_required
def take_exam(request, exam_id):
  exam = get_object_or_404(Exam, id=exam_id)
  questions = Question.objects.filter(exam=exam)

  # Check if form was submitted (POST request)
  if request.method == 'POST':
    score = 0

    #Read time taken (sent by hidden input)

    time_taken = int(request.POST.get('time_taken', 0))

    #score calculation
    for q in questions:
      selected_option_id = request.POST.get(str(q.id))
      if selected_option_id:
        option = Option.objects.get(id=selected_option_id)
        if option.is_correct:
          score += 1
    
    # Save result with time taken
    Result.objects.create(
      user=request.user,
      exam=exam,
      score=score,
      time_taken=time_taken
    )
    return redirect('view_result', exam_id=exam.id)
  
  # If GET request, just show the exam
  return render(request, 'take_exam.html', {
    'exam': exam,
    'questions': questions,
    'duration_seconds': exam.duration_minutes * 60,  #timer value
  })


@login_required
def view_result(request, exam_id):
  exam = get_object_or_404(Exam, id=exam_id)
  result = Result.objects.filter(user=request.user, exam=exam).last()

  return render(request, 'result.html', {
    'exam': exam,
    'result': result
  })