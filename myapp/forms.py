from django import forms
from .models import QuoteItem, Source

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["name"]
        
class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteItem
        fields = ['quote', 'source', 'weight']
        widgets = {
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'source': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.all().order_by('name')