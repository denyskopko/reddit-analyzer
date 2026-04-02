import logging
import requests
from app.my_config import Config

logger = logging.getLogger("reddit_analyzer")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("out.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class RedditService:
    def __init__(self):
        self.debug = Config.DEBUG
        self.headers = {"User-Agent": "reddit_analyzer:v1.0"}

    def fetch_and_filter(self, subreddit_name: str, keywords: list, limit: int):
        clean_sub = subreddit_name.replace("r/", "").replace("/", "").strip()
        logger.info(f"Processing: {clean_sub} | Limit: {limit} | Keywords: {keywords}")

        if self.debug:
            logger.info("DEBUG режим — используем заглушки")
            titles = [
                "Beautiful forest in autumn", "River in the mountains",
                "Cute dog playing", "Cat sleeping", "Forest river flow"
            ]
        else:
            try:
                url = f"https://www.reddit.com/r/{clean_sub}.json?limit={limit}"
                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code != 200:
                    logger.error(f"Reddit вернул статус {response.status_code} для {clean_sub}")
                    return []

                data = response.json()
                posts = data["data"]["children"]
                titles = [post["data"]["title"] for post in posts]
                logger.info(f"Найдено {len(titles)} постов из {limit} запрошенных | r/{clean_sub}")

            except requests.exceptions.ConnectionError:
                logger.error(f"Нет соединения с Reddit для {clean_sub}")
                return []
            except requests.exceptions.Timeout:
                logger.error(f"Таймаут при запросе к {clean_sub}")
                return []
            except Exception as e:
                logger.error(f"Ошибка при запросе к {clean_sub}: {e}")
                return []

        filtered = [t for t in titles if any(kw.lower() in t.lower() for kw in keywords)]
        logger.info(f"Найдено {len(filtered)} из {len(titles)} запрошенных | r/{clean_sub}")
        return filtered


reddit_service = RedditService()



