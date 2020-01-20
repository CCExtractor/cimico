import glob, os
from PIL import Image, ImageDraw, ImageFont
import json
import copy
import textwrap
import cv2 as cv
import yaml
from moviepy.editor import *

dta = {}

def convertogif(pth):
    clip = (VideoFileClip(pth))
    gifpth = ""
    for i in range(len(pth)-3):
        gifpth += pth[i]
    gifpth += "gif"
    clip.write_gif(gifpth)

def generatevid(pth):
    imgs = []
    with open(pth, 'r') as f:
        dta = json.load(f)
    pth2style = input("Enter the path to the yaml file: ")
    try:
        with open(pth2style) as f:
            style = yaml.load(f, Loader=yaml.FullLoader)
    except:
        style = {'introtext_time': 5, 'fps': 1, 'watermark': False, 'fontsz': 20, 'introtext': 'Code written by knightron0', 'font_path': 'fonts/hack.ttf', 'width': 1920, 'height': 1080, 'mute': ["a", "b"],'textwrap': 100, 'ptr': [["i", "arr"]]}
    height = style["height"]
    width = style["width"]
    ifmute = {}
    pnter = {}
    for j in style["mute"]:
        ifmute[j] = True
    for j in style["ptr"]:
        pnter[j[0]] = j[1]

    src = dta["source"].splitlines()
    fntsz = style["fontsz"]
    curr = -1
    strtln = dta["lines"]["1"]["report"][0]
    allvars = {}
    variablevalues = {}
    length = len(dta["lines"])
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    fnt = ImageFont.truetype(style["font_path"], fntsz)
    d = ImageDraw.Draw(img)
    w, h = d.textsize(style["introtext"], font=fnt)
    d.text(((width-w)/2, (height-h)/2), style["introtext"], fill=(255,255,255), font = fnt)
    num = 1

    for i in range(style["fps"]*style["introtext_time"]):
        imgnm = 'img' + str(num) + ".png"
        img.save(imgnm)
        img2 = cv.imread(imgnm)
        imgs.append(img2)
        num+=1
    tms = int(height//fntsz)
    till = 0
    outputtillnow = []
    oouttill = 0
    for j in range(1, len(dta["lines"])+1):
        img = Image.new('RGB', (width, height), color = (0, 0, 0))
        fnt = ImageFont.truetype(style["font_path"], fntsz)
        d = ImageDraw.Draw(img)
        if(dta["lines"][str(min(j+1, length))]["report"][10] != ""):
            outputtillnow.append(dta["lines"][str(j+1)]["report"][10])
        d.line((width/2,0, width/2,height), fill=(255,255,255), width=5)
        curr = dta["lines"][str(j)]["report"][0]-strtln+1
        for i in range(till, min(len(src), till + tms)):
            if(i == curr):
                d.rectangle(((0,((i-till)*fntsz)), (width/2,((i-till)*fntsz)+fntsz)), fill=(58, 61, 72))
                d.text((0,((i-till)*fntsz)),src[i], fill=(255,255,255), font = fnt)
            else:
                d.text((0,((i-till)*fntsz)),src[i], fill=(255,255,255), font = fnt)
        if curr >= (tms//2) and (len(src)-curr) >= (tms//2):
            till+=1
        fnt = ImageFont.truetype(style["font_path"], fntsz)
        if dta["lines"][str(min(j+1, length))]["report"][2] == 1:
            ln = "This line has been executed %s time and the time spent till now on this" % (1)
        else:
            ln = "This line has been executed %s times and the time spent till now on this" % (dta["lines"][str(min(j+1, length))]["report"][2])
        ln2 = "line is {:f} seconds".format(dta["lines"][str(min(j+1, length))]["report"][3])
        d.text((width/2+fntsz, fntsz),ln, fill=(255,255,255), font = fnt)
        d.text((width/2+fntsz, fntsz+fntsz),ln2, fill=(255,255,255), font = fnt)
        d.line((width/2, fntsz*4, width,fntsz*4), fill=(255,255,255), width=5)
        lftlnotpt = int((85*(height))/100)
        lfttms = int((height-lftlnotpt-fntsz)/fntsz)-1
        d.line((width/2, lftlnotpt, width,lftlnotpt), fill=(255,255,255), width=5)
        for i in range(max(len(outputtillnow) - lfttms, 0), len(outputtillnow)):
            d.text((width/2+fntsz, lftlnotpt + fntsz + ((i-max(len(outputtillnow) - lfttms, 1)) * fntsz)),outputtillnow[i], fill=(255,255,255), font = fnt)
        didmodify = {}
        for i in dta["lines"][str(min(j+1, length))]["report"][7]:
            allvars[i[0]] = [i[0], None, i[1]]
            variablevalues[i[0]] = i[1]
            didmodify[i[0]] = True

        for i in dta["lines"][str(min(j+1, length))]["report"][9]:
            allvars[i[0]] = [i[0], None, i[1]]
            didmodify[i[0]] = True

        for i in dta["lines"][str(min(j+1, length))]["report"][8]:
            allvars[i[0]] = [i[0], i[1], i[2]]
            didmodify[i[0]] = True

        for i in dta["lines"][str(min(j+1, length))]["report"][6]:
            temp = variablevalues[i[0]].copy()
            temp[i[1]] = i[3]
            allvars[i[0]] = [i[0], variablevalues[i[0]], temp]
            variablevalues[i[0]] = temp.copy()
            didmodify[i[0]] = True

        for i in dta["lines"][str(min(j+1, length))]["report"][5]:
            temp = variablevalues[i[0]].copy()
            temp[i[0]].append(i[1])
            allvars[i[0]] = [i[0], variablevalues[i[0]], temp]
            variablevalues[i[0]] = temp.copy()
            didmodify[i[0]] = True
        stp = 0
        yval = {}
        xval = {}
        for i in allvars:
            if i in didmodify and i not in ifmute:
                if(didmodify[i] == True):
                    if(allvars[i][1] != None):
                        if i not in pnter:
                            st = "The variable " + allvars[i][0] + " was changed, previous value " +  str(allvars[i][1]) + " and current value " + str(allvars[i][2])
                        else:
                            st = "The variable " + allvars[i][0]  + ", points to " +  pnter[i] + ", was changed, previous value " +  str(allvars[i][1]) + " and current value " + str(allvars[i][2])
                        lines = textwrap.wrap(st, width=70)
                        for k in lines:
                            d.text((width/2+fntsz, ((fntsz*4)+10) + (stp*fntsz)),k, fill=(0,200,0), font = fnt)
                            w, h = d.textsize(k, font=fnt)
                            stp+=1
                        yval[i] = ((fntsz*4)+10) + (stp*fntsz)- (fntsz/2)
                        xval[i] = width/2+fntsz + w + 20
                    else:
                        if i not in pnter:
                            st = "The variable " + allvars[i][0] + " was created, current value " + str(allvars[i][2])
                        else:
                            st = "The variable " + allvars[i][0] + ", points to " +  pnter[i] + ", was created, current value " + str(allvars[i][2])
                        lines = textwrap.wrap(st, width=70)
                        for k in lines:
                            d.text((width/2+fntsz, ((fntsz*4)+10) + (stp*fntsz)),k, fill=(69, 243, 226), font = fnt)
                            stp+=1
                            w, h = d.textsize(k, font=fnt)
                        yval[i] = ((fntsz*4)+10) + (stp*fntsz)- (fntsz/2)
                        xval[i] = width/2+fntsz + w + 20
            elif i not in didmodify and i not in ifmute:
                if i not in pnter:
                    st = "The variable " + allvars[i][0] + ", current value " + str(allvars[i][2])
                else:
                    st = "The variable " + allvars[i][0] + ", points to " +  pnter[i] + ", current value " + str(allvars[i][2])
                lines = textwrap.wrap(st, width=70)
                for k in lines:
                    d.text((width/2+fntsz, ((fntsz*4)+10) + (stp*fntsz)),k, fill=(255,255,255), font = fnt)
                    stp+=1
                    w, h = d.textsize(k, font=fnt)
                yval[i] = ((fntsz*4)+10) + (stp*fntsz) - (fntsz/2)
                xval[i] = width/2+fntsz + w + 20
        for i in pnter:
            if i in allvars and pnter[i] in allvars:
                d.line((width/2+ fntsz/2, yval[i],width/2+ fntsz,yval[i]), fill=(255,0,0), width=2)
                d.line((width/2+ fntsz/2, yval[i],width/2+ fntsz/2,yval[pnter[i]]), fill=(255,0,0), width=2)
                d.line((width/2+ fntsz/2,yval[pnter[i]],width/2+ fntsz,yval[pnter[i]]), fill=(255,0,0), width=2)
        if style["watermark"] == True:
            txt = "Generated by " + os.path.basename(__file__)
            w, h = d.textsize(txt, font=fnt)
            d.text((width-w, height-h), txt, fill=(255,255,255), font = fnt)
        imgnm = 'img' + str(num) + ".png"
        img.save(imgnm)
        img2 = cv.imread(imgnm)
        height, width, layers = img2.shape
        size = (width,height)
        imgs.append(img2)
        num += 1
    pth2vid = input("Where do you want your video to be stored? ")
    pth2vid += "/DebuggerVideo.avi"
    out = cv.VideoWriter(pth2vid,cv.VideoWriter_fourcc(*'DIVX'), style["fps"], size)
    imglast = imgs[len(imgs)-1]
    for i in range(5):
        imgs.append(imglast)
    for i in range(len(imgs)):
        out.write(imgs[i])
    out.release()
    for file in glob.glob("*.png"):
        os.remove(file)
    return pth2vid
    print("Path to video: " + pth2vid)
# generatevid("data.json")