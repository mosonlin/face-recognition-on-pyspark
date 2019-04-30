import pyspark
from pyspark.context import SparkContext
sc = SparkContext.getOrCreate()
from PIL import Image
from io import BytesIO
import face_recognition
import numpy as np
import cv2
print('finish face_recognition,numpy,cv2')

#read as binary
def rcg_face(data):
    image = BytesIO (data)      #_io.BytesIO
    # image_temp=Image.open(BytesIO(data))  #JpegImageFile
    # image_final=np.asarray(image_final1)  #numpy.ndarray
    #we use numpy.array to create a numpy.ndarray
    image_result = face_recognition.load_image_file (image)
    face_locations = face_recognition.face_locations (image_result)
    num_faces =len(face_locations)
    # print(face_locations,num_faces)   #It only display on worker node
    #print will show nothinig,cause this runs on worker nodes.

    # crop the faces
    # i=0
    # for result in face_locations:
    #     top, right, bottom, left = result
    #     pro_img = cv2.imread (image_temp, cv2.IMREAD_COLOR)
    #     crop_img = pro_img[top:bottom, left:right]
    #     im = Image.fromarray (crop_img)
    #     # final_name = store_location + file_name + '_face{}.jpg'.format (i)
    #     # im.save(final_name)
    #     i+=1
    return (face_locations,num_faces)

#map function,in method 1.
def process_img(path):
    image_test = face_recognition.load_image_file (path[0][::])
    face_locations = face_recognition.face_locations (image_test)
    num_faces = len (face_locations)
    return (face_locations,num_faces)

# #use wholetextFiles(*.jpg) doesn't work
#also because they have redundancy at the beginning
# test_image1=sc.wholeTextFiles('gs://ece795zylin/final_pro/test/*.jpg',12)
# image_list=test_image1.map(lambda image:(image[0],
#                                         rcg_face(image[-1])))
# print('-------------')
# print(image_list.collect())

# #-------------------------compare-------------------------#
# #wholetextfiles will add some more bytes,which can't reconstruct the image
# test_folder=sc.wholeTextFiles("gs://ece795zylin/final_pro/test/"
#                               ,use_unicode=False)   #encoding with 'utf-8'
# #read the whole folder,which will return a pairRDD
# image_list=test_folder.collect()[:1] #each element is also a list
# # print(type(image_list[0]))  #element is a tuple
# # print(image_list[0][0])   #filename
# print(image_list[0][1]) #data
# print('-------------')

# #binary
# test_image=sc.binaryFiles('gs://ece795zylin/final_pro/test/image_page1_caption7.jpg')
# image=test_image.collect()[0][1]
# print(image)
# #-------------------------compare-------------------------#

#-----------------------main---------------------------#
#read as an rdd and do the partition

#method 1:transform the origin rdd
# image_rdd=sc.wholeTextFiles('gs://ece795zylin/final_pro/image/*.jpg')
# image_rdd.map(process_img)  #directly change the origin rdd
# print(type(image_rdd))
# print('-------------')
# print(image_rdd.collect())


#method 2:use binaryFiles
test_image=sc.binaryFiles('gs://ece795zylin/final_pro/image/*.jpg',12)
#get the image in pairRDD,tuple image(filename,data)
image_pair=test_image.map(lambda image:(image[0],
                                        rcg_face(image[-1])))
#we want to get a (image_name,(locations,list))

#check if we can get a clean data(without redundancy at the beginning)
# print ('-------------')
# print(type(image_pair))     #'pyspark.rdd.PipelinedRDD'

# test=image_pair.collect()
# for data in test:
#     # print(type(data))   #bytes
#     # print ('-------------')
#     # print (data)
#     # print ('-------------')
#     if BytesIO(data):
#         rcg_face(data)
#     else:
#         print('dirty data')

# test=test_image.collect()
# print(type(test))   #list
# for tuple in test:
#     filename=tuple[0]
#     data=tuple[1]
#     # print(filename)
#     # print('-------------')
#     # print(data)
#     print('-------------')
#     if BytesIO (data):
#         rcg_face(data)
#     else:
#         print('dirty data')

#-----------------------------save----------------------------#
#can't insert the header,can't interpret tuple as integer
# tuple_list.insert(('img_name','face_location','num_of_people'),0)
store_path='gs://ece795zylin/final_pro/final_result/2nodes'
#convert to partition
image_pair.saveAsTextFile(store_path)
