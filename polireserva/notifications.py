
from django.core.mail import send_mail

send_mail(
    'Polireserva',
    'Fuck you son of a bitch.',
    'krlosbobadilla@gmail.com',
    ['sebasfranco92@gmail.com'],
    fail_silently=False,
)

''''# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open('Polireservas', 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

# me == the sender's email address
# you == the recipient's email address

me = 'krlosbobadilla@gmail.com'
you = 'sebasfranco92@gmail.com'
msg['Subject'] = 'Polireservas'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('krlosbobadilla@gmail.com', 587)
s.starttls()
s.login(me, "AVANTISEMPREAVANTI")
s.sendmail(me, you , msg.as_string())
s.quit()'''