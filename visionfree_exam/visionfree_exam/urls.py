from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import view_answers
from .views import submit_answer
from exam.views import student_profile
from .views import export_answers_pdf
from exam import views as exam_views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('tts/<int:question_id>/', views.text_to_speech, name='text_to_speech'),
    path('stt/', views.speech_to_text, name='speech_to_text'),
    path('submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('student_exam/', views.student_exam, name='student_exam'),  # <-- ADD THIS LINE
    path('view_answers/', view_answers, name='view_answers'),
    path('submit/', submit_answer, name='submit_answer'),
    path('profile/', student_profile, name='profile'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export_answers_pdf/', export_answers_pdf, name='export_answers_pdf'),
    path('api/question/<int:question_id>/', views.get_question_json, name='get_question_json'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('logout/', views.admin_logout, name='admin_logout'),

   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









