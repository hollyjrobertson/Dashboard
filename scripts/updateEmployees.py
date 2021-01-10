import csv
import io
import datetime
import random
from django.contrib.auth.models import User
from dashboard.models import Employee, Statistics, QA_Score, TimeStats, Updates
from django.db import IntegrityError

def importStatisticsFile(file):
    # Import data
    result = formatStatisticsFile(file)
    
    # Return result of import
    return result

def formatStatisticsFile(file):
    result = ''
    io_string = io.StringIO(file) 
    Statistics.objects.all().delete()
    i = 0
    for stat in csv.DictReader(io_string, delimiter='\t'):
        date = stat['Date'] 
        if (date != 'Date'):
            employee = findEmployee(stat['Agent Name'])
            if (employee != ''):
                aht = int(float(stat['AHT (Seconds)']))
                acw = int(float(stat['ACW Time']))
                calls = int(stat['ACD Calls']) + int(stat['ACW Out Calls'])
                aux_time = stat['AUX Time']
                staffed_time = stat['Staffed Time']
                acw_total = stat['Total ACW Time']
                avail_time = stat['Avail Time']
                staffed_time = stat['Staffed Time']
                try:
                    s, created = Statistics.objects.get_or_create(
                        employee = employee,
                        date = datetime.datetime.strptime(date, '%m/%d/%Y').date(),
                        acw = acw,
                        aht = aht, 
                        call = calls,
                        ticket = calls-1, 
                        aux_total = aux_time,
                        staffed_time = staffed_time,
                        acw_total = acw_total,
                        avail_time = avail_time,
                    )
                    # If object wasn't in db
                    if created:
                        s.save()
                        i += 1
                        after_creation_msg = 'Added '+  str(i) + ' Statistics'
                        result = after_creation_msg
                # If object was in db (specialist and date constraint failed)
                except Exception as e:
                    result = ("Error in Statistic update: " + str(e) + "with: " + file)
        else:
            continue
    
    return result  
            
def importEmployeeFile(file):
    # Import data
    result = formatEmployeeFile(file)
    
    # Return result of import
    return result

def formatEmployeeFile(file):
    result = ''
    io_string = io.StringIO(file)
    pre_delete_size = len(Employee.objects.all())
    Employee.objects.all().delete()
    # Create an object and db entry for each row in File
    for employee in csv.DictReader(io_string):
        try:
            s, created = Employee.objects.get_or_create(
                employee_id=employee['Employee ID'],
                role=employee['Role'],
                team=employee['Team'],
                first_name=employee['First Name'],
                last_name=employee['Last Name'],
                email=employee['Email'],
                mobile=employee['Mobile'],
                ext=employee['Ext'],
                avaya_login=employee['Login'],
                user=findUser(employee['Email']),
                hire_date=datetime.datetime.strptime(employee['Hire Date'], '%m/%d/%Y'),
                birthdate=datetime.datetime.strptime(employee['Birthdate'], '%m/%d/%Y'),
            )
            # If object wasn't in db
            if created:
                s.save()
                after_creation_size = len(Employee.objects.all())
                result = 'Deleted ' + str(pre_delete_size) + ' Employees\n' + str(after_creation_size) + ' Employees Created'
        # if Object was in db (employee_id constraint failed)
        except IntegrityError:
            # Go onto next row in File
            pass
        except Exception as e:
            result = ("Error in Employee update: ",  employee, ' Error:', str(e), " in file: " , file)
    return result

def findUser(email):
    try:
        user = User.objects.get(email=email)
        if user is not None:
            return user
        else:
            return 
    except User.DoesNotExist:
        return
    except Exception as e:
        print("Error in Finding User in Employee Creation", email, str(e))
def findEmployee(employee):
    last_name = employee.split(",")[0]
    employee = ''
    try:
        employee = Employee.objects.get(last_name=last_name)
    except Employee.DoesNotExist:
        employee = Employee.objects.get(last_name__contains=last_name)
    except Exception as e:
        print("Error in Finding Employee: " + str(e) + " with: " + str(employee))
    
    return employee 

def getTickets():
    return random.randint(0, 30)
def run(): 
    # Commands to run when python manage.py runscript updateSpecialists is called
    return "Hello"