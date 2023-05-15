from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from tkinter import *
import time


root = Tk()
root.title('Amazon Scraper')
root.geometry('400x100')

keyword_entry = Entry(root, width=30)
keyword_entry.pack(pady=10)
scrape_button = Button(root, text='Scrape')
scrape_button.pack()

root.mainloop()