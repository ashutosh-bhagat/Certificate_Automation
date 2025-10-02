"""
personalize_and_send.py

Takes base certificate PDF (with blank underline), overlays attendee name,
and emails it as PDF attachment.
"""

import csv
import os
import ssl
import smtplib
import time
import logging
from email.message import EmailMessage
import argparse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter

# -------------------------
# CONFIGURATION
# -------------------------
BASE_CERT = "life of py certi.pdf"   # your uploaded certificate
CSV_PATH = "email and name.csv"
OUTPUT_DIR = "personalized_certs"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Allow overriding credentials via environment variables for safety
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "thea.i.m.club21@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "dajf vgsk kqkb yisw")

FROM_NAME = "The A.I.M. Club Team"
FROM_EMAIL = SMTP_USERNAME
SUBJECT = "Your Certificate of Participation For Life Of .py"
BODY_TEMPLATE = """Hello {name},

Congratulations! Please find your certificate attached.

Regards,
{from_name}
"""

FONT_PATH = "KodeMono-SemiBold.ttf"  # place Kode Mono TTF here or set absolute path
FONT_SIZE = 36
TEXT_X = "center"   # use "center" to horizontally center on the page
TEXT_Y = None        # exact Y in points; if None, uses TEXT_Y_RATIO
TEXT_Y_RATIO = 0.42  # fraction of page height from bottom (e.g., 0.42 = 42%)

DELAY_BETWEEN_EMAILS = 1.0
LOG_FILE = "certificates.log"

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)


# -------------------------
# Generate overlay PDF with attendee name
# -------------------------
def create_name_overlay(name, overlay_path, page_width, page_height):
    c = canvas.Canvas(overlay_path, pagesize=(page_width, page_height))

    try:
        pdfmetrics.registerFont(TTFont("CustomFont", FONT_PATH))
        font_name = "CustomFont"
    except Exception:
        font_name = "Helvetica-Bold"

    c.setFont(font_name, FONT_SIZE)
    # White text
    c.setFillColorRGB(1, 1, 1)

    # Centered on the underline area
    text_width = c.stringWidth(name, font_name, FONT_SIZE)
    x = TEXT_X if TEXT_X != "center" else (page_width - text_width) / 2
    y = TEXT_Y if TEXT_Y is not None else (page_height * TEXT_Y_RATIO)
    c.drawString(x, y, name)

    c.save()


# -------------------------
# Merge overlay onto base certificate
# -------------------------
def personalize_certificate(name, out_path):
    base = PdfReader(BASE_CERT)
    base_page = base.pages[0]
    page_width = float(base_page.mediabox.width)
    page_height = float(base_page.mediabox.height)

    overlay_pdf = "overlay.pdf"
    create_name_overlay(name, overlay_pdf, page_width, page_height)

    overlay = PdfReader(overlay_pdf)

    writer = PdfWriter()
    base_page.merge_page(overlay.pages[0])
    writer.add_page(base_page)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f_out:
        writer.write(f_out)

    os.remove(overlay_pdf)
    logging.info(f"Generated certificate for {name}: {out_path}")
    return out_path


# -------------------------
# Email sender
# -------------------------
def send_email(to_email, subject, body, attachment_path, attach=True, smtp_debug=False):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg.set_content(body)

    file_name = None
    if attach and attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if smtp_debug:
            server.set_debuglevel(1)
        server.starttls(context=context)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

    if file_name:
        logging.info(f"Email sent to {to_email} with {file_name}")
    else:
        logging.info(f"Email sent to {to_email} (no attachment)")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate and optionally email personalized certificates")
    parser.add_argument("--dry-run", action="store_true", help="Generate PDFs but do not send emails")
    parser.add_argument("--limit", type=int, default=0, help="Process only the first N rows (0 for all)")
    parser.add_argument("--only-email", type=str, default="", help="Process only the row matching this email")
    parser.add_argument("--only-name", type=str, default="", help="Process only the row matching this name (case-insensitive)")
    # Ad-hoc send without relying on CSV contents
    parser.add_argument("--adhoc-email", type=str, default="", help="Send directly to this email (bypass CSV)")
    parser.add_argument("--adhoc-name", type=str, default="Test Recipient", help="Name to render for adhoc send")
    # Email/debug controls
    parser.add_argument("--no-attach", action="store_true", help="Send email without PDF attachment (debug)")
    parser.add_argument("--subject", type=str, default="", help="Override email subject")
    parser.add_argument("--body", type=str, default="", help="Override email body")
    parser.add_argument("--smtp-debug", action="store_true", help="Enable SMTP debug output")
    return parser.parse_args()


# -------------------------
# Main
# -------------------------
def main():
    args = parse_args()
    if not os.path.isfile(CSV_PATH):
        logging.error(f"CSV file not found: {CSV_PATH}")
        # Allow ad-hoc send even if CSV missing
        if not args.adhoc_email:
            return

    processed = 0
    if os.path.isfile(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            # Normalize header names in case of BOM or trailing spaces
            if reader.fieldnames:
                reader.fieldnames = [fn.strip().lstrip('\ufeff') if isinstance(fn, str) else fn for fn in reader.fieldnames]

            for row in reader:
                # Normalize keys and values per row as well
                row = { (k.strip().lstrip('\ufeff') if isinstance(k, str) else k): (v.strip() if isinstance(v, str) else v) for k, v in row.items() }
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()

                if not name or not email:
                    logging.warning(f"Skipping invalid row: {row}")
                    continue

                # Optional filters
                if args.only_email and email.lower() != args.only_email.lower():
                    continue
                if args.only_name and name.lower() != args.only_name.lower():
                    continue

                safe_name = name.replace(" ", "_").lower()
                cert_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")

                try:
                    personalize_certificate(name, cert_path)
                    body_text = (args.body if args.body else BODY_TEMPLATE.format(name=name, from_name=FROM_NAME))
                    subject_text = (args.subject if args.subject else SUBJECT)
                    if args.dry_run:
                        logging.info(f"[DRY_RUN] Would email {email} with {cert_path}")
                    else:
                        send_email(email, subject_text, body_text, cert_path, attach=(not args.no_attach), smtp_debug=args.smtp_debug)
                except Exception as e:
                    logging.exception(f"Failed for {name} <{email}>: {e}")

                processed += 1
                if args.limit and processed >= args.limit:
                    logging.info(f"Limit reached ({args.limit}). Stopping.")
                    break

                time.sleep(DELAY_BETWEEN_EMAILS)

    # Ad-hoc single send if filters yielded nothing or CSV missing
    if processed == 0 and args.adhoc_email:
        name = args.adhoc_name.strip() or "Test Recipient"
        email = args.adhoc_email.strip()
        safe_name = name.replace(" ", "_").lower()
        cert_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")
        try:
            personalize_certificate(name, cert_path)
            body_text = (args.body if args.body else BODY_TEMPLATE.format(name=name, from_name=FROM_NAME))
            subject_text = (args.subject if args.subject else SUBJECT)
            if args.dry_run:
                logging.info(f"[DRY_RUN] Would email {email} with {cert_path}")
            else:
                send_email(email, subject_text, body_text, cert_path, attach=(not args.no_attach), smtp_debug=args.smtp_debug)
                logging.info(f"Ad-hoc email sent to {email}")
        except Exception as e:
            logging.exception(f"Ad-hoc send failed for {name} <{email}>: {e}")


if __name__ == "__main__":
    main()
