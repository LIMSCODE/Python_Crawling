from selenium import webdriver
import time
import random
import traceback
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import numpy
import pandas as pd 
import urllib.request
import requests
from bs4 import BeautifulSoup
import os, glob
import os.path
import cv2,numpy as np
import matplotlib.pylab as plt
from selenium.webdriver.common.action_chains import ActionChains
#from skimage.measure import compare_ssim as ssim
from skimage.metrics import structural_similarity 
import webbrowser as browser
import winsound as sd

# [웹사이트 정보 일괄저장하기 - 웹크롤링]
# 사이트에 로그인해서 특정 단어 검색후 
# 박스 하나하나당 이미지와 정보 저장하고 엑셀로 출력한다 

result = []  #찾은 결과
def scraping(driver1, search_name) :
    beepsound()
    driver1.get("https:// 웹사이트 ")
    time.sleep(1)
    
    # 로그인하기 
    idInput = 'form#formLogin > input:nth-child({})'.format(5)
    passwordInput = 'form#formLogin > input:nth-child({})'.format(6)
    driver1.find_element_by_css_selector(idInput).send_keys(' 아이디 ')
    driver1.find_element_by_css_selector(passwordInput).send_keys(' 비밀번호 ')

    loginClick = driver1.find_element_by_css_selector(".formSubmit")
    driver1.execute_script("arguments[0].click();", loginClick)

    # 검색된 목록    
    print(search_name)
    time.sleep(3)
    driver1.get("https:// 웹사이트 " + " " + " " + str(200) + " " + search_name + " ")
    time.sleep(1)

    #스크롤 맨아래까지 내리기
    driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver1.execute_script("window.scrollTo(0, 0);")

    # 현재 페이지
    curPage = 1

    # 크롤링할 전체 페이지수
    try :
        totalPage1 = driver1.find_element_by_css_selector('.page_number').text
        if (totalPage1 != '1') :
            totalPage2 = totalPage1.split("총")
            totalPage3 = totalPage2[1]
            totalPage = int(totalPage3[1:2])
            print(search_name)
            print(totalPage)
        else : 
            print(search_name)
            totalPage = 1
    except :
        pass    

    #마지막 페이지까지 모든 이미지 저장
    while curPage <= totalPage:  
        print(curPage)

        if curPage > totalPage :
            print('페이지초과')
            break

        #사진 저장할 폴더 생성  
        search_name = search_name.rstrip('\n')
        try:
            directory = "C:/Users/x" + folderName  
            if not os.path.exists(directory):
                os.makedirs(directory)
        except :
            print ("에러1")  
            pass

        try:
            directory = "C:/Users/x" + folderName  
            if not os.path.exists(directory):
                os.makedirs(directory)
        except :
            print ("에러1")  
            pass

        boxs = driver1.find_elements_by_css_selector(".sub_cont_bane1") 
        count = 0 

        # 박스 하나씩 돌면서 이미지 저장하고, 기존 폴더에 있는 이미지와 중복되는지 확인
        for box in boxs : 

            print("개수세기" + str(count))  
            if (count > 20) : 
                break 

            try :  
                Name = box.find_element_by_css_selector(".main_cont_text1").text
                
                Number1 = box.find_element_by_css_selector(".sub_cont_text1") 
                Number2 = Number1.find_element_by_css_selector(".SetListGallery_block") 
                Number = Number2.find_element_by_css_selector(".t10").text

                img_tag1 = box.find_element_by_css_selector(".bane_brd1")
                img_tag = img_tag1.find_element_by_tag_name("img")
                img_url = img_tag.get_attribute('src')

                actions = ActionChains(driver1)
                actions.move_to_element(img_tag).perform()

                search_name = search_name.rstrip('\n')
                savePath = "C:/Users/x/" + folderName + "/" + str(Number) + ".jpg"
                urllib.request.urlretrieve(img_url, savePath)

            except :  
                pass
 
            targetdir = "C:/Users/x/" + folderName
            file_list = os.listdir(targetdir)    
            
            sameornot = int(0)    
            for imageName in file_list :
                manyNumber = imageName 
               
                try :

                    #현재 커서가있는 박스의 이미지
                    img_1 = "C:/Users/x/" + folderName + "/" + str(Number) + ".jpg" 
                     
                    #기존에 저장된 박스의 이미지
                    img_2 = "C:/Users/x/" + folderName + "/" + str(manyNumber)
                       
                    dtype=np.uint8
                    img1 = cv2.imdecode(np.fromfile(img_1, dtype), cv2.IMREAD_COLOR)
                    img2 = cv2.imdecode(np.fromfile(img_2, dtype), cv2.IMREAD_COLOR)

                    #현재 커서에서 저장한 이미지 자기자신이면 건너뛴다. (+1 되는것 방지)
                    if (str(manyNumber) == str(Number) + ".jpg") :
                        continue
                
                    #이미지일치하는게 있으면, sameornot을 1로 바꾼다. 
                    tempDiff = cv2.subtract(img1, img2)
                    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                    (score, diff) = structural_similarity(grayA, grayB, full = True)
                    diff = (diff * 255).astype("uint8") 
                    Similarity = score  
                    assert score, "다른점 찾을수없음"
                    print(Similarity)

                    #이미지 일치시 sameornot을 1로바꿈
                    if (Similarity > 0.8) :
                        sameornot += 1
                      
                except: 
                    pass

            print(sameornot)
            if (sameornot > 0) :
                continue

            try : 
 
                # 페이지 길이 측정 
                click1 = box.find_element_by_css_selector(".sub_cont_text1")  
                click = click1.find_element_by_css_selector(".main_cont_text1") 
                driver1.execute_script("arguments[0].click();", click)
                    
                driver1.switch_to.window(driver1.window_handles[-1])
                time.sleep(2)
                driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # 현재 스크롤 전체 길이 추출 
                newHeight = driver1.execute_script("return window.pageYOffset")
                print(newHeight)

                # 페이지 길이가 8000 이상일때 
                if (newHeight > 8000) : 

                    #이미 저장된 이미지들과 일치하지 않는다면, (sameornot 이 1보다 작다) 이미지 최종저장하고, 엑셀로 저장   
                    search_name = search_name.rstrip('\n')
                    savePath = "C:/Users/x/" + folderName + "/" + str(Number) + ".jpg"
                    urllib.request.urlretrieve(img_url, savePath)
                    print('이미지저장완료')
      
                    lists = [search_name, Number, Name, newHeight]
                    result.append(lists)

                    print('결과')
                    print(result)
                    data = pd.DataFrame(result)      
                    data.columns = ['검색명', '번호', '이름', '길이']
                    data.to_csv("C:/Users/x.csv", encoding='cp949')
                    print('엑셀저장완료') 

                    count = count + 1

                    #원래창으로 돌아가기
                    driver1.close()
                    driver1.switch_to.window(driver1.window_handles[0])
                    time.sleep(3)
                    print("원래창으로 돌아옴.................")

                    #체크박스클릭
                    check1 = box.find_element_by_css_selector(".input_check3_") 
                    check = check1.find_element_by_css_selector(".input_check3")   
                    driver1.execute_script("arguments[0].click();", check)
                
                    time.sleep(1)

                    #DB담기 클릭
                    intoDB1 = driver1.find_element_by_css_selector(".footer_position2_bg")
                    intoDB2 = intoDB1.find_element_by_css_selector(".container > ul > li")
                    intoDB = intoDB2.find_element_by_css_selector(".footer_position_btn1")
                    driver1.execute_script("arguments[0].click();", intoDB)
                    driver1.execute_script("arguments[0].click();", intoDB)
                    time.sleep(1)

                    #페이지머무르기 클릭   
                    stayPage1 = driver1.find_element_by_css_selector("#pup_images_alert")
                    stayPage2 = stayPage1.find_element_by_css_selector(".container")
                    stayPage3 = stayPage2.find_element_by_css_selector(".scroll_bar1")
                    stayPage3 = stayPage2.find_element_by_tag_name('div')
                    stayPage = stayPage3.find_element_by_tag_name('a')
                    driver1.execute_script("arguments[0].click();", stayPage)
                    driver1.execute_script("arguments[0].click();", stayPage)
                    time.sleep(1)

                    print("DB넣고 페이지머무르기 완료.............")
                    time.sleep(3)            

                else :
                    #원래창으로 돌아가기
                    driver1.close()
                    driver1.switch_to.window(driver1.window_handles[0])
                    time.sleep(3)
                    print("원래창으로 돌아옴.................")
                    
            except :
                pass
                        
           

        if curPage != 1 :
            curPage1 = curPage + 2

        try :
            # 페이지 이동 클릭
            if (totalPage1 != '1') :
                if (curPage == 1) : 
                    curPage1 = curPage + 1
                    cur_css = 'div.page_number > a:nth-child({})'.format(curPage1)
                    element = driver1.find_element_by_css_selector(cur_css) 
                    driver1.execute_script("arguments[0].click();", element)
                    curPage += 1 
                else :
                    curPage1 = curPage1 + 1
                    cur_css = 'div.page_number > a:nth-child({})'.format(curPage1)
                    element = driver1.find_element_by_css_selector(cur_css) 
                    driver1.execute_script("arguments[0].click();", element)
                    curPage += 1 

            else :
                curPage += 1    
        except :
            print ("에러5")  
             
            pass
  

def crawl(search_name):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    driver1 = webdriver.Chrome('C:/Users/chromedriver.exe')   
 
    scraping(driver1, search_name)
      
def beepsound():
    fr = 2000    # range : 37 ~ 32767
    du = 1000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)
     

file = open('get__.txt', 'r', encoding='UTF8')
lines = file.readlines() 


for idx1,search_name in enumerate(lines):
 
    idx = idx1 + 9
    if (9 <= idx and idx <= 12) :
        folderName = "aa" 

    crawl(search_name)  #한줄씩 검색에 넣음
 
 
