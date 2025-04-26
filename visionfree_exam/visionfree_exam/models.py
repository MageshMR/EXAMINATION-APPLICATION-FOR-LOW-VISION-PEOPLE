
from django.db import models

#class Question(models.Model):
#    text = models.TextField()
#    audio_file = models.FileField(upload_to='questions/', blank=True, null=True)

class Question(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='questions/', blank=True, null=True)

    option_a = models.CharField(max_length=255, default="Option A")
    option_b = models.CharField(max_length=255, default="Option B")
    option_c = models.CharField(max_length=255, default="Option C")
    option_d = models.CharField(max_length=255, default="Option D")
    
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        default='A'
    )


    def __str__(self):
        return self.text

class StudentAnswer(models.Model):
    student_name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

   
        
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # ✅ Ensure this exists
    student_name = models.CharField(max_length=255)
    answer_text = models.TextField()



class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)



