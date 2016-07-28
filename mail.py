import smtplib
from email.mime.text import MIMEText

me='jose@che'
you='manuel.buil@ericsson.com'
msg=MIMEText("te llega esto?")
msg['Subject'] = 'cheeee'
msg['From'] = me
msg['To'] = you

# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())
s.quit()
