from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class StatisticsForm(ModelForm):
    class Meta:
        source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        model = Statistics
        fields =  ( 'date', 'acw', 'aht', 'call', 'ticket', 'employee', 'id')
        labels = {
            'date': ('Date'),
            'acw': ('ACW Avg'),
            'aht': ('AHT Avg'),
            'call': ('Calls Received'),
            'ticket': ('Tickets Created'),
        }
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'employee': forms.HiddenInput(),
            'id': forms.HiddenInput(),
            'acw': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'aht': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'call': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ticket': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        
        def clean(self):
            cleaned_data = super(StatisticsForm, self).clean()
            date = cleaned_data.get('date')
            acw = cleaned_data.get('acw')
            aht = cleaned_data.get('aht')
            call = cleaned_data.get('call')
            ticket = cleaned_data.get('ticket')
            if not date and not acw and not aht and not call and not ticket:
                raise forms.ValidationError('You forgot something!')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class EmployeeForm(ModelForm):
    class Meta:
        source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        model = Employee
        fields =  ('first_name', 'last_name', 'mobile', 'email', 'hire_date', 
                    'birthdate', 'ext', 'avaya_login', 'role', 'team')
        labels = {
            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'mobile': ('Phone #'),
            'email': ('Email'),
            'hire_date': ('Hire Date'),
            'birthdate': ('Birthday'),
            'ext': ('Phone Ext'),
            'avaya_login': ('Phone Login'),
            'role': ('Role'),
            'team': ('Team'),
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        
        def clean(self):
            cleaned_data = super(EmployeeForm, self).clean()
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
    
class QA_ScoreForm(ModelForm):
    class Meta:
        source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        model = QA_Score
        fields =  ('qa_date', 'qa_score', 'qa_ticket', 'qa_comment', 'employee', 'id')
        labels = {
            'qa_date': ('Date'),
            'qa_score': ('Score'),
            'qa_ticket': ('Ticket #'),
            'qa_comment': ('Remarks'),
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'id': forms.HiddenInput(),
            'qa_date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'qa_score': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'qa_ticket': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'qa_comment': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

        def clean(self):
            cleaned_data = super(QA_ScoreForm, self).clean()
            qa_date = cleaned_data.get('qa_date')
            qa_score = cleaned_data.get('qa_score')
            qa_ticket = cleaned_data.get('qa_ticket')
            qa_comment = cleaned_data.get('qa_comment')
            if not qa_date and not qa_score:
                raise forms.ValidationError('You forgot a score!')

class TimeStatsForm(ModelForm):
    class Meta:
        source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        model = TimeStats
        fields =  ('time_date', 'pto', 'lateArrival', 'earlyDepart', 'employee', 'id')
        labels = {
            'time_date': ('Date'),
            'pto': ('PTO'),
            'lateArrival': ('Late Arrivals'),
            'earlyDepart': ('Early Departures'),
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'id': forms.HiddenInput(),
            'time_date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'pto': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lateArrival': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'earlyDepart': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

        def clean(self):
            cleaned_data = super(TimeStatsForm, self).clean()
            time_date = cleaned_data.get('time_date')
            pto = cleaned_data.get('pto')
            lateArrival = cleaned_data.get('lateArrival')
            earlyDepart = cleaned_data.get('earlyDepart')

class UpdateForms(ModelForm):
    class Meta:
        source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        model = Updates
        fields =  ('update_date', 'important', 'update', 'id')
        labels = {
            'update_date': ('Date'),
            'update': ('Update'),
            'important': ('Important?'),
        }
        CHOICES = [('Y','Yes'),('N','No')]
        widgets = {
            'id': forms.HiddenInput(),
            'update_date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'update': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'important': forms.RadioSelect(
                choices=CHOICES,
            ),
        }

        def clean(self):
            cleaned_data = super(UpdateForms, self).clean()
            update_date = cleaned_data.get('update_date')
            update = cleaned_data.get('update')
            important = cleaned_data.get('important')