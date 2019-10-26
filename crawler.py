from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import urllib.request
import calendar
import re
import os


class NaverImageCrawler:
    def __init__(self):
        self.driver = None
        self.keyword_list = ['강아지', '고양이']
        self.search_url = 'https://search.naver.com/search.naver?where=image&section=image&query={keyword}\
        &res_fr=0&res_to=0&sm=tab_opt&face=0&color=0&ccl=0&nso=so%3Ar%2Cp%3Afrom{date}to{date}%2Ca%3Aall'
        self.driver_path = './driver/chromedriver.exe'
        self.img_file_directory = './images/'

    def print_log(self, *log_msg):
        print(datetime.today().strftime("%Y/%m/%d %H:%M:%S"), *log_msg)

    def execute(self, year, month):
        self.print_log('Start Naver Image Crawling.')
        self.open_browser()
        last_day = calendar.monthrange(year, month)[1]
        for day in range(1, last_day + 1):
            date = self.convert_to_string_date(year, month, day)
            for keyword in self.keyword_list:
                self.search_tag(keyword, date)
                link_list = self.down_scroll_and_get_img_links()
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
        self.print_log('Search {keyword} on {date}'.format(keyword=keyword, date=date))
        self.driver.get(self.search_url.format(
            keyword=keyword,
            date=''.join(date)
        ))
        self.driver.implicitly_wait(10)
        sleep(5)

    def down_scroll_and_get_img_links(self, target_number_of_links=50):
        self.print_log('Getting image link list.')
        scroll_pos = 1
        links_list = []
        patient = target_number_of_links / 5
        while len(links_list) < target_number_of_links:
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
        target_directory = self.img_file_directory + keyword + '/'
        if not os.path.isdir(target_directory):
            os.mkdir(target_directory)
        for link in link_list:
            file_name = link[-26:-16]
            urllib.request.urlretrieve(link, target_directory + file_name + '.jpg')
            self.print_log(file_name + ' is saved.')
            sleep(0.1)

    def close_browser(self):
        self.print_log('Closing Chrome Browser.')


if __name__ == '__main__':
    crawler = NaverImageCrawler()
    crawler.execute(2019, 1)
