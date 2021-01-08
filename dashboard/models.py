from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, date
from django.core.validators import RegexValidator
class Employee(models.Model):
    ROLE_CHOICES = [
        ('S', 'Specialist'),
        ('A', 'Analyst'),
        ('L', 'Leader'),
    ]
    
    TEAM_CHOICES = [
        ('IT', 'Information Technology'),
        ('CC', 'Call Center'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    mobile_regex = RegexValidator(regex=r'\d{3}-\d{3}-\d{4}', message="Phone number must be entered in the format: '999-999-9999'. Up to 12 digits allowed.")
    mobile = models.CharField(validators=[mobile_regex], max_length=12, blank=True) 
    email_regex = RegexValidator(regex=r'.{1,}@[^.]{1,}', message="Email must be entered in the format: 'email@domain.com'. At least 5-50 characters allowed. ")
    email = models.CharField(validators=[email_regex], max_length=50, blank=True) 
    hire_date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    birthdate = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)
    avaya_login = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    team = models.CharField(max_length=2, choices=TEAM_CHOICES, default=TEAM_CHOICES[0][0])

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('first_name', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['team']
        verbose_name_plural = 'Employees'

class Statistics(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.now, null=True, blank=True)
    acw = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    acw_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aht = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    call = models.IntegerField(null=True, blank=True)
    ticket = models.IntegerField(null=True, blank=True)
    aux_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avail_time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    staffed_time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return '%s: Date: %s ACW: %s AHT: %s Calls Taken: %s Tickets Made: %s' % (self.employee, self.date, self.acw, self.aht, self.call, self.ticket)
    
    class Meta:
        ordering = ['employee']
        verbose_name_plural = 'Statistics'
        unique_together = (('employee', 'date'),)

class QA_Score(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    qa_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.now, null=True, blank=True)
    qa_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    qa_ticket = models.CharField(max_length=100, null=True, blank=True)
    qa_comment = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '%s: Date: %s Score: %s Ticket: %s Comments: %s' % (self.employee, self.qa_date, self.qa_score, self.qa_ticket, self.qa_comment)

    class Meta:
        verbose_name = 'QA Score'
        verbose_name_plural = 'QA Scores'
        unique_together = (('employee', 'qa_ticket'),)

class TimeStats(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.now, null=True, blank=True)
    pto = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lateArrival = models.IntegerField(null=True, blank=True)
    earlyDepart = models.IntegerField(null=True, blank=True)
    
class Updates(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    update_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.now, null=True, blank=True)
    important = models.BooleanField(default=False, null=True, blank=True)
    update = models.TextField(max_length=500, null=True, blank=True)

def __str__(self):
    return 'Date: %s Update: %s' % (self.update_date, self.update)

