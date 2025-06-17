import smtplib
import logging
import idna
import json
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, mktime_tz, localtime
import os
import time
import threading
import sys
import ctypes
from PIL import Image
import win32gui
import win32con
import win32ui
import win32api
import requests
from io import BytesIO

os.system('title darkline')

def set_window_icon(icon_source='logo.png'):
    try:
        hwnd = win32gui.GetForegroundWindow()
        if icon_source.startswith(('http://', 'https://')):
            response = requests.get(icon_source)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(icon_source)
        icon_path = os.path.abspath('temp_icon.ico')
        image.save(icon_path, format='ICO')
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, icon_flags)
        if hicon:
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
            ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
            ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
            win32gui.DestroyIcon(hicon)
        if os.path.exists(icon_path):
            os.remove(icon_path)
    except Exception as e:
        logger.error(f"Failed to set window icon: {str(e)}")

set_window_icon('https://i.postimg.cc/g0nxDHsG/logo.png')

smtp_details = []
email_details = {
    "batch_size": 1,
    "punycode": True,
    "display_name": "",
    "display_email": "",
    "reply_email": "",
    "subject": "",
    "body_file": ""
}

SMTP_FILE = "smtp_servers.json"

def load_smtp_servers():
    global smtp_details
    if os.path.exists(SMTP_FILE):
        try:
            with open(SMTP_FILE, 'r', encoding='utf-8') as f:
                smtp_details = json.load(f)
        except Exception as e:
            logger.error(f"Error loading SMTP servers: {str(e)}")
            smtp_details = []

def save_smtp_servers():
    try:
        with open(SMTP_FILE, 'w', encoding='utf-8') as f:
            json.dump(smtp_details, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving SMTP servers: {str(e)}")

def generate_random_text(length=35):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

X_MAILER_OPTIONS = [
    'Microsoft Outlook Express 6.00.2900.2869',
    'Microsoft Outlook 16.0',
    'Mozilla Thunderbird 91.5.0',
    'Apple Mail (13.4)',
    'Google Mailer',
    'Yahoo Mail',
    'ProtonMail',
    'Postbox 7.0',
    'The Bat! v9.3',
    'eM Client 8.2',
    'Spark',
    'Mailbird 2.9',
    'Windows Mail 10.0',
    'KMail 5.14',
    'Evolution 3.42',
    'Claws Mail 3.18',
    'Sylpheed 3.7',
    'Thunderbird 102.0',
    'Outlook 365',
    'Gmail Web Client'
]

X_MIMEOLE_OPTIONS = [
    'Produced By Microsoft MimeOLE V6.00.2900.2869',
    'Produced By Microsoft MimeOLE V16.0.4266.1001',
    'Produced By Mozilla Thunderbird',
    'Produced By Apple Mail',
    'Produced By Google Mail',
    'Produced By Yahoo Mail',
    'Produced By ProtonMail',
    'Produced By Postbox',
    'Produced By The Bat!',
    'Produced By eM Client',
    'Produced By Spark',
    'Produced By Mailbird',
    'Produced By Windows Mail',
    'Produced By KMail',
    'Produced By Evolution',
    'Produced By Claws Mail',
    'Produced By Sylpheed',
    'Produced By Thunderbird',
    'Produced By Outlook 365',
    'Produced By Gmail'
]

X_PRIORITY_OPTIONS = ['1', '3', '5']

IMPORTANCE_OPTIONS = ['High', 'Normal', 'Low']

MESSAGE_ID_DOMAINS = [
    "example.com",
    "mail.net",
    "host.org",
    "domain.co",
    "server.io",
    "sender.info",
    "emailservice.xyz",
    "webmail.biz",
    "securemail.online",
    "postoffice.site"
]

def update_title():
    while True:
        os.system(f'title {generate_random_text()}')
        time.sleep(1)

title_thread = threading.Thread(target=update_title, daemon=True)
title_thread.start()

load_smtp_servers()

ASCII_ART = r'''
`
       ....                                         ..            ..    .                             
   .xH888888Hx.                               < .z@8"`      x .d88"    @88>                           
 .H8888888888888:                   .u    .    !@88E         5888R     %8P      u.    u.              
 888*"""?""*88888X         u      .d88B :@8c   '888E   u     '888R      .     x@88k u@88c.      .u    
'f     d8x.   ^%88k     us888u.  ="8888f8888r   888E u@8NL    888R    .@88u  ^"8888""8888"   ud8888.  
'>    <88888X   '?8  .@88 "8888"   4888>'88"    888E`"88*"    888R   ''888E`   8888  888R  :888'8888. 
 `:..:`888888>    8> 9888  9888    4888> '      888E .dN.     888R     888E    8888  888R  d888 '88%" 
        `"*88     X  9888  9888    4888>        888E~8888     888R     888E    8888  888R  8888.+"    
   .xHHhx.."      !  9888  9888   .d888L .+     888E '888&    888R     888E    8888  888R  8888L      
  X88888888hx. ..!   9888  9888   ^"8888*"      888E  9888.  .888B .   888&   "*88*" 8888" '8888c. .+ 
 !   "*888888888"    "888*""888"     "Y"      '"888*" 4888"  ^*888%    R888"    ""   'Y"    "88888%   
        ^"***"`       ^Y"   ^Y'                  ""    ""      "%       ""                    "YP'   
'''

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record)
        icons = {
            logging.INFO: "ℹ️", 
            logging.WARNING: "⚠️", 
            logging.ERROR: "❌", 
            logging.CRITICAL: "🔥"
        }
        return f"{record.asctime} {icons.get(record.levelno, '')} [{record.levelname}]: {record.getMessage()}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def set_smtp_credentials():
    print()
    print(" " * 19 + "Enter SMTP Server Details:")
    server = input(" " * 19 + "SMTP Server: ").strip()
    port = int(input(" " * 19 + "Port: ").strip())
    username = input(" " * 19 + "Username: ").strip()
    password = input(" " * 19 + "Password: ").strip()
    smtp_details.append({
        "server": server,
        "port": port,
        "username": username,
        "password": password
    })
    save_smtp_servers()
    print(" " * 19 + "SMTP server added successfully!")
    print(" " * 19 + "> ", end="", flush=True)

def remove_smtp_server():
    if not smtp_details:
        print(" " * 19 + "No SMTP servers configured.")
        print(" " * 19 + "> ", end="", flush=True)
        return
    print()
    print(" " * 19 + "Configured SMTP Servers:")
    for i, smtp in enumerate(smtp_details, 1):
        print(" " * 19 + f"{i}. {smtp['server']} ({smtp['username']})")
    try:
        choice = int(input("\n" + " " * 19 + "Enter number to remove (0 to cancel): ").strip())
        if choice == 0:
            return
        if 1 <= choice <= len(smtp_details):
            removed = smtp_details.pop(choice - 1)
            save_smtp_servers()
            print(" " * 19 + f"Removed SMTP server: {removed['server']}")
        else:
            print(" " * 19 + "Invalid choice.")
    except ValueError:
        print(" " * 19 + "Please enter a valid number.")
    print(" " * 19 + "> ", end="", flush=True)

def load_email_body(body_file):
    if os.path.exists(body_file):
        with open(body_file, 'r', encoding='utf-8') as f:
            return f.read()
    logger.error(f"Email body file '{body_file}' does not exist.")
    return None

def send_email(smtp_details, recipient, email_details):
    if not smtp_details:
        logger.error("No SMTP servers configured. Please add SMTP servers first.")
        return False
    smtp = random.choice(smtp_details)
    body = load_email_body(email_details['body_file'])
    if body is None:
        return False

    random_boundary = generate_random_text(30)
    msg = MIMEMultipart('alternative', boundary=random_boundary)
    
    message_id_domain = random.choice(MESSAGE_ID_DOMAINS)
    message_id = f"<{generate_random_text(20)}@{message_id_domain}>"
    
    if email_details['punycode']:
        local_part, domain_part = email_details['display_email'].split('@')
        encoded_domain = idna.encode(domain_part).decode('utf-8')
        encoded_display_email = f"{local_part}@{encoded_domain}"
        msg['From'] = f"{email_details['display_name']} <{encoded_display_email}>"
    else:
        msg['From'] = f"{email_details['display_name']} <{email_details['display_email']}>"
    
    msg['Sender'] = smtp['server']
    msg['Reply-To'] = f"{email_details['display_name']} <{email_details['reply_email']}>"
    msg['To'] = recipient
    msg['Subject'] = email_details['subject']
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = message_id
    msg['X-Mailer'] = random.choice(X_MAILER_OPTIONS)
    msg['X-MimeOLE'] = random.choice(X_MIMEOLE_OPTIONS)
    msg['X-Priority'] = random.choice(X_PRIORITY_OPTIONS)
    msg['X-MSMail-Priority'] = msg['X-Priority']
    msg['Importance'] = random.choice(IMPORTANCE_OPTIONS)
    msg['X-Authentication-Warning'] = smtp['server']
    msg['List-Unsubscribe'] = f"<mailto:{email_details['reply_email']}?subject=unsubscribe>"
    msg['Precedence'] = 'bulk'
    msg['X-Auto-Response-Suppress'] = 'OOF, AutoReply'
    msg['Auto-Submitted'] = 'auto-generated'
    
    msg['DKIM-Signature'] = f"v=1; a=rsa-sha256; c=relaxed/relaxed; d={message_id_domain}; s=selector; h=From:To:Subject:Date:Message-ID; bh={generate_random_text(44)}=; b={generate_random_text(344)}"
    msg['ARC-Authentication-Results'] = f"i=1; {message_id_domain}; spf=pass smtp.mailfrom={smtp['username']}; dkim=pass header.d={message_id_domain}; dmarc=pass action=none header.from={message_id_domain}"
    msg['Authentication-Results'] = f"{message_id_domain}; spf=pass smtp.mailfrom={smtp['username']}; dkim=pass header.d={message_id_domain}; dmarc=pass action=none header.from={message_id_domain}"
    
    msg['MIME-Version'] = '1.0'
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP(smtp['server'], smtp['port'], timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp['username'], smtp['password'])
        
        server.sendmail(smtp['username'], recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(" " * 20 + f"Failed to send email to {recipient}. Error: {str(e)}")
    return False

def load_recipients(file_path):
    if not os.path.exists(file_path):
        logger.error(f"The file '{file_path}' does not exist.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        logger.error(f"Error reading the file '{file_path}': {str(e)}")
        return []

def batch_process(recipients, batch_size, email_details):
    email_count = 0
    for recipient in recipients:
        if send_email(smtp_details, recipient, email_details):
            email_count += 1
            print(" " * 19 + f"Email sent to {recipient}")
        delay = random.randint(2, 5)
        time.sleep(delay)
    return email_count

def main():
    if not smtp_details:
        print(" " * 19 + "No SMTP servers configured. Please add SMTP servers first.")
        print(" " * 19 + "> ", end="", flush=True)
        return
    print()
    print(" " * 19 + "Enter Email Details:")
    display_name = input(" " * 19 + "Display Name: ").strip()
    display_email = input(" " * 19 + "Display Email: ").strip()
    reply_email = input(" " * 19 + "Reply Email: ").strip()
    subject = input(" " * 19 + "Subject: ").strip()
    body_file = input(" " * 19 + "HTML File Path: ").strip()
    batch_size = int(input(" " * 19 + "Batch Size: ").strip())
    print()
    email_details.update({
        "batch_size": batch_size,
        "punycode": True,
        "display_name": display_name,
        "display_email": display_email,
        "reply_email": reply_email,
        "subject": subject,
        "body_file": body_file
    })
    recipients = load_recipients('emails.txt')
    if not recipients:
        print(" " * 19 + "No recipients found. Exiting.")
        return
    total_batches = (len(recipients) + batch_size - 1) // batch_size
    total_emails_sent = 0
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        current_batch = i // batch_size + 1
        print(" " * 19 + f"Batch {current_batch} of {total_batches}")
        print()
        emails_sent = batch_process(batch, batch_size, email_details)
        total_emails_sent += emails_sent
        if i + batch_size < len(recipients):
            print()
            animation = ['/', '-', '\\', '|']
            print(" " * 19 + "Batch complete, please wait 60 seconds", end="", flush=True)
            for _ in range(60):
                for char in animation:
                    sys.stdout.write(f"\r{' ' * 19}Batch complete, please wait 60 seconds {char}")
                    sys.stdout.flush()
                    time.sleep(0.25)
            print("\r" + " " * 100)
            print()
            print()
    print()
    batch_text = "batch" if total_batches == 1 else "batches"
    print(" " * 19 + f"Sent {total_emails_sent} emails with {total_batches} {batch_text}")
    print(" " * 19 + "> ", end="", flush=True)

def check_smtp():
    if not smtp_details:
        print(" " * 19 + "No SMTP servers configured. Please add SMTP servers first.")
        print(" " * 19 + "> ", end="", flush=True)
        return
    print()
    print(" " * 20 + "Checking SMTP servers...")
    for smtp in smtp_details:
        animation = ['/', '-', '\\', '|']
        for _ in range(10):
            for char in animation:
                sys.stdout.write("\r" + " " * 20 + f"Testing {smtp['server']} {char}")
                sys.stdout.flush()
                time.sleep(0.1)
        try:
            server = smtplib.SMTP(smtp['server'], smtp['port'], timeout=30)
            server.ehlo()
            server.starttls()
            server.login(smtp['username'], smtp['password'])
            server.quit()
            print("\r" + " " * 20 + f"SMTP server {smtp['server']} is working")
        except Exception as e:
            print("\r" + " " * 20 + f"SMTP server {smtp['server']} failed: {str(e)}")
    print(" " * 20 + "> ", end="", flush=True)

def check_recipients():
    recipients = load_recipients('emails.txt')
    print()
    if recipients:
        print(" " * 20 + f"Found {len(recipients)} recipient emails:")
        for i, recipient in enumerate(recipients, 1):
            print(" " * 20 + f"{i}. {recipient}")
    else:
        print(" " * 20 + "No recipients found in emails.txt")
    print(" " * 20 + "> ", end="", flush=True)

def clear_cache():
    try:
        if os.path.exists('temp_icon.ico'):
            os.remove('temp_icon.ico')
        if os.path.exists('__pycache__'):
            import shutil
            shutil.rmtree('__pycache__')
        if os.path.exists('.pytest_cache'):
            import shutil
            shutil.rmtree('.pytest_cache')
        if os.path.exists('.coverage'):
            os.remove('.coverage')
        if os.path.exists('htmlcov'):
            import shutil
            shutil.rmtree('htmlcov')
        if os.path.exists('.mypy_cache'):
            import shutil
            shutil.rmtree('.mypy_cache')
        if os.path.exists('.ruff_cache'):
            import shutil
            shutil.rmtree('.ruff_cache')
        if os.path.exists('.hypothesis'):
            import shutil
            shutil.rmtree('.hypothesis')
        if os.path.exists('.tox'):
            import shutil
            shutil.rmtree('.tox')
        if os.path.exists('.eggs'):
            import shutil
            shutil.rmtree('.eggs')
        if os.path.exists('build'):
            import shutil
            shutil.rmtree('build')
        if os.path.exists('dist'):
            import shutil
            shutil.rmtree('dist')
        if os.path.exists('*.egg-info'):
            import glob
            for egg in glob.glob('*.egg-info'):
                shutil.rmtree(egg)
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")

def display_menu():
    art_lines = ASCII_ART.strip().split('\n')
    max_width = max(len(line.rstrip()) for line in art_lines)
    terminal_width = 120
    padding = (terminal_width - max_width) // 2
    centered_art = '\n'.join(' ' * padding + line for line in art_lines if line.strip())

    def show_menu(first_time=False):
        print("\n" + centered_art + "\n")
        print(" " * 20 + "Email Sender" + "\n")
        print(" " * 20 + "1. Send Emails")
        print(" " * 20 + "2. Check SMTP")
        print(" " * 20 + "3. Check Receiver Emails")
        print(" " * 20 + "4. Add SMTP Server")
        print(" " * 20 + "5. Remove SMTP Server")
        print(" " * 20 + "6. Exit & Clear Cache")
        if first_time:
            print(" " * 20 + "> ", end="", flush=True)
        else:
            print()

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[2J\033[H", end="")

    class MenuStreamHandler(logging.StreamHandler):
        def emit(self, record):
            try:
                msg = self.format(record)
                print(" " * 20 + msg)
                print(" " * 20 + "> ", end="", flush=True)
            except Exception:
                self.handleError(record)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger.addHandler(MenuStreamHandler())

    clear_screen()
    show_menu(first_time=True)

    while True:
        choice = input().strip()
        clear_screen()
        show_menu(first_time=False)
        if choice == "1":
            main()
        elif choice == "2":
            check_smtp()
        elif choice == "3":
            check_recipients()
        elif choice == "4":
            set_smtp_credentials()
        elif choice == "5":
            remove_smtp_server()
        elif choice == "6":
            logger.info("Clearing cache and exiting...")
            clear_cache()
            logger.info("Goodbye!")
            break
        else:
            logger.warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    display_menu()
