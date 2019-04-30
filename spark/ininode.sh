#!/bash/bin
echo start installing face-recognition and its dependencies...

#because we use linux,it forces us to use conda,we can't use pip
conda create -n final python=3.6 -y

#activate virtualenv
source activate final

#find which python do we use
which python
#it will print '/home/g1996linmoson/.conda/envs/final/bin/python'

#install prerequesite
conda install pandas cmake boost -y
pip install opencv-python
sudo apt-get update
#--------------------------------------#
pip install dlib

pip install face_recognition
pip show face-recognition
#--------------------------------------#

#specifc virtual env
#nano spark-env.sh
#PYSPARK_PYTHON='/home/g1996linmoson/.conda/envs/final/bin/python'