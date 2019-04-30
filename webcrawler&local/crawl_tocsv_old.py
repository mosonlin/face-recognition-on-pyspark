import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import re
import csv
import spacy
nlp = spacy.load('en_core_web_sm')
import nltk

#--------------------get image url &caption ----------------------#
# find all of the links on a page and generate a list
# whose elements are tuples
def get_links(response):    #input 'future'
    soup = BeautifulSoup (response.text, "lxml")
    # use lxml to interpret the webpage

    # find all the links in the html,generate a list
    links = soup.find_all('span', class_='field-content')
    # 'links' is a list which contains all sublinks in one page
    # different links are between 'class=view-row ...' tags
    #both name and data have the same tag

    temp_list=[]    #links list would contain many null
    for link in links:
        temp_list.append(link.select('a'))
    str_list = list (filter (None,temp_list))   #get all the src

    # build a list,use for-loop to append different elements into the list
    final_links=[]
    for i in str_list:
        url = i[0]['href']
        final_url = "http://www.newyorksocialdiary.com" + url
        final_links.append(final_url)
        #---------test-----------#
        #print(final_url)
    #tell us how many links in each page
    #print (len (final_links))
    return final_links

def get_page_args(i):
    return {"url": url,
            "params": {"page": i}
           }

#get one page's image url
pattern=re.compile(r'^/i/partypictures.*(.jpg)$')
#begin with '/i/partypictures',ends with '.jpg'
def get_image_caption_url(link):
    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = BeautifulSoup (res.text, "lxml")
    #we use this list to do the filter
    total_image_list = soup.find_all('img')
    #use this two lists to output
    true_image_list=[]
    single_page_caption_list = []
    temp_url_list=[]
    special_list=[] #to put those with urls without <img src>
    for i in total_image_list:
        #tr is their father tree,tbody is tr's father
        # caption's fathertree tr and img's fathertree tr are paralleled
        if i.get('src'):
        # get <img src=...> but there are some urls without this
            url=i['src']
            if pattern.match(url):
                temp_url_list.append(i)
        #it's hard to delete,because only when the whole regexp doesn't fix then we can del it
        #which means we can't delete '/i/fasten.gif'
        # only when we sure they are they are images,then we will try to find their caption
        else:
            print(link) #print those special urls
            special_list.append(link)
    # print(len(temp_url_list))

    #in the same function,we need to use different local variables
    for node in temp_url_list:
        url=node['src']
        true_image_list.append(url)
        # if img's father's father's brothernode exists
        if node.parent.parent.next_sibling:
        # because image is always above caption and they are paralleled
        #so we use next_sibling to get brother nodes
            grgrparnode=node.parent.parent.parent
            # print(grgrparnode)

            #when this node exists,then we will try to find their captions in three methods
            #method 1
            if grgrparnode.find_all('div',align='center',class_="photocaption"):
                caption1=grgrparnode.find_all('div',align='center',class_="photocaption")[0].text
                #find will generate a list,use [0] to get the first element
                # print (caption1)
                # print (type (caption1))
                single_page_caption_list.append(caption1)
            #method 2
            elif grgrparnode.find_all('font',size='1',face='Verdana, Arial, Helvetica, sans-serif'):
                caption2=grgrparnode.find_all('font',size='1',face='Verdana, Arial, Helvetica, sans-serif')[0].text
                single_page_caption_list.append (caption2)
            # method 3
            elif grgrparnode.find_all('td', scope='row', class_='photocaption'):
                caption3=grgrparnode.find_all('td', scope='row', class_='photocaption')[0].text
                single_page_caption_list.append(caption3)
    # print(len(image_list))  #both 48
    # print(len(caption_list))    #both 48

    #generate a corresponding tuple
    single_page_final_list = []
    # http://www.newyorksocialdiary.com/legacy +each element to get final url
    urlpart='http://www.newyorksocialdiary.com/legacy'
    for image_url, caption in zip (true_image_list,single_page_caption_list):
        whole_image_url=urlpart+image_url
        tuple = (whole_image_url, caption)
        single_page_final_list.append(tuple)
    return single_page_final_list
# #test
# url='http://www.newyorksocialdiary.com/party-pictures/2007/the-new-york-philharmonic-symphony-space'
# testlist=get_image_caption_url(url)

#-------------------name-recognization-part-----------------#
#method 1:spacy
def spacy_name_recognition(one_caption_list):
    one_caption_name_list=[]
    for element in one_caption_list:
        doc = nlp(element)
        for ent in doc.ents:
            if (ent.label_ == 'PERSON'):
                one_caption_name_list.append(str(ent))
                #print (ent.text)
    return one_caption_name_list

#method 2:nltk
def nltk_name_recognition(text_string_list):
    #separate the article into sentences
    for sent in nltk.sent_tokenize(text_string_list):
        tokens = nltk.tokenize.word_tokenize(sent)
        #split them one word by one word
        pos = nltk.pos_tag(tokens)
        #output a tuple list (word,property）
        sent_tree = nltk.ne_chunk(pos, binary = False)
        #use classifier to recognize named entity,it'll return a nltk tree

        global person_list
        #add this,or it'll tell you local variable is assigned
        person_list=[]
        person = []
        name = ""
        for subtree in sent_tree.subtrees(filter=lambda t: t.label() == 'PERSON'):
            #we input t,only output those t.label='PERSON' t
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1:     #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '  #combine them as a whole name
                if name[:-1] not in person_list:
                    person_list.append(str(name[:-1]))
                name = ''   #clear the string
            person.clear()  #clear the list
    return person_list

#find and generate cp names
def find_cp_get_name(name_list_after_method):
    findspace = re.compile (r' ')  # if this is a husband name,there'll be a space between it
    for name in name_list_after_method:
        nameclean=name.lstrip(" ").rstrip(" ")    #clean both side
        if (name_list_after_method.index (name) < (len (name_list_after_method) - 1)):
        # if there is one typical name after it
            if(not findspace.search(nameclean)):
            #Can't find space inside it,which means it's a single name
                last_name=name_list_after_method[name_list_after_method.index(name)+1].split(" ")[-1]
                wifename=nameclean+" "+last_name
                #use new name to replace the origin on
                name_list_after_method[name_list_after_method.index(name)]=wifename
            else:
                continue
        else:   #this means it's the last one of it
            break
    #return a new name_list
    return name_list_after_method

#merge two method-generated lists together
def merge_list(spacy_list,nltk_list):
    for nltkname in nltk_list:
    #check if each name in nltk is in spacy_list
        if(nltkname in spacy_list):
        #if we can't find nltkname in spacy name
        #Which means it's a need name,we need to add it to the final list
            continue
        else:
            spacy_list.append(nltkname)
    return spacy_list

#remove the duplicate names in the same list
def remove_same_name(name_list):
    distinct_name_set=set(name_list)
    return distinct_name_set

def recognize_name(caption):
    pattern = r'\\xa0| +'
    pre_string = re.sub(pattern, ' ',caption)
    # a dirty data we need to clean,replace it with "space"

    # method 1:spacy
    #preprocessing the data as a list
    #split the caption by these misleading words
    temp_list2=re.split(r'\'|"|\n+|Dr.|Drs.|Dean|©|PhD|CEO|Director|Chairs|Chair',pre_string)
    # clean all the "null' element
    each_caption_name_list = list(filter(None,temp_list2))
    # each a caption will generate a list
    # but this list will still contain "space" element,we need to clear them
    each_caption_name_list_nospace = [x for x in each_caption_name_list if x != " "]

    #--------we can undo these part,because when recognizing,it will only find names----#
    # #drop all the 'and' element
    #each_caption_name_list_noand=[x for x in each_caption_name_list_nospace if x != "and"]

    # #clear the space on both side of the name
    each_caption_name_list_strip = [x.lstrip (" ").rstrip (" ") for x in each_caption_name_list_nospace]
    #-----------------------------------------------------------------------------------#
    spacy_recognize_list=spacy_name_recognition(each_caption_name_list_nospace)
    # check if there is couple in this list
    cp_spacy_name_list = find_cp_get_name (spacy_recognize_list)
    #print('cp_spacy_name_list:',cp_spacy_name_list)

    #method:nltk
    #preprocessing the data as a string
    prepro_nltk_string_list = re.sub(r'\'|"|\n+|Dr.|Drs.|Dean|©|PhD|CEO|Director|Chairs|Chair',' ',pre_string)

    nltk_recognize_list=nltk_name_recognition(prepro_nltk_string_list)
    #print('nltk_recognize_list:',nltk_recognize_list)

    #merge two lists(By testing:we think spacy's effect is better than nltk's)
    final_name_list=merge_list(cp_spacy_name_list, nltk_recognize_list)
    #print("final_name_list:",final_name_list)

    distinct_name_list=remove_same_name(final_name_list)
    print("finish image")
    return distinct_name_list

def polish_the_namelist(namelist):
    washed_name_list=[]
    for name in namelist:
        washedname=name.lstrip (' ').rstrip (' ').split ('\n')[0].rstrip (' ').lstrip ('\n').rstrip ('\n')
        #clean both sides
        washed_name_list.append(washedname)
    return washed_name_list

# ---------Initialize:Set the coefficients we want------------------#
url = "party-pictures"

session = FuturesSession(max_workers=5)
#the maximum crawler we use at a time
responses = [session.get(**get_page_args(i)) for i in range(33)]
#get all 32 pages,return a requests-type element in 'responses' list

#---------First----------------#
print('start getting all urls')
#put all the url in one list
total_links_list=[]
for response in responses:
    single_page_link_list=get_links(response.result())
    #right now,it's list contains list,we want to put all the links in one layer
    for single_link in single_page_link_list:
        total_links_list.append(single_link)
#print(total_links_list[:20])
#print(len(total_links_list))

# ------------Second---------------#
#put each page_list to an overall list
print('start handling')
final_image_caption_url=[]
i=1
for single_url in total_links_list:
    print ('start crawling')
    single_page_image_list=get_image_caption_url(single_url)
    print('finish {} urls!'.format(i))
    i=i+1
    final_image_caption_url.append(single_page_image_list)
    #we add a list into another list
# print(final_image_caption_url[:5])

#-------------Third--------------#
print('start polishing')
#convert data format
ultimate_format=[]

for single_url_list in final_image_caption_url:
    partyID=final_image_caption_url.index(single_url_list)
    #reset each page's index
    for im_cp_tuple in single_url_list:
        captionID=single_url_list.index(im_cp_tuple)
        # we can get tuple's element,but we can't change them
        # recognize the name and wash them
        namelist=polish_the_namelist(recognize_name(im_cp_tuple[1]))
        #each time finish one caption,it will print something
        ultimate_format.append((partyID,
                                captionID,
                                im_cp_tuple[0],   #image url
                                namelist,       #a name list
                                len(namelist)    #people num
                                ))
        print('finish one caption!')
#print(ultimate_format[:20])

#------write as csv--------------#
head=['pageID','captionID','image_url','names','number of names']

with open('image_caption_data.csv', "w", newline='') as writeFile:
    writer = csv.writer(writeFile)
    ultimate_format.insert(0, head)
    for line in ultimate_format:
        writer.writerow(line)   #transfer the list into a csv
