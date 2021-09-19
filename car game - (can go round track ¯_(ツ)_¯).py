# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 10:35:04 2019

@author: sebastian
"""
import pygame

import os


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
        self.weights1=[  [ 0,0,0,0 ],[ 0,0,0,0] ,[ 0,0,0,0 ]  ]
        self.weights2=[  [ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]  ]
        self.weights3=[  [ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]  ]
    def node(self):
        self.node0=[0,0,0]
        self.node1=[0,0,0,0]
        self.node2=[0,0,0,0]
        self.node2=[0,0,0,0]
        for n in range(0,4):
            for q in range(0,3):
                temptotal+=self.weights1[q][n]*self.node[q]
            self.node1[n]=temptotal/3
            
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_og = player_img
        self.image_og.set_colorkey(white)
        self.image=self.image_og
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/4
        self.rect.bottom=HEIGHT-40
        self.speedf=0

        self.rot=0
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
            if self.wheelpos<100:
                self.wheelpos+=7

            
        if keystate[pygame.K_RIGHT]or keystate[pygame.K_d]:
            self.key=0
            if self.wheelpos>-100:
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

def ai(player,difficulty):
    try:
        timetowall= shortest[0]/abs(player.speedf)
    except:
        timetowall=9999999

    if timetowall<difficulty:
        player.speedf+=0.15
        player.rot+=3
    if timetowall>difficulty+2:
        player.speedf+=-0.15
    

    if shortest[2]<150:
        player.rot+=4
    elif shortest[2]>250:
        player.rot+=-7
    
    if shortest[1]<75:
        player.rot+=-6

        
        
    

    


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
        return(math.sqrt((intersectx-player.rect.centerx)**2+(intersecty-player.rect.centery)**2))
    else:
        return(999999999)
    

  

   



def track():
    # box lines
    pygame.draw.line(screen, black, player.rect.midleft, player.rect.midright, 2)
    pygame.draw.line(screen, black, player.rect.midtop, player.rect.midbottom, 2)


    #front line
    farpoints=[[0,0],[0,0],[0,0]]
    linelength=1400
    farpoints[0]=[player.rect.centerx-(linelength*math.cos(math.radians(player.rot))),player.rect.centery-(linelength*math.sin(math.radians(player.rot)))]
    farpoints[1]=[player.rect.centerx-(linelength*math.cos(math.radians(player.rot+45))),player.rect.centery-(linelength*math.sin(math.radians(player.rot+45)))]
    farpoints[2]=[player.rect.centerx-(linelength*math.cos(math.radians(player.rot-45))),player.rect.centery-(linelength*math.sin(math.radians(player.rot-45)))]
    
   
    pygame.draw.line(screen, black, player.rect.center, farpoints[0], 2)
    pygame.draw.line(screen, black, player.rect.center, farpoints[1], 2)
    pygame.draw.line(screen, black, player.rect.center, farpoints[2], 2)
    
 
    # track


    pygame.draw.line(screen, black, [50, 50], [1350, 50], 2)
    pygame.draw.line(screen, black, [400, 50], [400, 350], 2)
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

    


    #line distance/death
    
    line=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
    global shortest
    shortest=[9999999,99999999,9999999]
    for q in range (0,3):
        line[0]=lineintersect(([50, 50], [1351, 51]),( player.rect.center, farpoints[q]))
        line[1]=lineintersect(([400, 50], [401, 351]),( player.rect.center, farpoints[q]))
        line[2]=lineintersect(([200, 650], [701, 651]),( player.rect.center, farpoints[q]))
        line[3]=lineintersect(([200, 750], [201, 251]),( player.rect.center, farpoints[q]))
        line[4]=lineintersect(([50, 50], [51, 981]),( player.rect.center, farpoints[q]))
        line[5]=lineintersect(([700, 650], [701, 251]),( player.rect.center, farpoints[q]))
        line[6]=lineintersect(([700, 250], [1101, 251]),( player.rect.center, farpoints[q]))
        line[7]=lineintersect(([1100, 250], [1101, 751]),( player.rect.center, farpoints[q]))
        line[8]=lineintersect(([50, 980], [1351, 981]),( player.rect.center, farpoints[q]))
        line[9]=lineintersect(([1350, 50], [1351, 981]),( player.rect.center, farpoints[q]))
        line[10]=lineintersect(([500, 980], [601, 901]),( player.rect.center, farpoints[q]))
        line[11]=lineintersect(([800, 980], [701, 901]),( player.rect.center, farpoints[q]))
        line[12]=lineintersect(([600, 900], [701, 901]),( player.rect.center, farpoints[q]))
        line[13]=lineintersect(([200, 750], [1100, 751]),( player.rect.center, farpoints[q]))

        for n in range (0,len(line)):
            if line[n]<shortest[q]:
                shortest[q]=line[n]
        if shortest[q]<40:

            player.realx = 450
            player.realy=900
            player.speedf=0
            player.rot=0
            global alive
            alive=False















pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('my game')
clock = pygame.time.Clock()
player_img = pygame.image.load(os.path.join(sprite_folder, 'car.png')).convert()
background=pygame.image.load(os.path.join(sprite_folder,'background.jpg')).convert()
b=0
all_sprites = pygame.sprite.Group()
distance=0
player = Player()
all_sprites.add(player)
difficultyy=14
##text##
basicfont = pygame.font.SysFont(None, 48)

####

global running 
running=True
global alive
alive=True
time=0
old_score=0
aia=0
wait=11
waitai=0
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

    distance=distance+abs(player.speedf)
    all_sprites.draw(screen)
    track()
    
    
    
    #time and score
    time=time+1
    absolutetime=time/60
    dt=round(distance/absolutetime,0)
    
    #score display
    text = basicfont.render('Score: '+str(dt), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.centerx = WIDTH/2
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('Previous Score: '+str(old_score), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.x =0 
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('Distance: '+str(round(distance,0)), True, (255, 0, 0), (0, 0, 0))
    text.set_colorkey(black)
    textrect = text.get_rect()
    textrect.right = WIDTH
    textrect.centery = 30
    screen.blit(text, textrect)
    
    text = basicfont.render('ai: '+str(difficultyy), True, (255, 0, 0), (0, 0, 0))
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
   
  
        ai(player,difficultyy)
    waitai+=1
    
    #reset
    if alive== False:

        old_score=dt

        
        time=0
        distance=0 
        alive=True
   
    pygame.display.flip()#do last

pygame.quit()
