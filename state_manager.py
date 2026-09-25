# state_manager.py

import json
import os


class StateManager:

    def __init__(
        self,
        filepath="data/processed_state.json"
    ):
        self.filepath = filepath

    def load(self):

        if not os.path.exists(self.filepath):
            return {}

        try:

            with open(
                self.filepath,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):
            return {}

    def save(self, state):

        os.makedirs(
            os.path.dirname(self.filepath),
            exist_ok=True
        )

        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                state,
                f,
                indent=4
            )

    def already_processed(
        self,
        username,
        timestamp
    ):

        state = self.load()

        username = username.lower()

        return (
            state.get(username)
            == timestamp
        )

    def mark_processed(
        self,
        username,
        timestamp
    ):

        state = self.load()

        state[
            username.lower()
        ] = timestamp

        self.save(state)
