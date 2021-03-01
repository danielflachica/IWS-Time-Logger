from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import PySimpleGUI as sg
import smtplib
from string import Template
import sys
import time

# Function to read the user's credential file
def get_credentials(filename):
    name, email, password = None, None, None
    with open(filename, mode='r', encoding='utf-8') as credentials_file:
        for line in credentials_file: 
            name = line.split()[0]  
            email = line.split()[1]
            password = line.split()[2]
    return name, email, password

# Function to read the contacts from a given recipients file and return a list of names and email addresses
def get_recipients(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    return names, emails

# Function to return a Template object made from message tempalte file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# Function to return string-formatted time, given input from time.time()
def format_time(time):
    hours, rem = divmod(time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:02.0f}".format(int(hours),int(minutes),seconds)

MY_NAME, MY_ADDRESS, PASSWORD = get_credentials('credentials.txt')


if __name__ == "__main__":
    # check if credentials are set up
    if MY_NAME is None or MY_ADDRESS is None or PASSWORD is None:
        print('Please set up your credentials file before proceeding.')
        print('Format: <first_name> <email> <password>', end="\n\n")
        input("Press Enter to quit...")
        sys.exit()
    else:
        print("Credentials loaded successfully.", end="\n\n")
        print("User:", MY_NAME.title())
        print("Email:", MY_ADDRESS)
        print("Password:", '*'*len(PASSWORD))

    # set up the SMTP server for Gmail
    s = smtplib.SMTP(host='smtp.gmail.com', port='587')
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # fetch recipient info and read message template
    names, emails = get_recipients('recipients.txt')
    message_template = read_template('summary_report_template.txt')

    # create the window
    layout = [
        [sg.Text("IWS Time Logger", font=("Helvetica", 12, "bold"))],
        # [sg.Text("0.0s", key='time_display', font=("Helvetica", 16))],
        [sg.Button("START", font=("Helvetica", 10))],
        [sg.Button("PAUSE", font=("Helvetica", 10))],
        [sg.Button("END", enable_events=False, font=("Helvetica", 10))]
    ]
    window = sg.Window("IWS Time Logger", layout)

    sg.change_look_and_feel('Dark Blue 3')
    sg.theme('DarkAmber')

    # create event loop
    while True:
        # start event loop
        event, values = window.read()

        # end program if user closes window
        if event == sg.WIN_CLOSED:
            break

        # disable end button
        # window.FindElement('END').Update(disabled=True)

        if event == "START":
            t0 = time.time()    # for timing elapsed time
            t_start = datetime.now().strftime("%m/%d/%Y %H:%M:%S")   # for logging time started
            window.FindElement('START').Update(disabled=True)
            window.FindElement('PAUSE').Update(disabled=False)
            window.FindElement('END').Update(disabled=False)

        if event == "PAUSE":
            # disable buttons
            window.FindElement('PAUSE').Update(disabled=True)
            window.FindElement('END').Update(disabled=True)

            # start timing the "break"
            tP = time.time()

            # create new temporary pause window
            pause_layout = [
                [sg.Text("Timer paused", font=("Helvetica", 10))],
                [sg.Button("CONTINUE")]
            ]

            pause_window = sg.Window("IWS Time Logger", pause_layout)
            pause_event, pause_values = pause_window.read()

            if pause_event == sg.WIN_CLOSED:
                pause_event.close()
                break
            
            if pause_event == "CONTINUE":
                # enable buttons
                window.FindElement('PAUSE').Update(disabled=False)
                window.FindElement('END').Update(disabled=False)

                # stop timing the "break"
                tP = time.time() - tP

                # write pause time to file
                with open('pause.txt', 'a') as f:
                    f.write(str(tP)+'\n')

                # close window
                pause_window.close()

        if event == "END":
            # compute elapsed time
            tN = time.time()    # for timing elapsed time
            t_end = datetime.now().strftime("%m/%d/%Y %H:%M:%S")   # for logging time started
            elapsed_time = tN - t0

            # compute paused time, if any
            paused_time = 0
            try:
                f = open("pause.txt", 'r')
                lines = f.readlines()
                for line in lines:
                    paused_time = paused_time + float(line.strip())
                f.close()
            except IOError:
                pass    # proceed with rest of code execution

            # compute total work duration
            total_time = elapsed_time - paused_time
            
            # format time variables
            elapsed_time = format_time(elapsed_time)
            paused_time = format_time(paused_time)
            total_time = format_time(total_time)

            # disable/enable necessary buttons
            window.FindElement('START').Update(disabled=False)
            window.FindElement('PAUSE').Update(disabled=True)
            window.FindElement('END').Update(disabled=True)

            # delete pause.txt, if exists
            if os.path.exists('pause.txt'):
                os.remove('pause.txt')

            # create new summary report window
            summary_layout = [
                [sg.Text("Time Started: " + t_start, font=("Helvetica", 10))],
                [sg.Text("Time Ended: " + t_end, font=("Helvetica", 10))],
                [sg.Text("Elapsed Time: " + elapsed_time, font=("Helvetica", 10))],
                [sg.Text("Time Paused: " + paused_time, font=("Helvetica", 10))],
                [sg.Text("Work Duration: " + total_time, font=("Helvetica", 10, "bold"))],
                [sg.Text("")],
                [sg.Text("Please enter a summary of the work done during your shift.", font=("Helvetica", 10))],
                [sg.Text("A copy of your response will be sent to cyrus@imagineware.ph", font=("Helvetica", 10, "italic"))],
                [sg.Multiline(size=(60, 10), key='content', font=("Helvetica", 10))],
                [sg.Submit(font=("Helvetica", 10, "bold")), sg.Cancel(font=("Helvetica", 10))]
            ]

            summary_window = sg.Window("Summary Report", summary_layout)

            summary_event, summary_values = summary_window.read()
            
            if summary_event == sg.WIN_CLOSED:
                summary_window.close()
                break

            if summary_event == "Submit":
                summary_report = summary_values['content']
                # print(summary_report)

                # for each recipient, send email
                for name, email in zip(names, emails):
                    msg = MIMEMultipart() # create a message

                    # update variables from message template
                    message = message_template.substitute(
                        DATE=datetime.date(datetime.now()).strftime("%b %d, %Y"),
                        COMPANY_HEAD="Cyrus",
                        START_TIME=t_start,
                        END_TIME=t_end,
                        ELAPSED_TIME=elapsed_time,
                        PAUSED_TIME=paused_time,
                        TOTAL_TIME=total_time,
                        SUMMARY=summary_report,
                        USER_NAME=MY_NAME.title()
                    )

                    # set up parameters of message
                    msg['From'] = MY_ADDRESS
                    msg['To'] = email
                    msg['Subject'] = 'IWS Work Summary Report for ' + datetime.date(datetime.now()).strftime('%m/%d/%Y') + " [" + name.title() + "'s copy]"

                    # add message body
                    msg.attach(MIMEText(message, 'html'))

                    # send message via server
                    s.send_message(msg)
                    # print('Email successfully sent to', email)

                    # delete message
                    del msg

                summary_window.close()
                break

            if summary_event == "Cancel":
                summary_window.close()

    window.close()
