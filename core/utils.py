from django.core.mail import send_mail

# Send a test email
def send_mail_to_console():
    send_mail(
        'Subject here',           # Email Subject
        'Here is the message.',    # Email Body
        'from@example.com',       # From Email (this can be any email you want to use)
        ['to@example.com'],       # To Email (recipient)
        fail_silently=False,      # If False, raise an error if sending fails
    )
