import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

time_consume_2workers=45*60+29
time_consume_3workers=30*60+29
time_consume_4workers=22*60+13
time_list=[time_consume_2workers,
           time_consume_3workers,
           time_consume_4workers]
name_list = ['2-worker','3-worker','4-worker']  #each bar's name

bars=plt.bar(x=name_list,        #set the labels
             height=time_list,   #data
             color='rgb',        #color is red,green,blue
             label='workernode')
for bar in bars:
    yval = bar.get_height()                  #get each bar's height
    plt.text(bar.get_x()+bar.get_width()/2-0.13,  #move text's x coordinate
             yval + 0.1,                     #move text's y coordinate
             s=yval)

plt.title('Diverse Working Nodes - Time Spend') #title
plt.xlabel('Working Nodes Number')      #x-label
plt.ylabel('Time spend/s',rotation=90)  #y-label

# plt.legend(labels=['Different Nodes'],
#            handles=name_list,
#            loc='best',
#            bbox_to_anchor=(1.05,1.00))  #show the identification
plt.grid()      #set grids
plt.savefig('nodes.png')    #save the illustration
plt.show()      #show the illustration
