from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Assistant(models.Model):
    name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120, default="Blauwe Ogen")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    query_count = models.PositiveIntegerField(default=0)
    files = models.FileField(upload_to='assistant_files/', null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.name
    
    def increment_query_count(self):
        self.query_count += 1
        self.save()
    
    
class Chat(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True)
    _input = models.TextField()
    _output = models.TextField()
    
    class Meta:
        db_table = "t_chat"
    

class CodeExplainer(models.Model):
    _input = models.TextField()
    _output = models.TextField()
    
    class Meta:
        db_table = "t_code_explainer"

class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.uploaded_on.date()
    