# main.py

from config import (
    MAL_CLIENT_ID,
    TOPIC_ID,
    SHEET_ID,
    PASSING_THRESHOLD
)

from mal_client import MALClient
from sheets_client import SheetsClient
from state_manager import StateManager
from report_writer import ReportWriter
from logger_setup import setup_logger


def main():

    logger = setup_logger()

    print("=" * 50)
    print("Starting Report Generation")
    print("=" * 50)

    logger.info(
        "Report generation started"
    )

    mal = MALClient(
        MAL_CLIENT_ID,
        TOPIC_ID
    )

    sheets = SheetsClient(
        SHEET_ID
    )

    state = StateManager()

    report = ReportWriter()

    # Create a completely fresh Excel report
    report.create_fresh_report()

    submissions = mal.get_valid_submissions()

    print(
        f"Found {len(submissions)} valid forum submissions"
    )

    logger.info(
        f"Found {len(submissions)} valid submissions"
    )

    passed_count = 0
    failed_count = 0
    missing_count = 0
    skipped_count = 0

    for submission in submissions:

        username = submission[
            "submitted_username"
        ]

        reply_number = submission[
            "reply_number"
        ]

        forum_user = submission[
            "forum_user"
        ]

        print(
            f"\nProcessing reply #{reply_number}"
        )

        print(
            f"Username: {username}"
        )

        logger.info(
            f"Processing username={username}"
        )

        form_data = (
            sheets.find_latest_submission(
                username
            )
        )

        # ======================
        # USER NOT FOUND
        # ======================

        if form_data is None:

            report.add_missing(
                username,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                "N/A",
                "Missing",
                "N/A"
            )

            missing_count += 1

            logger.warning(
                f"{username} not found in Google Sheet"
            )

            continue

        timestamp = form_data[
            "timestamp"
        ]

        score = form_data[
            "score"
        ]

        score_raw = form_data[
            "score_raw"
        ]

        # ======================
        # ALREADY PROCESSED
        # ======================

        if state.already_processed(
            username,
            timestamp
        ):

            skipped_count += 1

            logger.info(
                f"Skipped already processed: {username}"
            )

            continue

        # ======================
        # PASSED
        # ======================

        if score >= PASSING_THRESHOLD:

            report.add_passed(
                username,
                score_raw,
                timestamp,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                score_raw,
                "Passed",
                timestamp
            )

            passed_count += 1

            logger.info(
                f"PASSED | {username} | {score_raw}"
            )

        # ======================
        # FAILED
        # ======================

        else:

            report.add_failed(
                username,
                score_raw,
                timestamp,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                score_raw,
                "Failed",
                timestamp
            )

            failed_count += 1

            logger.info(
                f"FAILED | {username} | {score_raw}"
            )

        state.mark_processed(
            username,
            timestamp
        )

    report.update_summary()

    logger.info(
        f"Completed | Passed={passed_count} "
        f"Failed={failed_count} "
        f"Missing={missing_count} "
        f"Skipped={skipped_count}"
    )

    print("\n" + "=" * 50)
    print("REPORT COMPLETED")
    print("=" * 50)

    print(f"Passed : {passed_count}")
    print(f"Failed : {failed_count}")
    print(f"Missing: {missing_count}")
    print(f"Skipped: {skipped_count}")

    print(
        "\nExcel report saved to:"
        " data/results.xlsx"
    )


if __name__ == "__main__":
    main()
