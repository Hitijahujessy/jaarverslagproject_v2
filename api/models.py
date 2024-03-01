from django.db import models

class Assistant(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    query_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def increment_query_count(self):
        self.query_count += 1
        self.save()
    
    
class Chat(models.Model):
    _input = models.TextField()
    _output = models.TextField()
    
    class Meta:
        db_table = "t_chat"
    

class CodeExplainer(models.Model):
    _input = models.TextField()
    _output = models.TextField()
    
    class Meta:
        db_table = "t_code_explainer"