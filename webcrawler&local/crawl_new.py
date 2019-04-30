import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import re
import csv
import spacy
nlp = spacy.load('en_core_web_sm')
import nltk
import xpath

# test_url='https://www.newyorksocialdiary.com/an-all-american-festival-at-jay-heritage-center/'

root_url='https://www.newyorksocialdiary.com/category/party-pictures/page/{}/'
#--------------------get image url &caption ----------------------#
def get_page_index(rooturl):
    index_list=[rooturl.format(i) for i in range(7)]
    finalindexlist=[]
    for url in index_list:
        print('start crawling')
        response=requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup (response.text, "lxml")
        links=soup.find_all(class_='post-content')
        if len(links)>0:    #make sure there are links in this page
            for i in links:
                if i.find ('a'):
                    link=i.find('a')['href']
                    # print(link)
                    finalindexlist.append(link)
                else:
                    continue
        else:
            break
    return finalindexlist

def get_image_caption(single_page_url):
    print('start getting captions&images')
    pattern=re.compile(r'^http.*(.jpg)')
    #some begin with http,some with https;'.jpg' inside means it is the url we want
    res = requests.get(single_page_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup (res.text, "lxml")
    #we use this list to do the filter
    total_image_list = soup.find_all('img')
    fixed_image_list=[]

    for image in total_image_list:
        if image.get('src'):
            #filter other unrelated links
            image_url = image['src']
            if pattern.match(image_url):
                #we put this node into the list
                fixed_image_list.append(image)
                # print(image_url)

    page_image_caption_list = []
    for node in fixed_image_list:
        #only add nodes with image & captions
        if node.find_parent('figure'):
            fathernode=node.find_parent('figure')
            #iterativly to find parent node
            caption=fathernode.find('figcaption').get_text()
            # print(caption)
            tuple=(node['src'],caption)
            page_image_caption_list.append(tuple)
    print('finish one page')
    #print to test if we get something
    print(page_image_caption_list[:2])
    return page_image_caption_list

#get all the page links
indexlist=get_page_index(root_url)
# print(indexlist)

#download each page's caption and image
image_caption_url_list=[]
for single_page in indexlist:
    single_page_list=get_image_caption(single_page)
    image_caption_url_list.append(single_page_list)

#clean the data
final_result=[]
for single_page_list in image_caption_url_list:
    pageID=image_caption_url_list.index(single_page_list)
    for each_image in single_page_list:
        captionID=single_page_list.index(each_image)
        final_tuple=(pageID,captionID,each_image[0],each_image[1])
        #pageID,captionID,image_url,caption
        final_result.append(final_tuple)

head=['pageID','captionID','image_url','caption']
#write as a csv
with open('new_image_caption_data.csv', "w", newline='') as writeFile:
    writer = csv.writer(writeFile)
    final_result.insert(0, head)
    for line in final_result:
        writer.writerow(line)   #transfer the list into a csv
