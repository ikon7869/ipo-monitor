import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
import logging
import sys
import os

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Configuration - Use environment variables instead of Colab userdata
EMAIL_FROM = os.getenv("EMAIL_FROM", "ibrahimkhanik9797@gmail.com")
EMAIL_TO = os.getenv("EMAIL_TO", "ibrahim.786.ik09@gmail.com")
EMAIL_PASS_RAW = os.getenv("MAIL_PASS")

if EMAIL_PASS_RAW is None:
    logging.error("MAIL_PASS secret not set")
    raise RuntimeError("MAIL_PASS environment variable not set")

# Clean password (remove quotes, spaces, newlines)
EMAIL_PASS = EMAIL_PASS_RAW.strip().replace('"', '').replace("'", '').replace(' ', '').replace('\n', '')

def fetch_ipos():
    """
    Fetch today's priced IPOs from NASDAQ API.
    Returns list of IPO dictionaries or empty list on failure.
    """
    url = "https://api.nasdaq.com/api/ipo/calendar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        logging.info("Fetching IPO data from NASDAQ API...")
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        
        response_json = r.json()
        
        # Validate response structure
        if "data" not in response_json:
            logging.error("Unexpected API response structure: 'data' key missing")
            return []
        
        if "priced" not in response_json["data"]:
            logging.error("Unexpected API response structure: 'priced' key missing")
            return []
            
        if "rows" not in response_json["data"]["priced"]:
            logging.error("Unexpected API response structure: 'rows' key missing")
            return []
        
        data = response_json["data"]["priced"]["rows"]
        logging.info(f"Successfully fetched {len(data)} priced IPOs")
        return data
        
    except requests.exceptions.Timeout:
        logging.error("API request timed out after 15 seconds")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return []
    except ValueError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching IPOs: {e}")
        return []

def calculate_offer_amount(ipo):
    """
    Calculate total offer amount for an IPO.
    Returns float value in USD or 0 if calculation fails.
    """
    try:
        # Method 1: Direct dollar value if available
        if "dollarValueOfSharesOffered" in ipo and ipo.get("dollarValueOfSharesOffered"):
            value_str = ipo["dollarValueOfSharesOffered"].replace("$", "").replace(",", "").strip()
            return float(value_str)
        
        # Method 2: Calculate from price × shares
        price_str = ipo.get("proposedSharePrice", "0").replace("$", "").replace(",", "").strip()
        shares_str = ipo.get("sharesOffered", "0").replace(",", "").strip()
        
        if not price_str or not shares_str:
            return 0
            
        price = float(price_str)
        shares = float(shares_str)
        
        return price * shares
        
    except (ValueError, AttributeError, TypeError) as e:
        logging.warning(f"Failed to calculate offer amount for {ipo.get('proposedTickerSymbol', 'Unknown')}: {e}")
        return 0

def send_email(tickers, error_message=None):
    """
    Send email notification with qualified IPO tickers or error message.
    Returns True if successful, False otherwise.
    """
    if error_message:
        subject = "❌ IPO Monitor - Error Occurred"
        body = f"The IPO monitoring script encountered an error:\n\n{error_message}\n\nPlease check the logs."
    elif tickers:
        subject = f"🔔 IPO Monitor - {len(tickers)} Ticker(s) Found"
        body = "IPO tickers with offer amount > $200M today:\n\n"
        body += "\n".join(f"• {ticker}" for ticker in tickers)
    else:
        subject = "✓ IPO Monitor - No Large IPOs Today"
        body = "No IPOs with offer amount above $200M were found for today."

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.attach(MIMEText(body, "plain"))

    try:
        logging.info("Attempting to send email...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.send_message(msg)
        
        logging.info("✓ Email sent successfully")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP authentication failed: {e}")
        logging.error("Check: 1) App password is correct, 2) 2FA is enabled")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error sending email: {e}")
        return False

def main():
    """Main execution function."""
    try:
        logging.info("=" * 60)
        logging.info("IPO Monitor Started")
        logging.info("=" * 60)
        
        # Get current time in both Eastern (for IPO data) and Dubai (for context)
        eastern = pytz.timezone("US/Eastern")
        dubai = pytz.timezone("Asia/Dubai")
        now_eastern = datetime.now(eastern)
        now_dubai = datetime.now(dubai)
        
        today_eastern = now_eastern.strftime("%m/%d/%Y")
        
        logging.info(f"Current time (Dubai): {now_dubai.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logging.info(f"Current time (Eastern): {now_eastern.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logging.info(f"Checking IPOs for date: {today_eastern}")
        
        # Fetch IPO data
        ipos = fetch_ipos()
        
        if not ipos:
            logging.warning("No IPO data retrieved or API returned empty results")
            send_email([], error_message="Failed to retrieve IPO data from NASDAQ API")
            return
        
        # Filter for today's IPOs with offer > $200M
        qualified = []
        for ipo in ipos:
            priced_date = ipo.get("pricedDate")
            ticker = ipo.get("proposedTickerSymbol", "N/A")
            
            if priced_date == today_eastern:
                offer_amount = calculate_offer_amount(ipo)
                logging.info(f"Ticker: {ticker}, Offer Amount: ${offer_amount:,.0f}")
                
                if offer_amount > 200_000_000:
                    qualified.append(ticker)
                    logging.info(f"  ✓ Qualified: {ticker} (${offer_amount:,.0f})")
        
        logging.info(f"Total qualified IPOs: {len(qualified)}")
        logging.info(f"Qualified tickers: {qualified if qualified else 'None'}")
        
        # Send notification email
        email_sent = send_email(qualified)
        
        if not email_sent:
            logging.error("Failed to send email notification")
            raise RuntimeError("Email notification failed")
        
        logging.info("=" * 60)
        logging.info("IPO Monitor Completed Successfully")
        logging.info("=" * 60)
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}", exc_info=True)
        # Attempt to send error notification
        try:
            send_email([], error_message=str(e))
        except:
            logging.error("Failed to send error notification email")
        raise

if __name__ == "__main__":
    main()
