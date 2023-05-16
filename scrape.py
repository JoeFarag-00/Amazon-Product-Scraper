from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from tkinter import *
import time
import os
from selenium.common.exceptions import NoSuchElementException
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')


def Scrape_Amazon():
    keyword = keyword_entry.get()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.amazon.co.uk/s?k={keyword}')

    ct = 0
    pdct=0
    time.sleep(1)

    product_elements = driver.find_elements(
        By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')

    products = []
    for element in product_elements:
        try:
            try:
                product_page = element.find_element(
                    By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').get_attribute('href')
                print(product_page)
            except NoSuchElementException:
                product_page = "NULL"

            try:
                product_name = element.find_element(
                    By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal').text
                company_name = product_name.split(' ')[0]
            except NoSuchElementException:
                product_name = "NULL"
                company_name = "NULL"

            try:
                price = element.find_element(
                    By.CSS_SELECTOR, 'span.a-price-whole').text
            except NoSuchElementException:
                price = "NULL"

            try:
                rating = element.find_element(
                    By.CSS_SELECTOR, 'span[aria-label*=" out of 5 stars"]').get_attribute('aria-label').split(' out of 5 stars')[0]
            except NoSuchElementException:
                rating = "NULL"

            try:
                product_image = element.find_elements(
                    By.CSS_SELECTOR, 'div[data-component-type="s-search-result"] img')[0].get_attribute('src')
            except NoSuchElementException:
                product_image = "NULL"

            products.append([product_page, product_name,
                            company_name, price, rating, product_image])
            pdct += 1
        except:
            ct += 1

    print(f"Passed Scrapes: {pdct}")
    print(f"Failed Scrapes: {ct}")
    print('\n')
    for p in products:
        print(p)

    driver.quit()

    csv_path = 'products.csv'
    if os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            pass

    with open('products.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Page', 'Product Name',
                        'Company Name', 'Price', 'Ratings', 'Product Image'])
        writer.writerows(products)


mainPage = customtkinter.CTk()
mainPage.title('Amazon Scraper')
mainPage.geometry('600x225')
ScreenSizeX = mainPage.winfo_screenwidth()
ScreenSizeY = mainPage.winfo_screenheight()

TitleLabel = customtkinter.CTkLabel(mainPage, text='Amazon Scraper', font=('Times New Roman', 35, 'bold'))
TitleLabel.pack(pady=10)
keyword_entry = customtkinter.CTkEntry(mainPage, width=500, height=50)
keyword_entry.pack(pady=10)
scrape_button = customtkinter.CTkButton(
    mainPage, text='SCRAPE!', command=Scrape_Amazon, font=('Consolas', 32, 'bold'), width=500, height=50, fg_color='darkgreen')
scrape_button.pack()

mainPage.mainloop()
