from automation.celery import app
from django.conf import settings
# from dataentry.tasks import celery_test_task
from django.core.management import call_command
from .utils import send_email_notification, generate_csv_file


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command("importdata", file_path, model_name)

    except Exception as e:
        raise e

    mail_subject = "Import Data Completed"
    message = "Your data import has been successful"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    
    return "Data imported successfully"


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e

    file_path = generate_csv_file(model_name)
    
    mail_subject = "Export Data Successful"
    message = "Export data successful. Please find the attachment"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email, attachment=file_path)
    return "Export Data task executed successfully."