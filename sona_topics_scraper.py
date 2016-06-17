# SONA topics scraper
# Using selenium and PhantomJS

import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Some xpath and css selectors:
MAIN_XPATH = '//dd[1]'
TOGGLE_XPATH = '//dd'
CHECKBOX_XPATH = '//input[@data-id]'
PANEL_CSS = "div[class='chart panel']"
INFO_CSS = 'p'
HEAD_CSS = 'h2'
VALUES_CSS = 'ul'

URL = 'http://malacanang.gov.ph/sona-content-charts-and-word-clouds/'


class SonaTopicScraper(object):
    
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.url = URL
        self.data = []
    
    
    def scrape(self):
        
        try:
            print 'Accessing page...'
            
            self.driver.get(self.url)
            self.wait_for_element(By.XPATH, MAIN_XPATH, wait_time=60)
            self.toggle_all_presidents()    # make all checkboxes visible
            
            print 'Parsing...'
            
            for cb in self.driver.find_elements_by_xpath(CHECKBOX_XPATH):
                data_id = cb.get_attribute('data-id')
                print '-- Now at: %s' % data_id
                
                if not cb.is_selected():
                    cb.click()
                
                item = self.start_parse()
                self.data.append(item)
                cb.click()
                sleep(2)
                
                print 4*' ' + '- Added item: %s' % data_id
            
        except Exception, e:
            print '\a%s' % e
        
        else:
            
            with open('output_data.json', 'w') as f:
                json.dump(self.data, f)
            
            print 'Finished: Data saved to file.'
        
        finally:
            print 'Exiting.'
            self.driver.quit()
    
    
    def wait_for_element(self, find_by, expression,
                            wait_time=10, parent=None):
        
        base = self.driver if parent is None else parent
        
        return WebDriverWait(base, wait_time).until(
                EC.presence_of_element_located(
                    (find_by, expression)))
    
    
    def toggle_all_presidents(self):
        
        for x in self.driver.find_elements_by_xpath(TOGGLE_XPATH):
            x.find_element_by_xpath('a').click()
            sleep(1)
    
    
    def start_parse(self):
        elem = self.wait_for_element(By.CSS_SELECTOR, PANEL_CSS)
        
        print 4*' ' + '- Collecting fields...'
        self.driver.save_screenshot('screenshot_of_parsing.png')
        self.wait_for_element(By.CSS_SELECTOR, INFO_CSS, parent=elem)
        
        info = elem.find_elements_by_css_selector(INFO_CSS)
        vals = self.wait_for_element(By.CSS_SELECTOR, VALUES_CSS,
                                        parent=elem)
        head = self.wait_for_element(By.CSS_SELECTOR, HEAD_CSS,
                                        parent=elem)
        
        item = {}
        item['author'] = head.text
        item['title'] = info[0].text.strip()
        item['delivered'] = info[1].text.strip()
        item['topics'] = {u.split('-')[0].strip():u.split('-')[1].strip()
                            for u in vals.text.split('\n')}
        
        return item


if __name__ == '__main__':
    scraper = SonaTopicScraper()
    scraper.scrape()
