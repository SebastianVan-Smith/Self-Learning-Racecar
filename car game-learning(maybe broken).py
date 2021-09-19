# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 10:35:04 2019

@author: sebastian
"""
import pygame

import os

import random
import math




WIDTH =1400
HEIGHT=1000
FPS=60
white=(255,255,255)
black= (0,0,0)
red=(255,0,0)
green=(0,255,0)
yellow=(255,255,0)
rotationspeed=100

#folders
game_folder = os.path.dirname(__file__)
img_folder =os.path.join(game_folder,'img')
sprite_folder=os.path.join(img_folder,'Player')

class AI():
    def structure(self):
        self.weights1=[  [ 2,2,2,2,2 ],[ 2,2,2,2,2 ],[ 2,2,2,2,2 ],[ 2,2,2,2,2 ]  ]
        self.weights2=[  [ 2,2,2,2 ],[ 2,2,2,2 ],[ 2,2,2,2 ],[ 2,2,2,2 ]  ]
        self.weights3=[  [ 2,2,2,2 ],[ 2,2,2,2 ],[ 2,2,2,2 ],[ 2,2,2,2 ]  ]
        for n in range (0,4):
            for q in range (0,5):
                self.weights1[n][q]=(random.uniform(-1,1))
        for n in range (0,4):
            for q in range (0,4):
                self.weights2[n][q]=(random.uniform(-1,1))
        for n in range (0,4):
            for q in range (0,4):
                self.weights3[n][q]=(random.uniform(-1,1))
        self.node0=[0,0,0,0,0]
        self.node1=[0,0,0,0]
        self.node2=[0,0,0,0]
        self.node3=[0,0,0,0]
    def node(self):

        #layer 2
        for n in range(0,4):
            temptotal=0
            for q in range(0,5):
                temptotal+=(self.weights1[n][q]*self.node0[q])
            self.node1[n]=temptotal

        #layer 3
        for n in range(0,4):
            temptotal=0
            for q in range(0,4):
                temptotal+=(self.weights2[n][q]*self.node1[q])
            self.node2[n]=temptotal

        #lastlayer
        for n in range(0,4):
            temptotal=0
            for q in range(0,4):
                temptotal+=(self.weights3[n][q]*self.node2[q])
            self.node3[n]=temptotal
        
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_og = player_img
        self.image_og.set_colorkey(white)
        self.image=self.image_og
        self.rect=self.image.get_rect()
        self.rect.x = 100
        self.rect.y=150
        self.speedf=0

        self.rot=180
        self.wait=0
        self.realx=self.rect.x
        self.realy=self.rect.y
        self.length=0.5
        self.wheelpos=0
        self.circle_radius=0
        self.key=0
        self.steeringcenteringforce=0.5

    def rotate (self):
       new_image=pygame.transform.rotate(self.image_og,-self.rot) 

       old_center=self.rect.center
       self.image=new_image
       self.rect=self.image.get_rect()

       self.rect.center=old_center


        
    def update(self):
        #slowdown
        if self.key != 0:
            self.wheelpos=self.wheelpos*self.steeringcenteringforce
        self.key=1
        self.speedf=self.speedf*0.995
        
        if self.speedf>-2.5 and self.wait>40:
            self.speedf=0
            self.wait=0       
        if self.speedf>-2.5:
            self.wait=self.wait+1
            
        #control    
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]or keystate[pygame.K_a]:
            self.key=0
            if self.wheelpos<90:
                self.wheelpos+=7

            
        if keystate[pygame.K_RIGHT]or keystate[pygame.K_d]:
            self.key=0
            if self.wheelpos>-90:
                self.wheelpos+=-7
            
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedf=self.speedf-0.15
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedf=self.speedf+0.15
            
 
        #update        
              



        self.rot+=self.wheelpos*self.speedf*0.005

        tempx=self.speedf*math.cos(math.radians(self.rot))
        tempy=self.speedf*math.sin(math.radians(self.rot))
    
        self.realx+=tempx
        self.realy+=tempy

 


  
                    
                    
                    
            
        self.rotate()
        
        self.rect.centerx=self.realx
        self.rect.centery=self.realy


def sigmoid(x):
    return x / (1 + abs(x))

def ai():
    global f
    global gen
    global alive
    global aiammount
    for n in range (0,aiammount):
        for ee in range(0,5):
            ailist[gen][n].node0[ee]=round(shortest[n][ee],6)

        ailist[gen][n].node()

        if ailist[gen][n].node3[0] >0:
            players[n].speedf=players[n].speedf-0.15
        if ailist[gen][n].node3[1] >0:
            players[n].speedf=players[n].speedf+0.15
        if ailist[gen][n].node3[2] >0 :
            players[n].key=0
            if players[n].wheelpos<90:
                players[n].wheelpos+=7
        if ailist[gen][n].node3[3] >0 :
            players[n].key=0
            if players[n].wheelpos>-90:
                players[n].wheelpos+=-7
       
        if score[n] >scoremax[n]:
            scoremax[n]=score[n]
        

   
    
    
    
    
   
    print(f,gen,score[0])

    
    if f >300 and gen <=10:
        print(scoremax)
        
        scoremaxmax=0
        parent=0
            
        for p in range (0,aiammount):
            if scoremaxmax<scoremax[p]:
                scoremaxmax=scoremax[p]

        for t in range (0,aiammount):
            if scoremax[t]==scoremaxmax:
                parent=t
        print(scoremaxmax,parent)
        for go in range(0,aiammount):
            score[go]=0
        
        for got in range(0,aiammount):
            scoremax[got]=0
        scoremaxmax=0
        
        
        
        for d in range(0,5):
            for n in range (0,4):
                for q in range (0,5):
                    
                    ailist[gen+1][d].weights1[n][q]=ailist[gen][parent].weights1[n][q]

            for e in range (0,4):
                for q in range (0,4):
                    ailist[gen+1][d].weights2[e][q]=ailist[gen][parent].weights2[e][q]

            for r in range (0,4):
                for q in range (0,4):
                    ailist[gen+1][d].weights3[r][q]=ailist[gen][parent].weights3[r][q]
        
        
        for d in range(5,aiammount):
            for n in range (0,4):
                for q in range (0,5):
                    
                    ailist[gen+1][d].weights1[n][q]=ailist[gen][parent].weights1[n][q]+(random.uniform(-0.5,0.5))

            for e in range (0,4):
                for q in range (0,4):
                    ailist[gen+1][d].weights2[e][q]=ailist[gen][parent].weights2[e][q]+(random.uniform(-0.5,0.5))

            for r in range (0,4):
                for q in range (0,4):
                    ailist[gen+1][d].weights3[r][q]=ailist[gen][parent].weights3[r][q]+(random.uniform(-0.5,0.5))
        
    
        
        
        for n in range (0,aiammount):
            alive[n]=False  
            
            
                        
            
            
        
        f=0
        gen=gen+1

    elif f >600+gen*5 and gen >10:
            print(score)
            scoremaxmax=0
            parent=0
                
            for p in range (0,aiammount):
                if scoremaxmax<scoremax[p]:
                    scoremaxmax=scoremax[p]
    
            for t in range (0,aiammount):
                if scoremax[t]==scoremaxmax:
                    parent=t
            print(scoremaxmax,parent)
            for go in range(0,aiammount):
                score[go]=0
            
            for got in range(0,aiammount):
                scoremax[got]=0
            scoremaxmax=0
            
            
            
            for d in range(0,5):
                for n in range (0,4):
                    for q in range (0,5):
                        
                        ailist[gen+1][d].weights1[n][q]=ailist[gen][parent].weights1[n][q]
    
                for e in range (0,4):
                    for q in range (0,4):
                        ailist[gen+1][d].weights2[e][q]=ailist[gen][parent].weights2[e][q]
    
                for r in range (0,4):
                    for q in range (0,4):
                        ailist[gen+1][d].weights3[r][q]=ailist[gen][parent].weights3[r][q]
            
            
            for d in range(5,aiammount):
                for n in range (0,4):
                    for q in range (0,5):
                        
                        ailist[gen+1][d].weights1[n][q]=ailist[gen][parent].weights1[n][q]+(random.uniform(-0.4,0.4))
    
                for e in range (0,4):
                    for q in range (0,4):
                        ailist[gen+1][d].weights2[e][q]=ailist[gen][parent].weights2[e][q]+(random.uniform(-0.4,0.4))
    
                for r in range (0,4):
                    for q in range (0,4):
                        ailist[gen+1][d].weights3[r][q]=ailist[gen][parent].weights3[r][q]+(random.uniform(-0.4,0.4))
            
        
            
            
            for n in range (0,aiammount):
                alive[n]=False  
                
                
                            
                
                
    
            f=0
            gen=gen+1





def lineintersect(line1,line2):
 
    line1x=line1[0][0]-line1[1][0]
    line1y=line1[0][1]-line1[1][1]
    line1grad=line1y/line1x
    line1intersect=line1[0][1]-line1grad*line1[0][0]
        
    try:
   
        line2x=line2[0][0]-line2[1][0]
        line2y=line2[0][1]-line2[1][1]
        line2grad=line2y/line2x
    except:
        line2grad=999999

    line2intersect=line2[0][1]-line2grad*line2[0][0]
    
    intersectx=(line2intersect-line1intersect)/(line1grad-line2grad)
    intersecty=line1grad*intersectx+line1intersect
    if line1[0][0]<line1[1][0]:
        smallline1x=line1[0][0]
        largeline1x=line1[1][0]
    else:
        smallline1x=line1[1][0]
        largeline1x=line1[0][0]
    
    
    if line2[0][0]<line2[1][0]:
        smallline2x=line2[0][0]
        largeline2x=line2[1][0]
    else:
        smallline2x=line2[1][0]
        largeline2x=line2[0][0]
    
    
    if smallline1x<smallline2x:
        smalllinex=smallline2x
    else:
        smalllinex=smallline1x
    
    
    if largeline1x<largeline2x:
        largelinex=largeline1x
    else:
        largelinex=largeline2x
    if smalllinex<0:
        smalllinex=0
    
    if intersectx<largelinex and intersectx>smalllinex:
        return(math.sqrt((intersectx-line2[0][0])**2+(intersecty-line2[0][1])**2))
    else:
        return(999999999)
    

  

   



def track():
    # track
    pygame.draw.line(screen, black, [50, 50], [1350, 50], 2)
    pygame.draw.line(screen, black, [400, 50], [400, 450], 2)
    pygame.draw.line(screen, black, [200, 650], [700, 650], 2)
    pygame.draw.line(screen, black, [200, 750], [200, 253], 2)
    pygame.draw.line(screen, black, [50, 50], [50, 980], 2)
    pygame.draw.line(screen, black, [700, 650], [700, 250], 2)  
    pygame.draw.line(screen, black, [700, 250], [1100, 250], 2) 
    pygame.draw.line(screen, black, [1100, 250], [1100, 750], 2)
    pygame.draw.line(screen, black, [50, 980], [1350, 980], 2)
    pygame.draw.line(screen, black, [1350, 50], [1350, 980], 2)
    pygame.draw.line(screen, black, [200, 750], [1100, 750], 2)
    

    
    pygame.draw.line(screen, black, [500, 980], [600, 900], 2)
    pygame.draw.line(screen, black, [800, 980], [700, 900], 2)
    pygame.draw.line(screen, black, [600, 900], [700, 900], 2)

    # box lines
 
    #pygame.draw.line(screen, black, player.rect.midleft, player.rect.midright, 2)
    #pygame.draw.line(screen, black, player.rect.midtop, player.rect.midbottom, 2)


    #front line
    global shortest
    global aiammount
    shortest=[]
    for n in range(0,aiammount):
        shortest.append([9999999,99999999,9999999,9999999,9999999])
    for pp in range (0,aiammount):
        farpoints=[[0,0],[0,0],[0,0],[0,0],[0,0]]
        linelength=1400
        farpoints[0]=[players[pp].rect.centerx-(linelength*math.cos(math.radians(players[pp].rot))),players[pp].rect.centery-(linelength*math.sin(math.radians(players[pp].rot)))]
        farpoints[1]=[players[pp].rect.centerx-(linelength*math.cos(math.radians(players[pp].rot+45))),players[pp].rect.centery-(linelength*math.sin(math.radians(players[pp].rot+45)))]
        farpoints[2]=[players[pp].rect.centerx-(linelength*math.cos(math.radians(players[pp].rot-45))),players[pp].rect.centery-(linelength*math.sin(math.radians(players[pp].rot-45)))]
        farpoints[3]=[players[pp].rect.centerx-(linelength*math.cos(math.radians(players[pp].rot+89))),players[pp].rect.centery-(linelength*math.sin(math.radians(players[pp].rot+90)))]
        farpoints[4]=[players[pp].rect.centerx-(linelength*math.cos(math.radians(players[pp].rot-89))),players[pp].rect.centery-(linelength*math.sin(math.radians(players[pp].rot-90)))]
        

       
        #pygame.draw.line(screen, black, players[pp].rect.center, farpoints[0], 2)
        #pygame.draw.line(screen, black, players[pp].rect.center, farpoints[1], 2)
        #pygame.draw.line(screen, black, players[pp].rect.center, farpoints[2], 2)
        #pygame.draw.line(screen, black, players[pp].rect.center, farpoints[3], 2)
        #pygame.draw.line(screen, black, players[pp].rect.center, farpoints[4], 2)
     
        
    
    
    
        
    
    
        #line distance/death
        
        line=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
        
        for q in range (0,5):
            line[0]=lineintersect(([50, 50], [1351, 51]),( players[pp].rect.center, farpoints[q]))
            line[1]=lineintersect(([400, 50], [401, 451]),( players[pp].rect.center, farpoints[q]))
            line[2]=lineintersect(([200, 650], [701, 651]),( players[pp].rect.center, farpoints[q]))
            line[3]=lineintersect(([200, 750], [201, 251]),( players[pp].rect.center, farpoints[q]))
            line[4]=lineintersect(([50, 50], [51, 981]),( players[pp].rect.center, farpoints[q]))
            line[5]=lineintersect(([700, 650], [701, 251]),( players[pp].rect.center, farpoints[q]))
            line[6]=lineintersect(([700, 250], [1101, 251]),( players[pp].rect.center, farpoints[q]))
            line[7]=lineintersect(([1100, 250], [1101, 751]),( players[pp].rect.center, farpoints[q]))
            line[8]=lineintersect(([50, 980], [1351, 981]),( players[pp].rect.center, farpoints[q]))
            line[9]=lineintersect(([1350, 50], [1351, 981]),( players[pp].rect.center, farpoints[q]))
            line[10]=lineintersect(([500, 980], [601, 901]),( players[pp].rect.center, farpoints[q]))
            line[11]=lineintersect(([800, 980], [701, 901]),( players[pp].rect.center, farpoints[q]))
            line[12]=lineintersect(([600, 900], [701, 901]),( players[pp].rect.center, farpoints[q]))
            line[13]=lineintersect(([200, 750], [1100, 751]),( players[pp].rect.center, farpoints[q]))
    
            for n in range (0,len(line)):
                
                if line[n]<shortest[pp][q]:
                    shortest[pp][q]=line[n]
                
            if shortest[pp][q]<40 and q<3:

            
                global alive
                alive[pp]=False















pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('my game')
clock = pygame.time.Clock()
player_img = pygame.image.load(os.path.join(sprite_folder, 'car.png')).convert()
background=pygame.image.load(os.path.join(sprite_folder,'background.jpg')).convert()
b=0
all_sprites = pygame.sprite.Group()

#####################player = Player()
global aiammount
aiammount=50
##############################################all_sprites.add(player)
difficultyy=14
##text##
basicfont = pygame.font.SysFont(None, 48)
global ailist
ailist=[[]]
for q in range (0,200):
    ailist.append([])
    for n in range (0,aiammount):
        ailist[q].append(AI())
        ailist[q][n].structure()

    

####

players=[]
for n in range (0,aiammount):
    players.append(Player())

    all_sprites.add(players[n])
global ttime
ttime=100
global running 
running=True
global alive


alive=[]
for n in range (0,aiammount):
    alive.append(True)


time=[]
for n in range(0,aiammount): 
    time.append(0)


distance=[]
for n in range (0,aiammount):
    distance.append(0)

global score
score=[]
for n in range (0,aiammount):
    score.append(0)
print(score)
aia=0
wait=11
waitai=0

global f
f=0

global scoremax
scoremax=[]

#scoremax=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for n in range (0,aiammount):
    scoremax.append(0)
print(scoremax)
global gen
gen=0
while running==True:
    #event
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False




    #update
    all_sprites.update()
    screen.fill(black)
    screen.blit(background,background.get_rect())
    
    #draw

    
    all_sprites.draw(screen)
    track()
    
    
    
    #time and score
    for tt in range(0,aiammount):
        distance[tt]=distance[tt]-(players[tt].speedf)########abs(players[tt].speedf)
        time[tt]=time[tt]+1
        absolutetime=time[tt]/60
        dt=round(distance[tt]/absolutetime,0)
        score[tt]=distance[tt]

    #score display
    text = basicfont.render('Score: '+str(score[0]), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.centerx = WIDTH/2
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('Previous Score: '+str(1), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.x =0 
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('Distance: '+str(round(distance[0],0)), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.right = WIDTH
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('Gen: '+str(gen+1), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.x = 0
    textrect.centery = 60
    screen.blit(text, textrect)
    
    
    
    #16 min
    keystate=pygame.key.get_pressed()
    if keystate[pygame.K_p]and wait>10:
        if aia==1:
            aia=0
            wait=0
        if aia==0 and wait>10:
            aia=1
            wait=0
    wait=wait+1
    if keystate[pygame.K_o] and waitai>5:
        difficultyy+=5
        waitai=0
    if keystate[pygame.K_i]and waitai>5:
        difficultyy+=-5
        waitai=0
    
    if aia==1:
   
        
        ai()
        f=f+1
        
    waitai+=1
    
    #reset
    
    for ww in range (0,aiammount):
        if alive[ww]== False:
    

    
            players[ww].realx = 100#500 350
            players[ww].realy=150#900 80
            players[ww].speedf=0
            players[ww].rot=180

            time[ww]=0
            distance[ww]=0 
            alive[ww]=True
   
    pygame.display.flip()#do last

pygame.quit()
