#--------------------------------------------------------------#
#upload images to gs
# gsutil cp -r /Users/linzhengyang/Destop/document/bigdata/project2/code/data/image \
			  # gs://ece795zylin/final_pro/

#move one folder into another folder
# gsutil mv gs://ece795zylin/final_pro/final_result_test15img gs://ece795zylin/final_pro/test_spark

#then delete it
#gsutil rm -r gs://ece795zylin/final_pro/final_result_3nodes
#---------------------------------------------------------------#

#-------------------------run the script-------------------------#
#to run this sub.sh file,use
#sh /Users/linzhengyang/Desktop/document/bigdata/project2/code/sub.sh

#remove the job code in the bucket
gsutil rm gs://ece795zylin/final_pro/sparktest.py

#upload the new job code
gsutil cp /Users/linzhengyang/Desktop/document/bigdata/project2/code/sparktest.py \
gs://ece795zylin/final_pro/

#echo check the code
#catch the cloud in cloud storage
#gsutil cat gs://ece795zylin/final_pro/sparktest.py

#submit the job
gcloud dataproc jobs submit pyspark \
    --cluster cluster-final --region global \
    gs://ece795zylin/final_pro/sparktest.py \
    --properties 'spark.pyspark.python=/home/g1996linmoson/.conda/envs/final/bin/python'
     # --py-files gs://ece795zylin/final_pro/dependencies.zip

