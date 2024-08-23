from django.db import models

from django.db import models

class LegalDocument(models.Model):
    title = models.CharField(max_length=455)
    content = models.TextField()
    court = models.CharField(max_length=200)
    case_number = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.title
    

class CaseOutcome(models.Model):
    case = models.ForeignKey(LegalDocument, on_delete=models.CASCADE)
    predicted_outcome = models.TextField()
    actual_outcome = models.TextField()

    def __str__(self):
        return str(self.predicted_outcome)[:100]
    
