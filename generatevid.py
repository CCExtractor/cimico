import glob, os
from PIL import Image, ImageDraw, ImageFont
import json
import copy
import textwrap
import cv2 as cv

dta = {}

def main(pth):
    imgs = []
    with open(pth, 'r') as f:
        dta = json.load(f)
    src = dta["source"].splitlines()
    curr = -1
    strtln = dta["lines"]["1"]["report"][0]
    allvars = {}
    variablevalues = {}
    for j in range(len(dta["lines"])):
        img = Image.new('RGB', (1920, 1080), color = (255, 255, 255))
        fnt = ImageFont.truetype('fonts/ubuntu.ttf', 45)
        d = ImageDraw.Draw(img)
        curr = dta["lines"][str(j+1)]["report"][0]-strtln
        for i in range(len(src)):
            if(i == curr):
                d.text((50,50+(i*50)),src[i], fill=(255,0,0), font = fnt)
            else:
                d.text((50,50+(i*50)),src[i], fill=(0,0,0), font = fnt)
        fnt = ImageFont.truetype('fonts/ubuntu.ttf', 30)
        if dta["lines"][str(j+1)]["report"][2] == 1:
            ln = "This line has been executed %s time and the time spent till" % (dta["lines"][str(j+1)]["report"][2])
        else:
            ln = "This line has been executed %s times and the time spent till" % (dta["lines"][str(j+1)]["report"][2])
        ln2 = "now on this line is {:f} seconds".format(dta["lines"][str(j+1)]["report"][3])
        d.text((960, 50),ln, fill=(0,0,0), font = fnt)
        d.text((960, 80),ln2, fill=(0,0,0), font = fnt)
        didmodify = {}
        for i in dta["lines"][str(j+1)]["report"][7]:
            allvars[i[0]] = [i[0], None, i[1]]
            variablevalues[i[0]] = i[1]
            didmodify[i[0]] = True

        for i in dta["lines"][str(j+1)]["report"][9]:
            allvars[i[0]] = [i[0], None, i[1]]
            didmodify[i[0]] = True

        for i in dta["lines"][str(j+1)]["report"][8]:
            allvars[i[0]] = [i[0], i[1], i[2]]
            didmodify[i[0]] = True

        for i in dta["lines"][str(j+1)]["report"][6]:
            temp = variablevalues[i[0]].copy()
            temp[i[1]] = i[3]
            allvars[i[0]] = [i[0], variablevalues[i[0]], temp]
            variablevalues[i[0]] = temp.copy()
            didmodify[i[0]] = True

        for i in dta["lines"][str(j+1)]["report"][5]:
            temp = variablevalues[i[0]].copy()
            temp[i[0]].append(i[1])
            allvars[i[0]] = [i[0], variablevalues[i[0]], temp]
            variablevalues[i[0]] = temp.copy()
            didmodify[i[0]] = True

        stp = 1
        for i in allvars:
            if i in didmodify:
                if(didmodify[i] == True):
                    st = "The variable " + allvars[i][0] + " had value " +  str(allvars[i][1]) + " and now has value " + str(allvars[i][2])
                    lines = textwrap.wrap(st, width=60)
                    for k in lines:
                        d.text((960, 110 + (stp*30)),k, fill=(0,0,255), font = fnt)
                        stp+=1
                    stp+=1
            else:
                st = "The variable " + allvars[i][0] + " had value " +  str(allvars[i][1]) + " and now has value " + str(allvars[i][2])
                lines = textwrap.wrap(st, width=60)
                for k in lines:
                    d.text((960, 110 + (stp*30)),k, fill=(0,0,0), font = fnt)
                    stp+=1
                stp+=1
        imgnm = 'img' + str(j+1) + ".png"
        img.save(imgnm)
        img2 = cv.imread(imgnm)
        height, width, layers = img2.shape
        size = (width,height)
        imgs.append(img2)
    out = cv.VideoWriter('DebuggerVideo.avi',cv.VideoWriter_fourcc(*'DIVX'), 0.5, (1920, 1080))
    for i in range(len(imgs)):
        out.write(imgs[i])
    out.release()
    for file in glob.glob("*.png"):
        os.remove(file)
    
    print("Video Saved in this folder with name DebuggerVideo.avi")
