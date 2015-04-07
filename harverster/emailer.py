import smtplib
import settings


def sendEmail(message,from_addr=settings.from_address, to_addr_list=[settings.to_address], 
              subject=settings.def_subject,
              login=settings.from_address, password=settings.from_password,
              smtpserver=settings.smtp_server, port=settings.smtp_port):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    #header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver,port)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems