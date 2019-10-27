from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from config import CrawlerConfig
import urllib.request
import calendar
import uuid
import re
import os


class NaverImageCrawler(CrawlerConfig):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.keywords = set()

    def print_log(self, *log_msg):
        print(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), *log_msg)

    def set_keywords(self, *keyword_set):
        self.print_log('Setting keyword list.')
        self.keywords = keyword_set

    def execute(self, year, month, number_by_date=100):
        self.print_log('Starting Naver Image Crawling.')
        self.open_browser()
        last_day = calendar.monthrange(year, month)[1]
        for day in range(1, last_day + 1):
            date = self.convert_to_string_date(year, month, day)
            for keyword in self.keywords:
                self.search_tag(keyword, date)
                link_list = self.down_scroll_and_get_img_links(number_by_date)
                self.save_img_from_link_list(keyword, link_list)

        self.close_browser()

    def open_browser(self):
        self.print_log('Opening Chrome Browser.')
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def convert_to_string_date(self, year, month, day):
        year = str(year)
        month = str(month) if len(str(month)) == 2 else '0' + str(month)
        day = str(day) if len(str(day)) == 2 else '0' + str(day)
        return year, month, day

    def search_tag(self, keyword, date):
        self.print_log('Searching {keyword} on {date}'.format(keyword=keyword, date=date))
        self.driver.get(self.search_url.format(
            keyword=keyword,
            date=''.join(date)
        ))
        self.driver.implicitly_wait(10)
        sleep(5)

    def down_scroll_and_get_img_links(self, number_by_date):
        self.print_log('Getting image link list.')
        scroll_pos = 1
        links_list = []
        patient = number_by_date / 5
        while len(links_list) < number_by_date:
            self.driver.execute_script("window.scrollTo(0, " + str(scroll_pos * 500) + ");")
            sleep(2)
            scroll_pos += 1
            if scroll_pos >= patient:
                break
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            img_elements = soup.find_all("img")
            for img_element in img_elements:
                img_url_pt = re.compile('https://.*b400')
                matched_img_url = img_url_pt.search(str(img_element.attrs))
                if matched_img_url:
                    links_list.append(matched_img_url.group())
            links_list = list(set(links_list))
        return links_list

    def save_img_from_link_list(self, keyword, link_list):
        self.print_log('Downloading Images.')
        target_directory = self.download_directory + keyword + '/'
        if not os.path.isdir(target_directory):
            os.mkdir(target_directory)
        for link in link_list:
            file_name = uuid.uuid4()[:20]
            urllib.request.urlretrieve(link, target_directory + file_name + '.jpg')
            self.print_log(file_name + ' is saved.')
            sleep(0.1)

    def close_browser(self):
        self.print_log('Closing Chrome Browser.')
        self.driver.quit()


if __name__ == '__main__':
    crawler = NaverImageCrawler()
    crawler.set_keywords('강아지', '고양이')
    crawler.execute(year=2019, month=9, number_by_date=100)
