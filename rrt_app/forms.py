from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['component', 'description', 'troubleshooting', 'action_plan', 'error_message', 'spare_part', 'advisory', 'log_below_gen8', 'log_above_gen8',]
        widgets = {
            'component': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'troubleshooting': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'action_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'log_below_gen8': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'log_above_gen8': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'error_message': forms.Textarea(attrs={'class': 'form-control'}),
            'spare_part': forms.Textarea(attrs={'class': 'form-control'}),
            'advisory': forms.Textarea(attrs={'class': 'form-control'}),
        }
