import cv2
import numpy as np
import pandas as pd
import sys


# taking path + file name as 1st argument
img_path = sys.argv[1]
#Reading the image with opencv
img = cv2.imread(img_path)
print(img.shape)
print('Original Dimensions : ',img.shape)

# setting the window dimensions
screen_res = 1280, 650
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance
#from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
		
		



# creating and setting window dimensions		
cv2.namedWindow('image', cv2.WINDOW_NORMAL | cv2.WINDOW_FULLSCREEN )
cv2.resizeWindow('image', window_width, window_height)
cv2.setMouseCallback('image',draw_function)

img = cv2.resize(img, (window_width, window_height))

while(1):
	
	cv2.imshow("image",img)
	if (clicked):
		
		#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
		cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

		#Creating text string to display( Color name and RGB values )
		text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
		
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(img, text,(50,50),2,0.4,(255,255,255),1,cv2.LINE_AA)

		#For very light colours we will display text in black colour
		if(r+g+b>=600):
			cv2.putText(img, text,(50,50),2,0.4,(0,0,0),1,cv2.LINE_AA)
			
		clicked=False

	#Break the loop when user hits 'esc' key    
	if cv2.waitKey(20) & 0xFF ==27:
		break

cv2.destroyAllWindows()
