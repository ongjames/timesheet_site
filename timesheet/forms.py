from django import forms
from timesheet.models import Time


class EntryForm(forms.ModelForm):
    title = forms.CharField(max_length=30)
    hours = forms.IntegerField(min_value=1,max_value=23)
    hours.widget = forms.NumberInput(attrs={'title':'Numbers 1-23','min':1,'max':23})
    date = forms.DateField()
    date.widget = forms.DateInput(attrs={'title':'Format: yyyy-mm-dd'})
    comments = forms.CharField(max_length=128,required=False)
    comments.widget = forms.Textarea(attrs={'title':'Optional','rows':3})

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Time
        fields = ('title','hours','date','comments',)