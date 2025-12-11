from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Option, Result
from django.contrib.auth.models import User

@login_required(login_url='login')
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
    answers = {}

    # Read time taken (sent by hidden input)
    time_taken = int(request.POST.get('time_taken', 0))

    # Score calculation and collect answers
    for q in questions:
      selected_option_id = request.POST.get(str(q.id))
      if selected_option_id:
        try:
          option = Option.objects.get(id=selected_option_id, question=q)
          answers[str(q.id)] = int(selected_option_id)
          if option.is_correct:
            score += 1
        except Option.DoesNotExist:
          # Invalid option, skip
          pass

    # Validate score doesn't exceed total questions
    total_questions = questions.count()
    if score > total_questions:
      score = total_questions

    # Save result with time taken and answers
    Result.objects.create(
      user=request.user,
      exam=exam,
      score=score,
      time_taken=time_taken,
      answers=answers
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
  questions = Question.objects.filter(exam=exam)

  # calculate percentage:
  total_questions = questions.count()
  percentage = result.get_percentage()

  # build review data
  review = []
  for q in questions:
    selected_option_id = result.answers.get(str(q.id))
    chosen_option = None
    if selected_option_id:
      try:
        chosen_option = Option.objects.get(id=selected_option_id)
      except Option.DoesNotExist:
        chosen_option = None

    correct_option = q.option_set.filter(is_correct=True).first()

    review.append({
      "question": q.text,
      "chosen_answer": chosen_option.text if chosen_option else "Not answered",
      "correct_answer": correct_option.text if correct_option else "N/A",
      "is_correct": chosen_option and chosen_option.is_correct if chosen_option else False,
    })

  return render(request, 'result.html', {
    'exam': exam,
    'result': result,
    'percentage': percentage,
    'review': review,
    'total_questions': total_questions
  })


@login_required
def dashboard(request):
  results = Result.objects.filter(user=request.user).order_by('-submitted_at')

  dashboard_data = []
  for r in results:
    total_questions = r.exam.question_set.count()
    percentage = r.get_percentage()

    dashboard_data.append({
      "exam_title": r.exam.title,
      "score": r.score,
      "total": total_questions,
      "percentage": percentage,
      "time_taken": r.time_taken,
      "date": r.submitted_at
    })

  return render(request, 'dashboard.html', {
    'dashboard_data': dashboard_data
  })
