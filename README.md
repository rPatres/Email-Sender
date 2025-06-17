# DarkLine <img src="https://i.postimg.cc/g0nxDHsG/logo.png" width="30" height="30"/>
> **An application designed for sending spoofed emails undetectably**

*DarkLine is a powerful email automation application designed to help you manage and utilize your own SMTP servers with ease. It enables you to send large volumes of emails in organized batches, ensuring maximum efficiency and deliverability. With built-in mechanisms for staying under the radar, DarkLine operates undetected, making it ideal for high-volume campaigns that require both speed and discretion. Whether you're managing outreach, marketing, or transactional messages, DarkLine gives you the control, reliability, and performance you need*


## Features

*   **Configurable SMTP Servers**: Easily add and remove SMTP server credentials.
*   **Batch Sending**: Send emails in batches to manage sending rates.
*   **HTML Email Support**: Send rich, formatted emails using an HTML body file.
*   **Punycode Support**: Handles internationalized domain names in email addresses.
*   **Spam Evasion Techniques**:
    *   **Randomized Headers**: `X-Mailer`, `X-MimeOLE`, `X-Priority`, and `Importance` headers are randomized for each email to avoid pattern detection.
    *   **Randomized Date Header**: The `Date` header is slightly varied for each email.
    *   **Plain Text Alternative**: Each email includes both an HTML and a plain text version for better compatibility and spam score.
    *   **Randomized MIME Boundary**: The MIME boundary string, which separates different parts of the email, is unique for every message.
    *   **Randomized Message-ID Domain**: The domain used in the `Message-ID` header is randomized from a predefined list, making each email appear more distinct.
    *   **Randomized Batch Delay**: Introduces a variable delay between sending batches to mimic human sending patterns.

## Setup Instructions

Follow these steps to get the Email-Sender up and running on your local machine.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/rPatres/Email-Sender.git
cd Email-Sender
```

### 2. Install Dependencies

The project uses a `requirements.txt` file to manage its dependencies. Install them using pip:

```bash
pip install -r requirements.txt
```

### 3. Prepare Email Lists and Content

Before running the application, you need to prepare your recipient list and email body.

#### `emails.txt`

Create a file named `emails.txt` in the root directory of the project. Each line in this file should contain one recipient email address.

Example `emails.txt`:
```
recipient1@example.com
recipient2@another.org
```

#### HTML Email Body File

Create an HTML file (e.g., `email_body.html`) that contains the content of your email. This file path will be requested when you run the application.

Example `email_body.html`:
```html
<!DOCTYPE html>
<html>
<head>
<title>My Awesome Email</title>
</head>
<body>
    <p>Hello,</p>
    <p>This is a **test email** from the Email-Sender application.</p>
    <p>Hope you enjoy it!</p>
    <p>Best regards,<br>Your Name</p>
</body>
</html>
```

### 4. Configure SMTP Servers

The application manages SMTP server details in a `smtp_servers.json` file. You can add SMTP server details directly through the application's menu.

## How to Run

After completing the setup, you can run the application:

```bash
python app.py
```

Upon running, you will be presented with a menu:


  <img src="https://i.postimg.cc/28fQZF5g/image.png"/>


### Menu Options:

*   **1. Send Emails**: Prompts for email details (Display Name, Display Email, Reply Email, Subject, HTML File Path, Batch Size) and then starts sending emails to the recipients listed in `emails.txt`.
*   **2. Check SMTP**: Verifies the connectivity and login credentials for all configured SMTP servers.
*   **3. Check Receiver Emails**: Displays the list of recipient emails loaded from `emails.txt`.
*   **4. Add SMTP Server**: Allows you to input and save new SMTP server credentials. These are stored in `smtp_servers.json`.
*   **5. Remove SMTP Server**: Lets you remove an existing SMTP server configuration.
*   **6. Exit & Clear Cache**: Exits the application and removes temporary files and cache directories.

## Important Considerations for Email Deliverability

While this tool implements several techniques to improve the chances of your emails reaching the inbox, it's crucial to understand that **spoofing emails carries inherent risks and can lead to immediate spam flagging or blacklisting if not done responsibly and in accordance with email sending best practices.**

For legitimate email sending, always ensure:

*   **Proper DNS Records**: Configure SPF, DKIM, and DMARC DNS records for your sending domain. These are fundamental for email authentication and signal legitimacy to receiving mail servers. Without them, your emails are highly likely to be flagged as spam regardless of other techniques.
*   **Good Sender Reputation**: Maintain a positive sender reputation by sending to engaged recipients, avoiding spam complaints, and cleaning your email lists regularly.
*   **Relevant and Non-Spammy Content**: The content of your email itself plays a huge role. Avoid spammy keywords, excessive images, and always provide value to the recipient.
*   **Consent**: Always ensure you have consent from recipients to send them emails. Sending unsolicited emails (spam) can lead to severe consequences, including legal issues and permanent blacklisting.

This tool is provided for educational and legitimate testing purposes. Misuse of this tool for unsolicited bulk emailing (spamming) is not endorsed and can have negative consequences.

<p align="center">
  <img src="https://img.shields.io/badge/License-%23bcbcbc?style=for-the-badge&logo=GitBook&logoColor=bcbcbc&labelColor=black&link=https%3A%2F%2Fopensource.org%2Flicense%2Fmit"/>
  <img src="https://img.shields.io/badge/Undetected-%23bcbcbc?style=for-the-badge&logo=hackaday&logoColor=bcbcbc&labelColor=black"/>
  <img src="https://img.shields.io/badge/Python-%23bcbcbc?style=for-the-badge&logo=python&logoColor=bcbcbc&labelColor=black&link=https%3A%2F%2Fwww.python.org%2F"/>
  <img src="https://img.shields.io/badge/%40imrxp-%23bcbcbc?style=for-the-badge&logo=telegram&logoColor=bcbcbc&labelColor=black&link=t.me%2Frxpdev"/>
</p>



