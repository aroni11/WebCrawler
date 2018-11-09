from link_finder import LinkFinder
from robot_parser import RobotParser
from helpers import *
from domain import *


class Spider:

    project_name = ''
    base_url = ''
    page_url = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    robotsCache = dict()

    def __init__(self, project_name, base_url, page_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.page_url = page_url
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.page_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled: #and not RobotParser(Spider.robotsCache).can_crawl(page_url):
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            print(Spider.gather_links())
            Spider.add_links_to_queue(Spider.gather_links())
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links():
        try:
            finder = LinkFinder(Spider.base_url, Spider.page_url)
        except Exception as e:
            print(str(e))
            return set()
        return finder.get_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if get_sub_domain_name(url) not in Spider.base_url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
