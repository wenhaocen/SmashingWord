import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText


def rp():
		email = "cenwenhao@hotmail.com"
		password = "123"
		msg = MIMEText("Dear Smashing Word User, your password is " + password+" . Enjoy")

		# me == the sender's email address
		# you == the recipient's email address
		msg['Subject'] = 'Password Recovery'
		msg['From'] = 'wenhaocen@gmail.com'
		msg['To'] = email

		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP('pop.gmail.com')
		s.sendmail('wenhaocen@gmail.com', [email], msg.as_string())
		s.quit()
		return 1
