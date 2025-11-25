import os
from utils.api_client import APIClient
from utils.excel_writer import create_excel
from utils.emailer import build_email_body, send_email_with_attachments
from utils.error_handler import log_error, log_info, attachable_log_exists

def main():
    # env / secrets
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    TO_EMAIL   = os.getenv("TO_EMAIL")

    API_KEY = os.getenv("API_KEY")
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

    # internal endpoints (provided)
    API_TXN = os.getenv("API_TXN", "https://internal.company.com/api/v1/transactions/summary")
    API_SCORE = os.getenv("API_SCORE", "https://internal.company.com/api/v1/scorecard/monthly")
    API_DAILY = os.getenv("API_DAILY", "https://internal.company.com/api/v1/reports/daily")

    client = APIClient(headers=headers)

    try:
        transactions = client.fetch(API_TXN)
    except Exception as e:
        log_error("Transactions API failed", e)
        transactions = []

    try:
        scorecard = client.fetch(API_SCORE)
    except Exception as e:
        log_error("Scorecard API failed", e)
        scorecard = []

    try:
        daily_report = client.fetch(API_DAILY)
    except Exception as e:
        log_error("Daily Report API failed", e)
        daily_report = []

    excel_file = create_excel(transactions, scorecard, daily_report)

    counts = {
        "Transactions records": len(transactions),
        "Scorecard records": len(scorecard),
        "Daily report records": len(daily_report),
    }

    body = build_email_body(counts)
    if attachable_log_exists():
        body = "⚠ Some errors occurred. See attached log.\n\n" + body

    attachments = [excel_file]
    if attachable_log_exists():
        attachments.append("error.log")

    try:
        send_email_with_attachments(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL,
                                    "Automated Multi-API Report", body, attachments)
    except Exception as e:
        log_error("Final email failed", e)
        # email failed — still exit with non-zero to show failure in workflow
        raise

if __name__ == "__main__":
    main()
