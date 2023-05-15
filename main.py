from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from tkinter import *
import time
from selenium.common.exceptions import NoSuchElementException

def Scrape_Amazon():
    keyword = keyword_entry.get()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.amazon.co.uk/s?k={keyword}')
    
    ct = 0
    time.sleep(1)
    
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
 
    products = []
    for element in product_elements:
        try:
            try:
                product_page = element.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').get_attribute('href')
            except NoSuchElementException:
                product_page = "Lost"
            
            try:
                product_name = element.find_element(By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal').text
            except NoSuchElementException:
                product_name = "Lost"
            
            try:
                price = element.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
            except NoSuchElementException:
                price = "Lost"
            
            try:
                rating = element.find_element(By.CSS_SELECTOR, 'span[aria-label*=" out of 5 stars"]').get_attribute('aria-label').split(' out of 5 stars')[0]
            except NoSuchElementException:
                rating = "Lost"
            # company_name = element.find_element(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"] span.a-size-small.a-color-secondary.a-text-normal').text.split('by ')[-1]# NOT Scrapable
            try:
                product_image = element.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"] img')[0].get_attribute('src')
            except NoSuchElementException:
                product_image = "Lost"
                
            products.append([product_page, product_name, price, rating, product_image])
        except:
            ct+=1
    
    print("Failed Scrapes: ", ct)
    
    print(products)

    driver.quit()

    with open('products.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Page', 'Product Name','Price', 'Ratings', 'Product Image'])
        writer.writerows(products)

root = Tk()
root.title('Amazon Scraper')
root.geometry('400x100')

keyword_entry = Entry(root, width=30)
keyword_entry.pack(pady=10)
scrape_button = Button(root, text='Scrape', command=Scrape_Amazon)
scrape_button.pack()

root.mainloop()
