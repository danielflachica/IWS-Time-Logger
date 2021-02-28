from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
            t0 = time.time()
            window.FindElement('START').Update(disabled=True)
            window.FindElement('END').Update(disabled=False)

        if event == "END":
            tN = time.time()
            elapsed_time = tN - t0

            # format elapsed time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            # print("Elapsed time:", elapsed_time)
            elapsed_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

            window.FindElement('START').Update(disabled=False)
            window.FindElement('END').Update(disabled=True)

            # Create new summary report window
            summary_layout = [
                [sg.Text("Elapsed Time: " + elapsed_time, font=("Helvetica", 10))],
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
                        ELAPSED_TIME=elapsed_time,
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
