from datetime import datetime
import selenium


class NaverImageCrawler:
    def __init__(self):
        pass

    def print_log(self, *log_msg):
        print(datetime.today().strftime("%Y/%m/%d %H:%M:%S"), *log_msg)

    def open_browser(self):
        self.print_log('Opening Chrome Browser.')

    def close_browser(self):
        self.print_log('Closing Chrome Browser.')


if __name__ == '__main__':
    crawler = NaverImageCrawler()