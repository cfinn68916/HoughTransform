msg='''
this code takes an image and filters it and tries to detect straight lines with hough transform


'''

print(msg)

import math,time,random,pygame,img
from pygame.locals import *
from PIL import Image

im=Image.open(input('file path:')) #
nim=im.reduce(8)
nim3=nim.convert('L')
nim2=nim3.rotate(270)
pimgs={}
for x in range(nim2.size[0]):
    for y in range(nim2.size[1]):
        pimgs[(x,y)]=nim2.getpixel((x,y))/256
imgs=img.panp(pimgs)
sz=nim2.size[0]
tres=1.1
seg_tres=0.5

#imgs=img.panp(img.gen_fiducial())
#sz=160
print('done with setup')

def sin(i):
    return math.sin(math.radians(i))
def cos(i):
    return math.cos(math.radians(i))
def dropout(t,h,im):
    p=[]
    for i in h:
        if h[i]<t:
            p.append(i)
    for i in p:
        h.pop(i)
    return h


print('init img')
st=time.time()
res={}
for i in imgs:
    #st=time.time()
    x,y=i
    v=imgs[i]
    if v<tres:
        continue
    for th in range(901):
        theta=th/10
        r=x*cos(theta)+y*sin(theta)
        rr=int(r*10)
        if (rr,th) in res:
            res[(rr,th)]+=v
        else:
            res[(rr, th)]=v
    #end=time.time()
    #print(end-st)
all=dropout(20,res,imgs)
print(len(all))
np=[]
for i in all:
    r=i[0]/10
    t=i[1]/10
    pairs=[]
    for x in range(sz):
        if t!=0.0:
            pairs.append((x,int((r-cos(t)*x)/sin(t))))
        else:
            pairs.append((r,x))
        #if (100,38) in pairs:
            #print(x)
            #print(r)
            #time.sleep(100)
    for x,y in pairs:
        if y<0 or y>=sz:
            continue
        else:
            np.append((x,y))
rp=[]
for i in np:
    if imgs[i]>seg_tres:
        rp.append(i)



print(time.time()-st)
pygame.init()
display=pygame.display.set_mode((sz, sz))
pygame.display.update()



for x,y in rp:
    pygame.draw.rect(display, (0,0,255), pygame.Rect(x, y, 1, 1))
    
for i in imgs:
    if imgs[i]>tres:
        if min(255,int(imgs[i]*256))>100:
            pygame.draw.rect(display, (min(255,int(imgs[i]*256)),0,0), pygame.Rect(i[0], i[1], 1, 1))
            
print('red means that the line meets the threshold, blue means it detected a line')
pygame.display.update()
while True:
    pygame.display.update()
    time.sleep(0.5)
time.sleep(100)
