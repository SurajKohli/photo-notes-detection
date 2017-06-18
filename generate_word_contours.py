import cv2
import os
import sys

"""Error Handling For Empty/Corrupt Image"""

    # i = input("\nEnter Image Name For Word Contours:\n")
    # i="test1.jpg"
    # i="1.png"
i = sys.argv[1]
image = cv2.imread(i)
if( image is None ):
    #cannot proceed forward with empty image
    print('''**************************************************************
**************************************************************
********************* Empty/Corrupt Image ********************
********************* Give Correct Image *********************
**************************************************************
**************************************************************''')
    sys.exit()
else:
    print('''**************************************************************
**************************************************************
********************* Image Validated ************************
**************************************************************
**************************************************************''')

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
dilated = cv2.dilate(thresh,kernel,iterations = 15) # dilate
imgContours, contours, hierarchy  = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

idx = 0

""" Create directory if it doesnt exist else overwrite """

# x = input("Save to which directory ?\n")
x = sys.argv[2]
#Exit Code for Failure
if x is '':
    sys.exit(0)
if not os.path.exists(x):
    os.makedirs(x)
os.chdir(os.getcwd() + "/" + str(x)) 

# for each contour found, draw a rectangle around it on original image
for contour in contours:
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)

    # discard areas that are too large
    if h>300 and w>300:        
        continue

    # discard areas that are too small
    if h<60 or w<60:
        continue
    # draw rectangle around contour on original image
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
    idx += 1
    roi = image[y:y+h,x:x+w]
    cv2.imwrite(str(idx) + ".jpg", roi)    

cwd = os.getcwd()
print(cwd)
print(idx)

# write original image with added contours to disk  
cv2.imwrite("Result/contoured.jpg", image) 
# print(image.shape)

""" Resize image for displaying"""
r = 400.0/image.shape[1]
dim = (400, int(image.shape[0] * r))
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# print(resized.shape)
cv2.imshow("CONTOURED IMAGE",resized)
cv2.waitKey(0)


# os.chdir('..')
# """Write prints to logfile.log"""
# l = [str(cwd),str(idx)]
# with open('logfile.log','w') as f:
#     f.write('\n'.join(l))
# f.close()    
# """End"""

#Exit code for Integrated Script
# sys.exit(100)