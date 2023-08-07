# img crawling test

import sys
import os
import argparse
import time
import random

import urllib.request
import urllib.error
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#############################################
### Set timeout of urllib.request.retrive ###
#############################################
import socket
socket.setdefaulttimeout(4)

#######################################################
### This codes for ssl authorization error handling ###
#######################################################
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

######################
### Directory info ###
######################
current_parent_dir = os.getcwd()

#################
### Arguments ###
#################
# args parsing
def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labels', nargs='+', type=str, help='class names')
    parser.add_argument('--num', type=int, help='the maximum number of collected image of each label')
    parser.add_argument('--keywords', nargs='+', type=str, help='keywords combined with class name; "class name + keyword" will be searched.')
    pars = parser.parse_args()
    print(vars(pars))
    return pars

# check keywords from arguements
def name_parsing(names):
    name_list = []
    if len(names) == 1 and names[0][-4:] == '.txt': # labels file
        if os.path.exists(names[0]):
            label_file = open(names, 'r')
            while True:
                line = label_file.readline()                
                if not line: break
                line = list(line.strip().split())
                name_list = name_list + line
            label_file.close()
        else:
            print('Error: No labels file directories')
            exit(1)
    elif len(names) < 1:
        print('Error: No label')
        exit(1)
    else:
        name_list = names
    print('Name list is successfully parsed : ', end = '')
    print(name_list)
    return name_list

#################################
### Check keywords input file ###
#################################
# If there is no input file, then create the default keywords input files.
def createWordsFile(names : list, keywords : list):
    for name in names:
        file_name = current_parent_dir + '\\search_words\\' + name + '.txt'
        try:
            if not os.path.exists(file_name):
                file = open(file_name, 'w')
                if keywords == None:
                    file.write(name)
                else:
                    for keywords in keywords:
                        file.write(name + ' ' + keywords, '\t')
                file.close()
                print('Create:' + file_name)
            else: print("Exception: There is same file :" + name)
        except OSError:
            print("Error: Failed to create the word file :" + name)

################################
### Create keyords dataframe ###
################################
# Read the input text file and add row of the label into dataframe
def readWords(names : list):
    cols = ['name', 'words']
    values = []
    for name in names:
        file_name = current_parent_dir + '\\search_words\\' + name + '.txt'
        current_words = []
        try:
            if os.path.exists(file_name):
                file = open(file_name, 'r')
                while True:
                    line = file.readline()                
                    if not line: break
                    line = list(line.strip().split('\t'))
                    current_words = current_words + line
                    print(name)
                file.close()
                print(file_name + 'is read successfully.')
            else: print("Error: There is no file: " + file_name)
        except OSError:
            print("Error: Failed to create the word file :" + name)
        
        # add label name and keywords into row
        value = [name]
        value.append(current_words)
        values.append(value)
    df_words = pd.DataFrame(values, columns=cols)
    return df_words

######################
###### Crawling ######
######################
# send download request
def send_request(img_src, folder_name, name, cnt):
    print("\nrequest sent : ", img_src[:10], "..", img_src[-10:], "(", cnt, ")")
    
    def _progress(count, block_size, total_size):
      sys.stderr.write('\r>> Downloading %s %.1f%%' % (
          img_src[:10], float(count * block_size) / float(total_size) * 100.0))
      sys.stderr.flush()
    try:
        urllib.request.urlretrieve(img_src, folder_name + '\\' + name + str(cnt) + '.jpg', _progress)
    except urllib.error.HTTPError as e:
        print(e.code, "(HTTP Error) occurs; The request is failed.")
    except urllib.error.URLError as e:
        print(e.code, "(URL Error) occurs; The request is failed.")

# crawling
def crawling(name : str, keywords : list, max_cnt : int = 100):
    # Create folder to store images of the class.
    folder_name = current_parent_dir + '\\images\\' + name
    try:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print("Create Folder:" + folder_name)
        else: print("Exception: There is same folder :" + name)
    except OSError:
        print("Error: Failed to create the folder" + name)
    
    # Create or get source list for preventing duplicate images from being collected.
    src_list_txt_name = folder_name + '\\' + name + '_src list.txt'
    
    cnt = 0
    fail_cnt = 0
    for keyword in keywords:
        print('Start Crawling: keyword ' + keyword)
        load_time = 4
        if not os.path.exists(current_parent_dir + '\\chromedriver.exe'):
            print('Error: Chromedriver need to installed.')
            return
        driver = webdriver.Chrome() # Caution!: in the main dir, chrome driver have to be located.
        driver.get("https://www.google.co.kr/imghp") # Google image search url.
        search_bar = driver.find_element(By.NAME, "q") # Select the search bar.
        search_bar.send_keys(keyword) # Put the keyword in the search bar.
        search_bar.send_keys(Keys.RETURN) # Click 'return' button.
        time.sleep(load_time) # Wait for loading the result page.
        
        # Scrolling
        # It is stopped if the number of loaded images is greater or equal than the maximum number
        # or meet the end of page.
        last_hegiht = driver.execute_script("return document.body.scrollHeight")
        imgs = []
        while True :
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(load_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height - last_hegiht > 0 :
                last_hegiht = new_height
                continue
            else :
                imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # Select all small images.
                print('Scrolling.. Find ' + str(len(imgs)) + ' images of ' + name)
                if len(imgs) > max_cnt * 2:
                    print('Find' + str(len(imgs)) + 'images of' + name)
                    break
                try:
                    time.sleep(load_time + 2)
                    # 2023.07.04 Update
                    # The suffix of CSS SELECTOR of 'more' button is updated.
                    # previous: driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
                    driver.find_element(By.CSS_SELECTOR, ".LZ4I").click()
                except:
                    break
        
        # Redetect all small images.
        time.sleep(load_time)
        imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # Select all small images(elements).
        print('Finally, Find  ' + str(len(imgs)) + '  images of  ' + keyword)

        # Download images
        for img in imgs:
            try:
                img.click()
                # Prevent websites consider the crawler as bot.
                # For this, change the wait time randomly.
                print('image click successes..', end = '')
                load_rand_time = random.uniform(1.5, 4)
                time.sleep(load_rand_time)
                # 2023.07.04 Update
                # XPATH of the source url is updated.
                # So, get the source url from the elements of small image.
                # previous: img_elem = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
                img_elem = img
                img_src = img_elem.get_attribute('src')
                print('\nFinding source successes..\nStart overlapping check..')
            except:
                fail_cnt += 1
                print('File loading fails.')
                continue
            
            # Check whether the image was collected.
            isOverlapped = False
            if os.path.exists(src_list_txt_name):
                file = open(src_list_txt_name, 'r')
                while True:
                    line = file.readline()
                    line_seg = list(line.split())
                    if len(line_seg) < 2:
                        break
                    if line_seg[1] == img_src:
                        isOverlapped = True
                        break
                file.close()
            if isOverlapped:
                print('This img is already downloaded.')
                fail_cnt += 1
                continue
            else:
                print('This img is bandnew..', end = '')
            
            # Send request to download the image.
            send_request(img_src, folder_name, name, cnt)
            
            # If the download is succes.
            if os.path.exists(folder_name + '\\' + name + str(cnt) + '.jpg'): 
                # Store source url in source url list file.
                isFirstWriting = False
                if not os.path.exists(src_list_txt_name):
                    isFirstWriting = True
                try:
                    file = open(src_list_txt_name, 'a')
                    if not isFirstWriting:
                        file.write('\n')
                    file.write(str(cnt) + '\t' + img_src)
                    file.close()
                    print('Current image and its source is stored successfully..')
                    cnt += 1
                except OSError:
                    print("Error: Failed to store the src list file :" + name)
            else:
                fail_cnt += 1
                print("Storing is failed.")
            print("SUCCESS: " + str(cnt) + " / FAIL: " + str(fail_cnt) + " of " + str(len(imgs))
                  + " to " + str(max_cnt) + " images")
                
            if cnt >= max_cnt:
                break
            
        driver.close()
        
        if cnt >= max_cnt:
            break
        else:
            time.sleep(load_time)
            

def main(pars):
    name_list = pars.labels
    name_list = name_parsing(name_list)
    keyword_list = pars.keywords
    createWordsFile(name_list, keyword_list)
    df_keywords = readWords(name_list)
    
    max_cnt = pars.num
    for name in name_list:
        row_idx = df_keywords.index[(df_keywords['name'] == name)][0]
        keywords = df_keywords.at[row_idx, 'words']
        crawling(name, keywords, max_cnt)
        print('Crawling over : ' + name)
    
    return 0

if __name__ == '__main__':
    pars = parsing()
    main(pars)