from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import argparse

def Checker(upc,zipcode,stores,output=None):
    ret_dict = {}
    ret_dict['Entered Zipcode'] = zipcode
    for elem in stores:
        if elem == 'Target':
            url = 'https://brickseek.com/target-inventory-checker'
        elif elem == 'Walmart':
            url = 'https://brickseek.com/walmart-inventory-checker'
        try:
            res_list = store_inventory(upc, zipcode, url)
            if not res_list:
                ret_dict[elem] = "No Available Products"
            else:
                ret_dict[elem]= res_list
            
        except:
            ret_dict[elem] = "No Availible Products"
        
    with open(output+'.txt','w') as json_file:
        json.dump(ret_dict,json_file,indent=4)


def store_inventory(upc,zipcode,url):
    driver = uc.Chrome()
    driver.get(url)
    typeA = driver.find_element(By.CSS_SELECTOR, "#main > div > form > div > div.grid__item.inventory-checker-form__method > div > div > label:nth-child(4)")
    typeA.click()

    #Enters upc and zipcode
    upc_in = driver.find_element(By.ID, 'inventory-checker-form-upc')
    upc_in.send_keys(upc)
    searchbar = driver.find_element(By.ID, 'inventory-checker-form-zip')
    searchbar.send_keys(zipcode)
    searchbar.send_keys(Keys.ENTER)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stores_list = soup.find_all('div',{'class':'table__row'})
    store_list = []

    for elem in stores_list:
        try:
            store_name= elem.find('strong').text.replace('\n','')
            addy = elem.find('address').text
            addy = addy[0:addy.index('\n\n')].replace('\n','')
            avail = elem.find('span',{'class':'availability-status-indicator__text'}).text
            if avail == 'In Stock':
                quant= elem.find('span', {'class': 'table__cell-quantity'})
            else:
                quant = 0
            price = elem.find('span',{'class':'price-formatted price-formatted--style-display'}).text
            if(elem.find('span',{'class':'table__cell-price-discount'})):
                disc = elem.find('span',{'class':'table__cell-price-discount'}).text
            else:
                disc = "No Discount"

            store_list.append({'store_name':store_name,'address':addy,'availability':avail, 'quantity': quant, 'price': price, 'discount': disc})
        except:
            continue 

    return store_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the Inventory and Price of Item\'s given a UPC value')
    parser.add_argument('--upc','-u',type=str, metavar='',required=True,help='UPC of the Item')
    parser.add_argument('--zip','-z',type=str, metavar='',required=True,help='Your Current ZipCode')
    parser.add_argument('--stores','-s',type=str, metavar='',required=True,help='Stores You want to search In', choices=['a','w','t'])
    parser.add_argument('--output','-o',type=str, metavar='',help='Output json to a given file')
    args=parser.parse_args()
    stores = []
    if args.stores =='a':
        stores.append('Walmart')
        stores.append('Target')
    elif args.stores == 't':
        stores.append('Target')
    elif args.stores == 'w':
        stores.append('Walmart')
    Checker(args.upc,args.zip,stores,args.output)