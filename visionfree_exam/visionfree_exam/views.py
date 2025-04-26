from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, StudentAnswer
from .forms import QuestionForm
import speech_recognition as sr
from gtts import gTTS
import os
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Answer



def index(request):
    return render(request, 'exam/index.html')

# def admin_dashboard(request):
#     questions = Question.objects.all()
#     return render(request, 'exam/admin_dashboard.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'exam/add_question.html', {'form': form})

import os
from django.conf import settings
from gtts import gTTS
from .models import Question
from django.http import JsonResponse

def text_to_speech(request, question_id):
    question = Question.objects.get(id=question_id)
    
    # Define the path where the file should be saved
    media_root = settings.MEDIA_ROOT
    audio_dir = os.path.join(media_root, 'questions')
    audio_path = os.path.join(audio_dir, f'question_{question.id}.mp3')

    # Create the 'questions' directory if it doesn't exist
    os.makedirs(audio_dir, exist_ok=True)

    # Generate the speech file
    tts = gTTS(text=question.text, lang='en')
    tts.save(audio_path)  # Save the audio file

    # Return the audio file path
    return JsonResponse({'audio_url': f'/media/questions/question_{question.id}.mp3'})


@csrf_exempt  # Disable CSRF for testing
def speech_to_text(request):
    if request.method == "POST":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)  # Convert speech to text
                print("Recognized Speech:", text)
                return JsonResponse({"answer_text": text})  # Return recognized text
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand audio"}, status=400)
            except sr.RequestError:
                return JsonResponse({"error": "Speech Recognition service unavailable"}, status=500)
    
    return JsonResponse({"error": "Invalid request method!"}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Answer, Question

@csrf_exempt
def submit_answer(request, question_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Parse JSON data
            
            student_name = data.get("student_name")  # Extract fields
            answer_text = data.get("answer_text")

            if not student_name or not answer_text:
                return JsonResponse({"error": "Missing required fields!"}, status=400)

            # Ensure the question exists
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return JsonResponse({"error": "Question not found"}, status=404)

            # Save the answer
            Answer.objects.create(
                question=question, 
                student_name=student_name, 
                answer_text=answer_text
            )

            return JsonResponse({"message": "Answer submitted successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"error": "Invalid request method!"}, status=405)

def student_exam(request):
    questions = Question.objects.all()  # Fetch all questions
    return render(request, 'visionfree_exam/student_exam.html', {'questions': questions}) 

def view_answers(request):
    answers = Answer.objects.all()  # Fetch all answers
    return render(request, 'exam/view_answers.html', {'answers': answers})




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












from django.http import JsonResponse, Http404
from .models import Question

def get_question_json(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        return JsonResponse({
            'id': question.id,
            'text': question.text,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
        })
    except Question.DoesNotExist:
        raise Http404("Question not found")





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











from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_logout(request):
    logout(request)
    return redirect('index')  # Replace 'index' with your home page URL name


