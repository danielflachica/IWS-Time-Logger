# IWS-Time-Logger
A work contribution tracker and time logger for IWS

## How it Works
This work contribution tracker and time logger was designed to automate work shift summaries and reports. Whenever you start working on IWS-related projects, start the timer and end it once you're done. You'll then be presented with your work shift duration and a form where you can summarize the details of your work shift. By submitting the form, you'll notify IWS of your contributions via email; a copy of the said report will also be forwarded to your own email address.

## Dependencies
- `datetime`
- `email`
- `os`
- `PySimpleGUI` (Installation: `pip3 install PySimpleGUI`)
- `smtplib`
- `string`
- `sys`
- `time` 

## Installation
1. Install necessary dependencies.
1. Create a file called `credentials.txt` in the root directory.
1. Create a file called `recipients.txt` in the root directory and copy paste this on the first line: cyrus cyrus@imagineware.ph
1. Open `credentials.txt` and enter your credentials in the following format: `<first_name> <email> <password_for_email>`. (ex: john john.doe@gmail.com password123) Follow this format **strictly**.
2. Open `recipients.txt` and APPEND your details in the following format: `<first_name> <IWS_email>`. (ex: john john@imagineware.ph) DO NOT delete the first line (i.e. Cyrus' email details)
3. Click [this link](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Mr32TdVzceNvqvSTxRurTYBXU6mPTBNunG75FZUbH4WUFpWpUv37D9zgyKjkyEUTk7Oqe2-BaTq9Gj_2OyNfKS6iPNCQ) and login with the same email you specified in `credentials.txt`. 
4. In the resulting page, make sure that "Allow less secure apps" is switched to ON.
5. In the root directory, open `IWSTimeLogger.py`.
6. If your credentials have been set up properly, you'll be presented with the GUI. Otherwise, an error message prompting you to enter your credentials will display on the command line.

## Usage
1. Follow the installation steps above before using for the first time
1. Double click `IWSTimeLogger.py` (or run using your Python interpreter via command line)
2. Click "START" on the Timer window
3. Begin work on IWS Projects
4. If you need to take a break, click "PAUSE" on the Timer window. A new window will pop up. Once ready to resume, click "CONTINUE"
5. Once finsished, click "END" on the Timer window
6. A new Summary Report window will pop up showing your work session details
7. Type a summary of your contributions 
8. Click "Submit"
9. Check your email for a copy of the report

## Troubleshooting
- If, upon starting the app, it quits by itself, check your `credentials.txt` and enter your own details.
- If you click "Submit" after typing a summary report and it won't send, check your `credentials.txt` and ensure you've entered the correct email address and password combination.
- If that still doesn't work, make sure that your email service provider is Gmail. As of now, other domains are not yet supported.

## Limitations
- As of writing, the system has not been tested to the fullest extent yet, there might be a few bugs outside of its primary usage (i.e. timer feature and sending email reports).
- You have to manually specify recipients in a .txt file. [See also #8](https://github.com/danielflachica/IWS-Time-Logger/issues/8).
- No checking of valid domains before sending emails, the app just quits. [See also #7](https://github.com/danielflachica/IWS-Time-Logger/issues/7).
- Timer doesn't display how much time has passed since you clicked "start". [See also #3](https://github.com/danielflachica/IWS-Time-Logger/issues/3).
- No support for bulleted summary reports, only plain text for now. [See also #4](https://github.com/danielflachica/IWS-Time-Logger/issues/4).
- No support for email service providers other than Gmail. [See also #6](https://github.com/danielflachica/IWS-Time-Logger/issues/6).
