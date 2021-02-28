# IWS-Time-Logger
A work contribution tracker and time logger for IWS

## How it Works
This work contribution tracker and time logger was designed to automate work shift summaries and reports. Whenever you start working on IWS-related projects, start the timer and end it once you're done. You'll then be presented with your work shift duration and a form where you can summarize the details of your work shift. By submitting the form, you'll notify IWS of your contributions via email; a copy of the said report will also be forwarded to your own email address.

## Installation
1. Open `credentials.txt` and enter your credentials in the following format: `<first_name> <email> <password_for_email>`. Follow this format **strictly**.
2. Open `recipients.txt` and APPEND your details in the following format: `<first_name> <IWS_email>`. DO NOT delete the first line (i.e. Cyrus' email details)
3. Click [this link](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Mr32TdVzceNvqvSTxRurTYBXU6mPTBNunG75FZUbH4WUFpWpUv37D9zgyKjkyEUTk7Oqe2-BaTq9Gj_2OyNfKS6iPNCQ) and login with the same email you specified in `credentials.txt`. 
4. In the resulting page, make sure that "Allow less secure apps" is switched to ON.
5. In the root directory, open `IWSTimeLogger.py`.
6. If your credentials have been set up properly, you'll be presented with the GUI. Otherwise, an error message prompting you to enter your credentials will display on the command line.

## Usage
1. Follow the installation steps above before using for the first time
1. Double click `IWSTimeLogger.py`
2. Click "START"
3. Begin work on IWS Projects
4. Once finsished, click "END" on the Timer window
5. Type a summary of your contributions 
6. Click "Submit"
7. Check your email for a copy of the report

## Troubleshooting
- If you click "Submit" after typing a summary report and it won't send, check your `credentials.txt` and ensure you've entered the correct email address and password combination.
- If that still doesn't work, make sure that your email service provider is Gmail. As of now, other domains are not yet supported.

## Limitations
- As of writing, the system has not been tested to the fullest extent yet, there might be a few bugs outside of its primary usage (i.e. timer feature and sending email reports)
- You have to manually specify recipients in a .txt file
- No checking of valid domains before sending emails
- Timer doesn't display how much time has passed since you clicked "start"
- No support for bulleted summary reports, only plain text for now
