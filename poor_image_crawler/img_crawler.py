import sys
import os
import threading
import ctypes
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
print(current_parent_dir)

#################################
### Default classes and names ###
#################################
name_list = ['Fly', 'Ant', 'Cicade', 'Butterfly', 'Beetle','Stag Beetle', 'Ladybug', 
             'Dragonfly', 'Spider', 'Cockroach', 'Mosquito', 'Mantis', 'Cricket', 
             'Grasshoper', 'Korean Grasshoper', 'Bee', 'Firefly', 'Water Strider',
             'Scorpion', 'Diving Beetle', 'Snail', 'Earthworm', 'Longhorn Beetle',
             'Centipede', 'Camel Cricket']
korean_name_list = ['파리', '개미', '매미', '나비', '장수풍뎅이', '사슴벌레', '무당벌레',
                    '잠자리', '거미', '바퀴벌레', '모기', '사마귀', '귀뚜라미',
                    '메뚜기', '여치', '벌', '반딧불이', '소금쟁이', '전갈', '물방개',
                    '달팽이', '지렁이', '하늘소', '지네', '곱등이']

# mapping korean names and english names.
eng_to_kor_dict = {}
for i in range(len(name_list)):
    eng_to_kor_dict[name_list[i]] = korean_name_list[i]
name_list.sort()

print(name_list)

#################################
### Check keywords input file ###
#################################
# If there is no input file, then create the default keywords input files.
def createWordsFile(bug_name : str):
    file_name = current_parent_dir + '\\search_words\\' + bug_name + '.txt'
    try:
        if not os.path.exists(file_name):
            file = open(file_name, 'w')
            file.write(eng_to_kor_dict[bug_name] + ' 해충\t')
            file.write(eng_to_kor_dict[bug_name] + ' 곤충\t')
            file.write(eng_to_kor_dict[bug_name] + '\t')
            
            file.close()
            
            print('Create:'+file_name)
        else: print("Exception: There is same file :" + bug_name)
    except OSError:
        print("Error: Failed to create the word file :" + bug_name)
for bug_name in name_list:
    createWordsFile(bug_name)
    

################################
### Create keyords dataframe ###
################################
cols = ['name', 'words']

# Read keywords input files
def readWords(bug_name : str):
    file_name = current_parent_dir + '\\search_words\\' + bug_name + '.txt'
    current_words = []
    try:
        if os.path.exists(file_name):
            file = open(file_name, 'r')
            while True:
                line = file.readline()                
                if not line: break
                line = list(line.strip().split('\t'))
                current_words = current_words + line
                print(bug_name)
            file.close()
            print(file_name + 'is read successfully.')
        else: print("Error: There is no file: " + file_name)
    except OSError:
        print("Error: Failed to create the word file :" + bug_name)
    return current_words

values = []
for bug_name in name_list:
    value = [bug_name]
    value.append(readWords(bug_name))
    values.append(value)
    
df_words = pd.DataFrame(values, columns=cols)

###############################
###### Thread to requset ######
###############################
# Terminate the threads of request
def thread_terminate(thread_id):
    if thread_id is not None:
        thread_id = ctypes.c_long(thread_id)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Failed to terminate request thread.")
    else:
        print("Invalid thread ID.")

# Send request with handling HTTP, URL error.
def send_request(img_src, folder_name, bug_name, cnt):
    print("\nrequest sent : ", img_src[:10], "..", img_src[-10:], "(", cnt, ")")
    
    # progress bar
    def _progress(count, block_size, total_size):
      sys.stderr.write('\r>> Downloading %s %.1f%%' % (
          img_src[:10], float(count * block_size) / float(total_size) * 100.0))
      sys.stderr.flush()
    try:
        # send request
        urllib.request.urlretrieve(img_src, folder_name + '\\' + bug_name + str(cnt) + '.jpg', _progress)
    except urllib.error.HTTPError as e:
        print(e.code, "(HTTP Error) occurs; The request is failed.")
    except urllib.error.URLError as e:
        print(e.code, "(URL Error) occurs; The request is failed.")

# This function directly used for calling request.
# Create the thread for 'send_request' function, and run.
# If wait time is over, terminate the thread.
def check_request_timeout(img_src, folder_name, bug_name, cnt):
    urlrq_thread = threading.Thread(target=send_request, args=(img_src, folder_name, bug_name, cnt,))
    urlrq_thread.start()

    # Wait for 5 seconds
    time.sleep(5)
    isStopped = False
    if urlrq_thread.is_alive():
        # Timeout occurred, stopping the func1 thread
        isStopped = True
        print(img_src[:10] + ".." + img_src[-10:] +
              " : request took too long to execute! Stopping the thread...")
        rq_thread_id = urlrq_thread.ident
        thread_terminate(rq_thread_id)

    urlrq_thread.join()
    if isStopped:
        print("request was stopped.")
    else: print("request has completed.")
    
#############
### Crawl ###
#############

# Get the class name and upper bound of the number of collected images.
def crawling(bug_name : str, max_cnt : int = 100):
    # Create folder to store images of the class.
    folder_name = current_parent_dir + '\\images\\' + bug_name
    try:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print("Create Folder:" + folder_name)
        else: print("Exception: There is same folder :" + bug_name)
    except OSError:
        print("Error: Failed to create the folder" + bug_name)

    # Find keywords of the class in the keyword dataframe.
    row_idx = df_words.index[(df_words['name'] == bug_name)][0]
    keywords = df_words.at[row_idx, 'words']
    
    # Create or get source list for preventing duplicate images from being collected.
    src_list_txt_name = folder_name + '\\' + bug_name + '_src list.txt'
    
    cnt = 0       # Success count
    fail_cnt = 0  # Fail count
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
            time.sleep(load_time)  # Wait for loading.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height - last_hegiht > 0 :
                last_hegiht = new_height
                continue
            else :
                imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # Select all small images.
                print('Scrolling.. Find ' + str(len(imgs)) + ' images of ' + bug_name)
                if len(imgs) > max_cnt * 2:
                    print('Find' + str(len(imgs)) + 'images of' + bug_name)
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
        imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
        print('Finally, Find ' + str(len(imgs)) + ' images of ' + bug_name)

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
            check_request_timeout(img_src, folder_name, bug_name, cnt)
            
            # If the download is succes.
            if os.path.exists(folder_name + '\\' + bug_name + str(cnt) + '.jpg'): 
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
                    print("Error: Failed to store the src list file :" + bug_name)
            else:
                fail_cnt += 1
                print("Storing is failed.")
            print("SUCCESS: " + str(cnt) + " / FAIL: " + str(fail_cnt) + " of " + str(len(imgs))
                  + " to " + str(max_cnt) + " images")
                
            if cnt >= max_cnt:
                break
            
        driver.close()
        
        if cnt > max_cnt:
            break
        else:
            time.sleep(load_time)
            
# 전체 크롤링
# for bug_name in name_list:
#    crawling(bug_name, 10000)

# 2023.07.06 검색어 잘못해놔서 Cricket (index = 8)부터 모으면 됨.
# 2023.07.27 검색어 잘못해놔서 Mosquito (index = 18)부터 모으면 됨.
for i in range(18, len(name_list)):
   crawling(name_list[i], 10000)