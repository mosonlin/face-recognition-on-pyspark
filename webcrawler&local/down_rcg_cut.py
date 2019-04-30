import face_recognition
import pandas as pd
from os import listdir
from os.path import isfile, join
import cv2
import os
import requests
from itertools import zip_longest
from PIL import Image
import ntpath

csv_location='image_caption_data.csv'    #the one only with caption result
#read the csv to get urls
df=pd.read_csv(csv_location,usecols=['image_url'])

#where the images are stored
image_folder_location="/Users/linzhengyang/Desktop/document/bigdata/project2/code/data/image/"

#download the images,nominate it with its page&caption
def download_image(df):
    i = 0
    for row in df.iterrows():   #iterate by rows
        if i<=30500:
            image_name = 'image_page{0}_caption{1}.jpg'.format(row[1][0],row[1][1])
            #row[0] is the index, the following part would be a list,we need to choose twice
            #nominate the images with pageID & captionID
            response = requests.get(row[1][2],stream=True)
            #get the image_url
            if response.status_code == 200:     #get the picture
                with open (''.join([image_folder_location,image_name]), 'wb') as f:
                    f.write (response.content)
                f.close()
                i=i+1
                print(i)
            else:
                continue
    #recognize face for a single image

#get one imag's name & location
def path_leaf(path):
    head, tail = ntpath.split(path)
    return head,tail

#cut faces
def cut_faces(result_list,image_to_pre):
    i = 0
    pro_img = cv2.imread(image_to_pre,cv2.IMREAD_UNCHANGED)
    # openCV uses BGR as its default colour order for images
    # matplotlib uses RGB

    # cv2.imshow('origin',pro_img)
    #have to read it before we use it,or this name would be changed
    filelocation, filename = path_leaf (image_to_pre)
    file_name = filename.split ('.')[0]
    # we want to save images in a paralleled folder
    up_layer_folder = filelocation[0:-5]    #delete the last 'image'
    # print(up_layer_folder)
    #-----------------------------------------------#
    # we must create a 'faces' folder in advance    #
    #-----------------------------------------------#
    store_location = os.path.join (up_layer_folder, 'faces/')
    # print(store_location)

    for result in result_list:
        # print(result)
        # method 1: get four elements,their types are int
        x_left_top = result[0]
        y_left_top = result[1]
        x_right_bottom = result[2]
        y_right_bottom = result[3]
        crop_img = pro_img[x_left_top:x_right_bottom, y_right_bottom:y_left_top]
        # cv2.imshow ("cropped_{}".format(i),crop_img)
        # cv2.waitKey(0)
        # #decide how long the window will display,equal to 0 will show infinite time

        # method 2:
        # top, right, bottom, left = result
        # crop_img = pro_img[top:bottom,left:right]
        # pil_image.show ()

        # turn the np.array into an image
        final_name = store_location + file_name + '_face{}.jpg'.format(i)
        # print(final_name)
        cv2.imwrite(final_name, crop_img)
        i = i + 1

#Find faces in the picture,cut them
def face_rcg(img_file_position):      #input is the image's location
    #each image has a face_recognition list
    image = face_recognition.load_image_file(img_file_position)
    face_locations = face_recognition.face_locations(image)     #return a list of location
    # print(img_file_position)
    #use this list to cut them,return nothing,just operations
    cut_faces(face_locations,img_file_position)
    print('finish one image')
    return face_locations

#load & recognize images
# decouple them,this data only get access to that folder
def get_imgs_list(store_path):
    file_location_list = [join(store_path, f)
                  for f in listdir(store_path)
                  if isfile(join(store_path, f))]
    #In mac,we would read a hidden file in the folder.We have to remove it
    if store_path +'.DS_Store' in file_location_list:
        file_location_list.remove(store_path + '.DS_Store')
    return file_location_list

#---------------------------main-------------------------------#
#download images,if have already downloaded,please comment this part
# download_image(df)

#get all the image's postion,return a list of their locations
img_postion_list=get_imgs_list(image_folder_location)
#know how many images in this list,so we can read corresponding rows in the csv
num_of_files=len(img_postion_list)

#recognize it,generate two columns
img_rcg_name_list=[face_rcg(img_position)
                   for img_position in img_postion_list]
img_rcg_num_list=[len(rcglist)
                  for rcglist in img_rcg_name_list]  #number of recognized people

#read part of the origin csv files,generate a copy of it
df=pd.read_csv(csv_location,
               #skiprows=100,         #skip from the beginning
               nrows=num_of_files,    #only read corresponding rows
               index_col=0)           #read its index
write_header = True  # Needed to get header

#----------------add columns to the origin csv-------------------------#
#check in case their length are different
# d = [img_rcg_name_list, img_rcg_num_list]
# export_data = zip_longest(*d, fillvalue = '')

# #choice 1:generate just two columns
# with open('final_result.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
#       wr = csv.writer(myfile)
#       wr.writerow(('rcgnize_location', 'rcg_num'))   #set headers
#       wr.writerows(export_data)
# myfile.close()

# #choice 2:add columns,save as a new one
# df['rcgnize_location'] = pd.Series(img_rcg_name_list,index=df.index)
# df['rcg_num'] = pd.Series(img_rcg_num_list,index=df.index)
# df.to_csv('final_result.csv',mode='a', header=write_header)

#generate a new csv file,add three columns
# df2 = df.assign(rcg_position=img_postion_list,      #the faces' position
#                 rcgnize_location=img_rcg_name_list, #image file location
#                 rcg_num=img_rcg_num_list)           #how many faces were rcg
# df2.to_csv('final_add3col.csv')

