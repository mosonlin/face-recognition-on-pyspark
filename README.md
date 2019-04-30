# face-recognition-on-pyspark
Deploy face recognition worker nodes on GCP cluster

## Attention:
If you want to test the code in pyspark, please reconfigure the path in sub.sh and sparktest.py.
Meanwhile, reconfigure the path in down_rcg_cut.py to get the corresponding csv file and store path.

# Implement in local machine(in local folder):

## Situation 1:Before update
Because the website have been updated on March 30th, so the former method to crawl the captions and images would be useless.

They are crawl_tocsv_old.py and down_rcg.py

## Situation 2:After update
### Step 1
Right now, to crawl data on the website, please use crawl_new.py.It will generate a csv called image_caption_data.csv on google cloud storage.

### Step 2
Since we already get all the images in folder ‘/data/images/‘ and upload them to google cloud with in terminal.Then we just execute down_rcg_cut.py which will implement face recognition and crop the faces and store them in a folder in /data/faces/.I have commented download images part, which just recognize faces in local machine. 

At last, it read the data from new_image_caption_data.csv (which was get in step 1) and generate a new csv file called final_add3col.csv.

Meanwhile, the get_accuracy.py will output the accuracy comparing the caption processing result and image face recognition result.

You can use draw_plot.py to get the final diagram.

# Implement on Spark:

Suppose we already have uploaded all the images to bucket, in 
"gs://ece795zylin/final_pro/image/"

### Step 1:
Use the command in ininode.sh to configure all the master node and worker nodes.
Can’t run this sh script directly!Because the virtual machine can’t enter virtual environment to install all the packages.

### Step 2:
In local terminal, run sub.sh script to upload the sparktest.py automatically.

### Step 3:
To change the number of partitions, we must manually change the number in sparktest.py.
