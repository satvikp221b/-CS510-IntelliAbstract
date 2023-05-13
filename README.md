# -CS510-IntelliAbstract
## 1. Adding the Chrome Extension:
a. Open Google Chrome and navigate to chrome://extensions.
b. Enable "Developer Mode" by toggling the switch on.
c. Click on "Load Unpacked" and navigate to the Chrome
Extension folder on your system. Select this folder. This
action installs the Chrome Extension on your Google
Chrome browser.

## 2. Starting the Server:
a. Navigate to the "FlaskApp" folder on your system.
b. Determine which model you want to use. For a non-
machine learning model, use the flask.py file. For a
model that uses BERT, use the FlaskBert.py file.
c. Open a terminal, navigate to the folder containing the
appropriate Python file, and run it. This action starts
the server for the chosen model type. Note that you
only need to start the server once to summarize multi-
ple articles or websites.

## 3. Summarizing an Article:
a. With the server running, navigate to the website con-
taining the article you want to summarize.
b. Click on the icon for the Chrome Extension you in-
stalled earlier.
c. Click on the "Summarize Text!" button. The extension
will generate a summary of the article and display it
in the user interface.
Remember that you need to keep the server running as long
as you’re using the Chrome Extension. If you stop the server,
the extension will not be able to generate summaries
