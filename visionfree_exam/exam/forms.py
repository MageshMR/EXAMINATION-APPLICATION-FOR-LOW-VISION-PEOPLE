from django import forms
from .models import Question

#class QuestionForm(forms.ModelForm):
#    class Meta:
#        model = Question
#        fields = ['text', 'audio_file']

from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Question

from django import forms
from .models import Question

from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'audio_file', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
