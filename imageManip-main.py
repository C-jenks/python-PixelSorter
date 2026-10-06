from PIL import Image
from operator import itemgetter

# TODO use input("Enter your value: ") to set values

input_image = Image.open("exampleLandscape.jpeg")
# input_image.save("input", format="jpeg")

# Extract pixel map
pixel_map = input_image.load()

width, height = input_image.size

# parameters

direction = True #true is horizontal, false is vertical
bothDirections = False #will apply the other direction following the application of the selected direction
directionPass = 0 #which pass curently on

sortOrder = True #true is ascending, false is decending for all segment sorting

sortBy = True #true is saturation, false is luminance

def getCurrentDirection():
    #return true if sorting horizontal, false for vertical
    if (direction & directionPass == 1) | (not direction & directionPass == 2 & bothDirections) :
        return True
    elif (not direction & directionPass == 1) | (direction & directionPass == 2 & bothDirections) :
        return False
    else :
        #if fail safe
        print("getCurrentDirection fail safe")
        return True

def getRange(iorj):
    # if iorj is true get layers direction else get pixels direction
    if getCurrentDirection() :
        if iorj :
            return height
        else :
            return width
    else :
        if iorj :
            return width
        else :
            return height
    
def sortLoop():
    # increase pass number
    directionPass += 1

    segment = []
    segmentFound = False
    segmentCount = 0

    #TODO if direction is true i will be y and j will be x
    #     if direction is false i will be x and j will be y
    #     change getDirection to return current sort direction

    # loop pixel layers
    for i in range(getRange(True)):
        # loop layers pixels
        for j in range(getRange(False)):
            # enter segment of pixels based on chosen parameters (above set lightness / below set darkness / TODO edge detection)
            if(pixel_map[i, j]):
                pixel = pixel_map.getpixel(i,j)
                # sort pixels in segment asending or decending based on chosen parameters (luminance \ saturation \ hue \ custom)
                if sortBy:
                # saturation is highest r,g,b minus lowest r,g,b

                    #sort bright add dark option
                    if (max(pixel)-min(pixel))>200:
                        #ADD i,j and .getPixel data into array
                        segment[segmentCount] = {'x':i,'y':j,'data':pixel,'satVal':max(pixel)-min(pixel)}
                        segmentFound = True
                        segmentCount += 1
                    elif segmentFound & segmentCount>1:
                        for k in range(segmentCount):
                            sortedSeg = sorted(segment, key=itemgetter('satVal'), reverse=False)
                        #with sortedSeg reright pixels using data from newSegment but location from segment

                        #reset found and count
                        segmentFound = False
                        segmentCount = 0
                    else:
                        #segment is only 1 pixel long

                        #reset found and count
                        segmentFound = False
                        segmentCount = 0
                        
                else:
                # luminance is Y = 0.2126 × R + 0.7152 × G + 0.0722 × B

                    #sort high sat add low option
                    if ((pixel[0]*0.2126)+(pixel[1]*0.7152)+(pixel[2]*0.0722))>200:
                        pass

                    
                # getPixel return (255, 160, 122) as a tuple
                print (pixel_map.getpixel(i,j))
                #pixel_map[i, j] = (255, 165, 0)

#first sort
sortLoop()

#second sort if selected
if bothDirections:
    sortLoop()

#reset pass counter after sorts finished
directionPass = 0 


# save the final output
input_image.save("output", format="jpeg")

# view final output on screen.
input_image.show() 


#TODO add masking using black white image to retain certain features

#TODO add edge based segment selection to add more image interaction 