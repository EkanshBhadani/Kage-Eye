# mal_client.py

import re
import html
import requests


class MALClient:

    def __init__(self, client_id, topic_id):
        self.client_id = client_id
        self.topic_id = topic_id

    def get_posts(self):

        url = (
            f"https://api.myanimelist.net/v2/"
            f"forum/topic/{self.topic_id}"
        )

        headers = {
            "X-MAL-CLIENT-ID": self.client_id
        }

        params = {
            "limit": 100,
            "offset": 0
        }

        all_posts = []

        while True:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            posts = (
                data.get("data", {})
                .get("posts", [])
            )

            all_posts.extend(posts)

            paging = data.get("paging", {})

            next_url = paging.get("next")

            if not next_url:
                break

            url = next_url

            # next_url already contains
            # pagination parameters
            params = None

        return all_posts

    def extract_submission(self, body):

        if not body:
            return None

        # Decode escaped HTML
        body = html.unescape(body)

        # Convert HTML line breaks
        body = re.sub(
            r"<br\s*/?>",
            "\n",
            body,
            flags=re.IGNORECASE
        )

        body = body.replace("\r", "")

        pattern = (
            r"submited(?:\s+the\s+form)?!"
            r".*?"
            r"username:\s*([^\r\n<]+)"
        )

        match = re.search(
            pattern,
            body,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            return None

        return match.group(1).strip()

    def get_valid_submissions(self):

        posts = self.get_posts()

        submissions = []

        print(
            f"Total forum posts fetched: "
            f"{len(posts)}"
        )

        for post in posts:

            username = self.extract_submission(
                post.get("body", "")
            )

            print(
                f"Reply #{post.get('number')} "
                f"-> {username}"
            )

            if username is None:
                continue

            submissions.append({
                "reply_number":
                    post.get("number"),

                "forum_user":
                    post.get(
                        "created_by",
                        {}
                    ).get("name"),

                "submitted_username":
                    username
            })

        return submissions
