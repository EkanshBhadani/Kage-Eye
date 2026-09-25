# config.py

import os

from dotenv import load_dotenv

load_dotenv()

# MAL

MAL_CLIENT_ID = os.getenv(
    "MAL_CLIENT_ID"
)

TOPIC_ID = int(
    os.getenv("TOPIC_ID")
)

# Google Sheets

SHEET_ID = os.getenv(
    "SHEET_ID"
)

# Quiz

TOTAL_QUESTIONS = int(
    os.getenv(
        "TOTAL_QUESTIONS",
        4
    )
)

PASSING_THRESHOLD = int(
    os.getenv(
        "PASSING_THRESHOLD",
        1
    )
)

# Files

REPORT_FILE = os.getenv(
    "REPORT_FILE",
    "data/results.xlsx"
)

STATE_FILE = os.getenv(
    "STATE_FILE",
    "data/processed_state.json"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "data/monitor.log"
)

# Report

GENERATE_AUDIT_LOG = (
    os.getenv(
        "GENERATE_AUDIT_LOG",
        "True"
    ).lower() == "true"
)

GENERATE_SUMMARY = (
    os.getenv(
        "GENERATE_SUMMARY",
        "True"
    ).lower() == "true"
)
