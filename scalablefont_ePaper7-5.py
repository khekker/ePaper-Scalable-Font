# *****************************************************************************
# * | File        :	  scalablefont_ePaper7-5.py
# * | Author      :   Keith Hekker
# * | Function    :   MicroPython demo of scalable font on ePaper 7.5 (black/white only)
# * | Info        :   Tested on Raspberry Pi Pico with MicroPython Version v1.21.0
# *----------------
# * | This version:   V1.0
# * | Date        :   2025-02-04
# # | Info        :   MicroPython demo of scalable font on ePaper 7.5 (black/white only)
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


from pico_epaper_with_scalable_font import EPD_7in5
import array

epd = EPD_7in5()

def CreatePolygon(nX,nY,aBasePoly,nMultiplier,nDivisor,cPrintColor):
    aPolyCoords = array.array('h',[int(z * nMultiplier/nDivisor) for z in aBasePoly])
    epd.image1Gray.poly(nX,nY,aPolyCoords,cPrintColor,1)


def PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor):
    if cPrintColor == white:
        cInversePrintColor = black
    else:
        cInversePrintColor = white
    if nFontMultiplier == 1:
        epd.image1Gray.text(cText,xStartPosition,yStartPosition,cPrintColor)
        return
    nStringPositionCounter = 0
    nCounter = 1
    lLower = True
    xco = xStartPosition - 1
    nXStartingCoord = xco
    for nLText in range(1,8*len(cText)):
        xco = xco + 1
        ycounter = 0
        if nCounter == 1:
            cCurChars = "¶" + cText[nStringPositionCounter]
            #print("cCurChars " + cCurChars)
            if cText[nStringPositionCounter].islower() or cText[nStringPositionCounter] == " " :
                nCurCharPosition = cTotalFontStringLower.find(cCurChars) + 1
                lLower = True
            else:
                nCurCharPosition = cTotalFontStringUpper.find(cCurChars) + 1
                lLower = False
            #print(nCurCharPosition)
        if nCounter > 1:
            nXStartingCoord = nXStartingCoord + nFontMultiplier
        for yco in range(yStartPosition,yStartPosition + 8):
            ycounter = ycounter + 1
            nCurCharPosition = nCurCharPosition + 1
            if lLower:
                px_color = cTotalFontStringLower[nCurCharPosition]
            else:
                px_color = cTotalFontStringUpper[nCurCharPosition]
            nYStartingCoord = yStartPosition + (ycounter * nFontMultiplier)
            if px_color == "1":  #default background color
                continue
            if px_color != "0":
                #ellipse or polygon required
                if px_color == "5":
                    epd.image1Gray.ellipse(nXStartingCoord + nFontMultiplier -1,nYStartingCoord, nFontMultiplier -1,nFontMultiplier -1,cPrintColor,True,4)
                if px_color == "3":
                    epd.image1Gray.ellipse(nXStartingCoord + nFontMultiplier -1,nYStartingCoord + nFontMultiplier -1, nFontMultiplier -1,nFontMultiplier -1,cPrintColor,True,2)    
                if px_color == "9":
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord, nFontMultiplier -1,nFontMultiplier -1,cPrintColor,True,8)
                if px_color == "2":
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord + nFontMultiplier -1, nFontMultiplier -1,nFontMultiplier -1,cPrintColor,True,1)
                if px_color == "e":
                    #Special case for tilde - part 1
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord + nFontMultiplier -1, nFontMultiplier * 2,nFontMultiplier * 2,cPrintColor,True,3)
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord + nFontMultiplier -1, nFontMultiplier,nFontMultiplier,cInversePrintColor,True,3)
                if px_color == "l":
                    #Special case for tilde - part 2
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord + nFontMultiplier -1, nFontMultiplier * 2,nFontMultiplier * 2,cPrintColor,True,12)
                    epd.image1Gray.ellipse(nXStartingCoord,nYStartingCoord + nFontMultiplier -1, nFontMultiplier,nFontMultiplier,cInversePrintColor,True,12)
                if px_color == "k":
                    aBasePolyCoords = array.array('h',[1,0, 3,0, 3,3, 5,2, 6,2, 6,3, 4,4, 6,6, 7,6, 7,7, 5,7 ,3,5 ,3,7 ,1,7])
                    nDivisor = 1
                if px_color == "v":
                    aBasePolyCoords = array.array('h',[0,2, 2,2, 4,5, 6,2, 8,2, 5,7, 3,7])
                    nDivisor = 1
                if px_color == "w":
                    aBasePolyCoords = array.array('h',[0,2, 2,2, 3,5, 4,4, 5,5, 6,2, 8,2, 6,7, 5,7, 4,6, 3,7, 2,7])
                    nDivisor = 1
                if px_color == "x":
                    aBasePolyCoords = array.array('h',[0,8, 8,8, 12,16, 16,8, 24,8, 16,18, 24,28, 16,28, 12,20, 8,28, 0,28, 8,18])
                    nDivisor = 4
                if px_color == "z":
                    aBasePolyCoords = array.array('h',[0,2, 6,2, 3,6, 6,6, 6,7, 0,7, 3,3, 0,3])
                    nDivisor = 1
                if px_color == "R":
                    #polygon coordinates go clockwise
                    #bottom right
                    aBasePolyCoords = array.array('h',[1,-2,21,15,13,15,-4,2])
                    nDivisor = 4
                if px_color == "K":
                    aBasePolyCoords = array.array('h', [-1,-2,13,-12,21,-12,3,0,3,4,21,15,13,15,-3,5])
                    nDivisor = 4
                if px_color == "A":
                    aBasePolyCoords = array.array('h', [0,0,2,-3,4,-3,6,0,4,0,3,-2,2,0,2,2,0,2])
                    nDivisor = 1
                if px_color == "M":
                    aBasePolyCoords = array.array('h', [0,0,3,4,6,0,6,4,3,8,0,4])
                    nDivisor = 2
                if px_color == "N":
                    aBasePolyCoords = array.array('h', [0,0,2,4,2,7,0,3])
                    nDivisor = 1
                if px_color == "W":
                    aBasePolyCoords = array.array('h', [0,-4,3,-7,6,-4,6,0,3,-4,0,0])
                    nDivisor = 2
                if px_color == "V":
                    aBasePolyCoords = array.array('h', [0,0,3,0,6,7,9,0,12,0,12,2,6,12,0,2])
                    nDivisor = 2
                if px_color == "X":
                    aBasePolyCoords = array.array('h', [0,0,4,0,14,14,10,14])
                    CreatePolygon(nXStartingCoord,nYStartingCoord,aBasePolyCoords,nFontMultiplier,2,cPrintColor)
                    aBasePolyCoords = array.array('h', [10,0,14,0,4,14,0,14])
                    CreatePolygon(nXStartingCoord,nYStartingCoord,aBasePolyCoords,nFontMultiplier,2,cPrintColor)
                if px_color == "Y":
                    aBasePolyCoords = array.array('h', [0,0,4,0,5,3,7,3,8,0,12,0,12,1,7,5,7,10,5,10,5,5,0,1])
                    nDivisor = 2
                if px_color == "Z":
                    aBasePolyCoords = array.array('h', [0,0,2,0,-2,5,-4,5])
                    nDivisor = 1
                if "kvwxzRKAMNWVYZ".rfind(px_color) > -1:
                    CreatePolygon(nXStartingCoord,nYStartingCoord,aBasePolyCoords,nFontMultiplier,nDivisor,cPrintColor)
            else:
                epd.image1Gray.fill_rect(nXStartingCoord,nYStartingCoord,nFontMultiplier,nFontMultiplier,cPrintColor)
        nCounter = nCounter + 1
        if nCounter == 9:
            if cText[nStringPositionCounter] == " ":
                xco = xco - 3
            if cText[nStringPositionCounter] == "i":
                xco = xco - 2
            nStringPositionCounter = min(nStringPositionCounter + 1,len(cText)-1)
            nCounter = 1
            if cText[nStringPositionCounter] == "i":
                xco = xco - 1
    

if __name__=='__main__':
    
    epd.Clear()

    black=0x00
    white=0xFF
    
    epd.image1Gray.fill(white)
    
    print("Starting font sizing...")
    cFontFile = open("font_lower_case.txt", "r")
    cTotalFontStringLower = cFontFile.read(-1)
    cFontFile.close()
    cFontFile = open("font_upper_case.txt", "r")
    cTotalFontStringUpper = cFontFile.read(-1)
    cFontFile.close()
    
    cPrintColor = black
    cText = "The quick brown fox jumps over the lazy dog"
    nFontMultiplier = 1
    xStartPosition = 10
    yStartPosition = 1
    PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor)
    
    nFontMultiplier = 4
    xStartPosition = 10
    yStartPosition = 10
    PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor)
    
    nFontMultiplier = 8
    xStartPosition = 10
    yStartPosition = 40
    PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor)
    
    nFontMultiplier = 16
    xStartPosition = 10
    yStartPosition = 106
    PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor)
    
    nFontMultiplier = 32
    xStartPosition = 10
    yStartPosition = 220
    PrintString(cText,xStartPosition,yStartPosition,nFontMultiplier,cPrintColor)
    
    print("Font sizing ended")
    epd.display(epd.buffer_1Gray)