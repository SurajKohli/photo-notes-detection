# TrainAndTest.py

import cv2
import numpy as np
import operator
import os
from PIL import Image
import pickle
import sys ###for integration purpose

#############
'''Added for Integration Purpose'''
'''Command Line arguments'''
command_line_input_image = str(sys.argv[1])
#############

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 800
# MIN_CONTOUR_AREA = 1000 

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################
class ContourWithData():

    # member variables ############################################################################
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False        # much better validity checking would be necessary
        return True

###################################################################################################

def editDistance( str1 , str2 ):

    l1 = len(str1)
    l2 = len(str2)
    dp = [[0 for x in range(l2+1)] for x in range(l1+1)]

    for i in range(l1+1):
        for j in range(l2+1):
            if( i == 0 ):
                dp[i][j] = j
            elif( j == 0 ):
                dp[i][j] = i
            elif( str1[i-1] == str2[j-1] ):
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min( dp[i-1][j]+1 , dp[i][j-1]+1 , dp[i-1][j-1]+2 )

    return dp[l1][l2]



def edit_distance(glossary_list,word):
    closest_word = ''
    small = 99999
    for i in glossary_list:
        dist = editDistance(word,i)
        if(small>dist):
            small = dist
            closest_word = i
    return closest_word

###################################################################################################
def main():
    allContoursWithData = []                # declare empty lists,
    validContoursWithData = []              # we will fill these shortly

    try:
        npaClassifications = np.loadtxt("./MachineLearningData/classifications.txt", np.float32)                  # read in training classifications
    except:
        print("error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return
    # end try

    try:
        npaFlattenedImages = np.loadtxt("./MachineLearningData/flattened_images.txt", np.float32)                 # read in training images
    except:
        print("error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return
    # end try
    with open('./MachineLearningData/final_glossary.txt','r') as handle:
        lines = handle.readlines()
        glossary_list = list()
        for i in lines:
            k = i.strip('\n')
            glossary_list.append(k)

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

    kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    # Image.open("a1.gif").save("a1.png")

    # imgTestingNumbers = cv2.imread("5.jpg")          # read in testing numbers image
    ###Integration Purpose
    imgTestingNumbers = cv2.imread(command_line_input_image)

    if imgTestingNumbers is None:                           # if image was not read successfully
        print("error: image not read from file \n\n")        # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit function (which exits program)
    # end if

    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)       # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean

    imgThreshCopy = imgThresh.copy()        # make a copy of the thresh image, this in necessary b/c findContours modifies the image

# imgThresh is white on black which is required for contour detection

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points


    for npaContour in npaContours:                             # for each contour
        contourWithData = ContourWithData()                                             # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
        allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data
        # show input image with green boxes drawn around found digits
    # end for

    print(len(allContoursWithData)) #length of all contours

    # contour_img = cv2.drawContours(imgTestingNumbers, npaContours, -1, (0,255,0), 3)
    # cv2.imshow("imgTestingNumbers", contour_img)

    for contourWithData in allContoursWithData:                 # for all contours
        if contourWithData.checkIfContourIsValid():             # check if valid
            validContoursWithData.append(contourWithData)       # if so, append to valid contour list
            print(contourWithData.fltArea)
        # end if
    # end for

    '''for contour in validContoursWithData:
        contour_img = cv2.drawContours(imgTestingNumbers, contour.npaContour, -1, (0,255,0), 3)
        cv2.waitKey(0)
        cv2.imshow("imgTestingNumbers", contour_img)
'''

    print(len(validContoursWithData)) # length of all valid contours

    validContoursWithData.sort(key = operator.attrgetter("intRectX"))         # sort contours from left to right

    strFinalString = ""         # declare final string, this will have the final number sequence by the end of the program

    idx = 0
    for contourWithData in validContoursWithData:            # for each contour
        idx += 1
        cv2.rectangle(imgTestingNumbers,                                        # draw rectangle on original testing image
                      (contourWithData.intRectX, contourWithData.intRectY),     # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      # lower right corner
                      (0, 255, 0),              # green
                      2)                        # thickness

        # x,y,w,h=cv2.boundingRect(contourWithData.npaContour) 

        # Added code for bounding Rect
        # roi=imgThresh[y:y+h,x:x+w]
        # cv2.imwrite(str(idx) + '.jpg', roi)
        #end code

        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,     # crop char out of threshold image
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]
        # imgROI = imgTestingNumbers[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,
                           # contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]                           

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consistent for recognition and storage
        # cv2.imwrite('TrainAndTest' + str(idx) + '.jpg', imgROI)
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

        npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)     # call KNN function find_nearest        
        strCurrentChar = str(chr(int(npaResults[0][0])))                                             # get character from results

        strFinalString = strFinalString + strCurrentChar            # append current char to full string
    # end for

    length_detect = len(strFinalString)
    m_glossary_list = list()
    for i in glossary_list:
        if(len(i)>=(length_detect-1) and len(i)<=(length_detect + 1)):
            m_glossary_list.append(i)
    closest_word = edit_distance(m_glossary_list,strFinalString)
    print("Detected word is => ")
    print("\n" + strFinalString + "\n")                  # show the full string
    print("Corrected word is => ")
    print("\n" + closest_word + "\n" )

    cv2.imshow("imgTestingNumbers", imgTestingNumbers)      # show input image with green boxes drawn around found digits
    cv2.waitKey(0)                                          # wait for user key press

    cv2.destroyAllWindows()             # remove windows from memory
    #### Integration Purpose
    # """Write prints to logfile.log"""
    with open('Result/word_list.txt','a') as f:
        if((closest_word == '') or ( closest_word == ' ')):
            pass
        else:
            f.write(closest_word)
            f.write('\n')
    f.close()    
    # """End"""
    return 
    ####Returning 100 for Integration Purpose
###################################################################################################
if __name__ == "__main__":
    main()
# end if









