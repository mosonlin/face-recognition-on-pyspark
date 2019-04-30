import pandas as pd

#----------------------calculate the accuracy------------------------#
final=pd.read_csv('final_add3col.csv',usecols=['number of names','rcg_num'])
total_row_num=final.shape[0]    #get the image number
wrong=0
for row in final.iterrows():
    if row[1][0]!=row[1][1]:    #if number of names != rcg_num
        wrong+=1

accuracy=(total_row_num-wrong)/total_row_num
print('total:',total_row_num)
print('accuracy is:',accuracy)