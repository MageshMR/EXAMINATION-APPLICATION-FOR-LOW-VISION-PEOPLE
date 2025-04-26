from django.urls import path
from . import views
from .views import view_answers
from .views import submit_answer
from exam.views import student_profile
from exam import views as exam_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('tts/<int:question_id>/', views.text_to_speech, name='text_to_speech'),
    path('stt/', views.speech_to_text, name='speech_to_text'),
    path('submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('view_answers/', view_answers, name='view_answers'),
    path('submit/', submit_answer, name='submit_answer'),
    path('profile/', student_profile, name='profile'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    

]


from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('voice_login/', views.voice_login, name='voice_login'),
]





