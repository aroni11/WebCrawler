from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import downloader


class RobotParser:
    def __init__(self, cache):
        self.cache = cache

    def can_crawl(self, url):
        robots_path = self.get_robots_path(url)
        parser = RobotFileParser()

        if self.cache.get(robots_path) is None:
            robots_content = self.read_robots(robots_path)
            self.cache[robots_path] = robots_content
        else:
            robots_content = self.cache.get(robots_path)

        if robots_content is None:
            return True

        if robots_content is False:
            return False

        parser.parse(robots_content)
        return parser.can_fetch("*", url)

    @staticmethod
    def get_robots_path(page_url):
        path = urlparse(page_url)
        return path.scheme + "://" + path.netloc + "/robots.txt"

    @staticmethod
    def read_robots(robots_path):
        f = downloader.download_file(robots_path)
        if f is False:
            return False

        if f is None:
            return None

        try:
            return f.read().decode('utf-8')
        except:
            return False
