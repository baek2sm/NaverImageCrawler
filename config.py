import platform


class CrawlerConfig:
    def __init__(self):
        self.search_url = 'https://search.naver.com/search.naver?where=image&section=image&query={keyword}\
                &res_fr=0&res_to=0&sm=tab_opt&face=0&color=0&ccl=0&nso=so%3Ar%2Cp%3Afrom{date}to{date}%2Ca%3Aall'
        self.download_directory = './images/'
        if platform.system() == 'Windows':
            self.driver_path = './driver/chromedriver.exe'
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.driver_path = './driver/chromedriver'
