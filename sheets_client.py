# sheets_client.py

import pandas as pd
import requests
import re

from io import StringIO


class SheetsClient:

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id

    @property
    def csv_url(self):
        return (
            f"https://docs.google.com/spreadsheets/d/"
            f"{self.sheet_id}/gviz/tq?tqx=out:csv"
        )

    def fetch_sheet(self):

        response = requests.get(
            self.csv_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        response.raise_for_status()

        df = pd.read_csv(
            StringIO(response.text)
        )

        # Normalize headers
        df.columns = [
            col.strip().lower()
            for col in df.columns
        ]

        return df

    def parse_score(self, score_text):

        if pd.isna(score_text):
            return None

        match = re.search(
            r"(\d+)",
            str(score_text)
        )

        return (
            int(match.group(1))
            if match
            else None
        )

    def find_latest_submission(
        self,
        username
    ):

        username = (
            username.lower().strip()
        )

        df = self.fetch_sheet()

        print("Columns found:")
        print(df.columns.tolist())

        if "username" not in df.columns:
            raise ValueError(
                "'username' column not found"
            )

        if "timestamp" not in df.columns:
            raise ValueError(
                "'timestamp' column not found"
            )

        if "score" not in df.columns:
            raise ValueError(
                "'score' column not found"
            )

        df["username"] = (
            df["username"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        matches = df[
            df["username"] == username
        ]

        if matches.empty:
            return None

        matches = matches.copy()

        matches["parsed_timestamp"] = pd.to_datetime(
            matches["timestamp"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

        latest = matches.sort_values(
            "parsed_timestamp",
            ascending=False
        ).iloc[0]

        return {
            "timestamp": str(
                latest["timestamp"]
            ),
            "username": str(
                latest["username"]
            ),
            "score_raw": str(
                latest["score"]
            ),
            "score": self.parse_score(
                latest["score"]
            )
        }
