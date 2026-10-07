from PIL import Image
from operator import itemgetter

def orderOfOperations():
    inputImage = Image.open("exampleLandscape.jpeg").convert('RGB')
    # input_image.save("input", format="jpeg")

    # Extract pixel map
    pixel_map = inputImage.load()

    width, height = inputImage.size

    # parameters
    direction = True #true is horizontal, false is vertical
    bothDirections = False #will apply the other direction following the application of the selected direction
    directionPass = 0 #which pass curently on

    sortOrder = True #true is ascending, false is decending for all segment sorting

    sortBy = 1 #0 is saturation, 1 is luminance, 2 is hue

    getParameters(direction, bothDirections, sortOrder, sortBy)

    #first sort
    sortLoop(inputImage, pixel_map, width, height, direction, bothDirections, directionPass, sortOrder, sortBy)

    #second sort if selected
    if bothDirections:
        sortLoop()

    #reset pass counter after sorts finished
    directionPass = 0 

    # save the final output
    #inputImage.save("output", format="jpeg")

    # view final output on screen.
    inputImage.show() 

def getParameters(direction, bothDirections, sortOrder, sortBy):
    # TODO user input with val = input("Enter your value: ") to set values
    #direction = input("Enter your value: ")
    pass

def getCurrentDirection(direction, bothDirections, directionPass):
    #return true if sorting horizontal, false for vertical
    if (direction and directionPass == 1) or (not direction and directionPass == 2 and bothDirections) :
        return True
    elif (not direction and directionPass == 1) or (direction and directionPass == 2 and bothDirections) :
        return False
    else :
        #if fail safe
        print("getCurrentDirection fail safe")
        return True

def getRange(iorj, width, height, direction, bothDirections, directionPass):
    # if iorj is true get layers direction else get pixels direction
    if getCurrentDirection(direction, bothDirections, directionPass) :
        if iorj :
            return height
        else :
            return width
    else :
        if iorj :
            return width
        else :
            return height
    
def sortLoop(inputImage, pixel_map, width, height, direction, bothDirections, directionPass, sortOrder, sortBy):
    # increase pass number
    directionPass += 1

    segment = []
    segmentFound = False
    segmentCount = 0

    currentDirection = getCurrentDirection(direction, bothDirections, directionPass)

    x = 0
    y = 0

    # loop pixel layers
    for i in range(getRange(True, width, height,direction, bothDirections, directionPass)):
        # loop layers pixels
        for j in range(getRange(False, width, height, direction, bothDirections, directionPass)):
            #TODO if direction is true i will be y and j will be x
            #     if direction is false i will be x and j will be y
            #     change getDirection to return current sort direction
            if currentDirection:
                x = j
                y = i
            else :
                x = i
                y = j

            pixel = pixel_map[x, y]
            # enter segment of pixels based on chosen parameters (above set lightness / below set darkness / TODO edge detection / hue)
            match sortBy:
                case 0:
                    # sort high sat add low option

                    # saturation is highest r,g,b minus lowest r,g,b
                    if (max(pixel)-min(pixel))>50:
                        #ADD i,j and .getPixel data into list
                        segment.append({'x':x, 'y':y, 'data':pixel, 'satVal':max(pixel)-min(pixel)})
                        segmentCount += 1
                        segmentFound = True
                    elif segmentFound and segmentCount>1:
                        for k in range(segmentCount):
                            sortedSeg = sorted(segment, key=itemgetter('satVal'), reverse=False)
                        #with sortedSeg reright pixels using data from newSegment but location from segment
                        for k in range(segmentCount):
                            #pixel_map[segment[k]['x'],segment[k]['y']] = (0,0,0)#sortedSeg[k]['data']
                            inputImage.putpixel([segment[k]['x'],segment[k]['y']], sortedSeg[k]['data'])

                        #reset segment, found and count
                        segment.clear()
                        segmentFound = False
                        segmentCount = 0
                    else:
                        #segment is only 1 pixel long

                        #reset segment, found and count
                        segment.clear()
                        segmentFound = False
                        segmentCount = 0
                        
                case 1:
                    # sort bright add dark option

                    # luminance is Y = 0.2126 × R + 0.7152 × G + 0.0722 × B
                    if ((pixel[0]*0.2126)+(pixel[1]*0.7152)+(pixel[2]*0.0722))>100:
                        #ADD i,j and .getPixel data into list
                        segment.append({'x':x, 'y':y, 'data':pixel, 'lumiVal':(pixel[0]*0.2126)+(pixel[1]*0.7152)+(pixel[2]*0.0722)})
                        segmentCount += 1
                        segmentFound = True
                    elif segmentFound and segmentCount>1:
                        for k in range(segmentCount):
                            sortedSeg = sorted(segment, key=itemgetter('lumiVal'), reverse=False)
                        #with sortedSeg reright pixels using data from newSegment but location from segment
                        for k in range(segmentCount):
                            #pixel_map[segment[k]['x'],segment[k]['y']] = (0,0,0)#sortedSeg[k]['data']
                            inputImage.putpixel([segment[k]['x'],segment[k]['y']], sortedSeg[k]['data'])

                        #reset segment, found and count
                        segment.clear()
                        segmentFound = False
                        segmentCount = 0
                    else:
                        #segment is only 1 pixel long

                        #reset segment, found and count
                        segment.clear()
                        segmentFound = False
                        segmentCount = 0
                case 2:
                    # sort hue
                    print()

#Run
orderOfOperations()

#TODO add masking using black white image to retain certain features

#TODO add edge based segment selection to add more image interaction 