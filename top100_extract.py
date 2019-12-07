from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import csv

options = Options()
options.headless = False
pwd = os.getcwd()
pwd=pwd+'/geckodriver'
driver = webdriver.Firefox(options=options, executable_path=pwd)
driver.get("https://www.ncbi.nlm.nih.gov/gene")
driver.implicitly_wait(5)

def create_file(content,x):
    f= open(x,"w+")
    for c in content:
        print("Writing content in",x)
        f.write(c.text)
    f.close()

with open('GMB.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if(line_count<100):
            x=row[0]
            driver.find_element_by_xpath("//*[@id='term']").clear()
            driver.find_element_by_xpath("//*[@id='term']").send_keys(x) 
            driver.find_element_by_xpath("//*[@id='search']").click()
            driver.implicitly_wait(5)
            try:
                driver.find_element_by_xpath("/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[6]/div[2]/div[3]/div/div/div[3]/div/p/a[2]").click()
                driver.implicitly_wait(5)
                content = driver.find_elements_by_xpath("/html/body/div/div[1]/form/div[1]/div[4]/div/div[5]/div[2]/div[1]/pre")
                create_file(content,x)
            except:
                try:
                    driver.find_element_by_css_selector("#feat_gene_title").click()
                    driver.implicitly_wait(5)
                    driver.find_element_by_link_text("FASTA").click()
                    driver.implicitly_wait(5)
                    content = driver.find_elements_by_xpath("/html/body/div/div[1]/form/div[1]/div[4]/div/div[5]/div[2]/div[1]/pre")
                    driver.implicitly_wait(5)
                    create_file(content,x)
                except:
                    print(x,"gene not found")
            line_count+=1    
            print(line_count)
        else:
            break