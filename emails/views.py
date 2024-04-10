from django.shortcuts import render, redirect
from .models import *
from .forms import EmailForm
from django.contrib import messages
from .tasks import send_email_task
from dataentry.utils import send_email_notification

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # Send an email
            mail_subject = request.POST["subject"]
            message = request.POST['body']
            email_list = request.POST['email_list']

            # Access the selected email list
            email_list = email.email_list

            # Extract email addresses from the Subscriber model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subscribers]

            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id

            #send without celery
            send_email_notification(
                mail_subject, message, to_email, attachment, email_id
            )
            # Handover email sending task to celery
            #send_email_task.delay(mail_subject, message, to_email, attachment, email_id)

            # Display a success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
    else:
        email = EmailForm()
        context = {
            'email_form': email,}
    return render(request, "emails/send-email.html", context)
