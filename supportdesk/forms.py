from django import forms
from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['summary', 'description', 'is_high_priority']
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Unable to login to application'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'is_high_priority': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }


#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['summary'].label = 'Summary'
#        self.fields['description'].label = 'Description'
#        self.fields['is_high_priority'].label = 'High priority'
#        self.fields['is_high_priority'].required = False
