from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Source(models.Model):
    
    name = models.CharField(max_length=200)
    
    class Meta:
        unique_together = ['name']
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def quote_count(self):
        return self.quote_set.count()
    
class QuoteItem(models.Model):
    quote = models.CharField(max_length=200)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['quote', 'source']
    
    def __str__(self):
        max_length = 50
        if len(self.quote) >= max_length:
            quote = self.quote[:max_length-3] + "..."
        
        else:
            quote = self.quote

        return f"{quote} - {self.source}"
    
    def clean(self):
        if self.quote[-1] not in '.?!':
            self.quote += '.'
            
        if self.pk is None:
            if QuoteItem.objects.filter(source=self.source).count() >= 3:
                raise ValidationError("У одного источника не может быть более 3 цитат")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def rating(self):
        return self.likes - self.dislikes
