#########################################################################################################
#
# Author:         Diego Montufar
# Date:           Apr/2015
# Name:           emailer.py
# Description:    Sends email notifications from/to the configured email accounts in the settings.py file
#
#
#########################################################################################################

import smtplib
import settings


def sendEmail(message,from_addr=settings.from_address, to_addr_list=[settings.to_address], 
              subject=settings.def_subject,
              login=settings.from_address, password=settings.from_password,
              smtpserver=settings.smtp_server, port=settings.smtp_port):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver,port)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems