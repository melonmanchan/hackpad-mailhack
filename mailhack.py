#!usr/bin/env python
# Hack for sending Hackpad invitatiol emails

import StringIO
import csv
import json
import sendgrid
import subprocess
import time

with open('config.json') as data_file:
    config = json.load(data_file)

sendgridclient = sendgrid.SendGridClient(config['sendgrid_key'])

def send_mail(toMail, token):
    verificationlink = config['hackpad_url'] + '/ep/account/validate-email?email=' + toMail + '&token=' + token

    message = sendgrid.Mail(to=toMail, subject='Verifying your Hackpad account',
                            html='Your verification link is <a href="{}">{}</a> . Happy hacking!'.format(verificationlink, verificationlink),
                            from_email= config['from_mail'])
    status, resp = sendgridclient.send(message)
    print status
    print resp

def main():
    while True:
        mailfile = open('already_sent.txt', 'ab+')
        filecontents = mailfile.read().splitlines()
        cmdoutput = subprocess.check_output("docker exec -i " + config['container_name'] + " mysql  --batch  hackpad -e 'select email, token from email_signup;'", shell=True)
        f = StringIO.StringIO(cmdoutput)
        outputlist = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, delimiter='\t')]

        for i, val in enumerate(outputlist):
            email = val['email']
            token = val['token']

            if not email in filecontents:
                print 'inviting person ' + email
                send_mail(email, token)

                print 'appending... ' + email
                mailfile.write(email + '\n')

        mailfile.close()
        time.sleep(10)

if __name__ == '__main__':
    main()
