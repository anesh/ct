import smtplib
from email.mime.text import MIMEText

with open('textfile', 'rb') as fp:
    msg = MIMEText(fp.read(),'html', 'utf-8')

recipients = ['']

msg['Subject'] = 'F5 UCS backup job completed'
msg['From'] = 'netdevops@cantire.com'
msg['To'] = ", ".join(recipients)

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('')
s.sendmail(msg['From'],recipients, msg.as_string())
s.quit()

