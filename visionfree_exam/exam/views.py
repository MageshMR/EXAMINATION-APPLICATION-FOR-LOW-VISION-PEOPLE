from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, StudentAnswer
from .forms import QuestionForm
import speech_recognition as sr
from gtts import gTTS
import os

def index(request):
    return render(request, 'exam/index.html')

#def admin_dashboard(request):
 #   questions = Question.objects.all()
  #  return render(request, 'exam/admin_dashboard.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'exam/add_question.html', {'form': form})

def text_to_speech(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    tts = gTTS(text=question.text, lang='en')
    audio_path = f'media/questions/question_{question_id}.mp3'
    tts.save(audio_path)
    return JsonResponse({'audio_url': audio_path})

def speech_to_text(request):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return JsonResponse({'answer_text': text})
    except sr.UnknownValueError:
        return JsonResponse({'error': 'Could not understand the audio'})
    except sr.RequestError:
        return JsonResponse({'error': 'Speech recognition service is unavailable'})

def submit_answer(request, question_id):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        answer_text = request.POST['answer_text']
        question = get_object_or_404(Question, id=question_id)
        StudentAnswer.objects.create(student_name=student_name, question=question, answer_text=answer_text)
        return JsonResponse({'message': 'Answer submitted successfully'})

def student_exam(request):
    questions = Question.objects.all()  # Fetch all questions
    return render(request, 'student_exam.html', {'questions': questions}) 
    


from django.shortcuts import render

def student_profile(request):
    student_data = {
        "name": "John Doe",
        "reg_no": "123456",
        "course": "B.A. English",
        "year": "Final Year",
        "email": "john@example.com",
    }
    return render(request, "exam/student_profile.html", {"student": student_data})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'exam/admin_login.html', {'error': 'Invalid credentials!'})
    return render(request, 'exam/admin_login.html')

@login_required
def admin_dashboard(request):
    questions = Question.objects.all()
    return render(request, 'exam/admin_dashboard.html', {'questions': questions})

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Answer  # Adjust based on your model location

def export_answers_pdf(request):
    answers = Answer.objects.all()
    template_path = 'exam/answers_pdf_template.html'
    context = {'answers': answers}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="submitted_answers.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response




 # voice register

# exam/views.py







from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm

def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Update this to your admin dashboard name if needed
    else:
        form = QuestionForm(instance=question)
    return render(request, 'exam/edit_question.html', {'form': form})



def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('admin_dashboard')  # Replace with actual dashboard name





