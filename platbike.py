#! /usr/bin/python
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''' Alphabet Bike!                                                                       '''
'''                                                                                      '''
''' Code: Jeremy Overbay  2013                                                           '''
''' www.energyresearchlabs.com                                                           '''
'''                                                                                      '''
'''                                                                                      '''
'''                                                                                      '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''' add scrolling backgrounds. add lanes  add rotation   change jumping behavior to be based on ramps'''
import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 550
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()
    bgOne = pygame.image.load('res/bg.png').convert()

    up = down = left = right = rotright = rotleft = turbo = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#0033FF"))
    entities = pygame.sprite.Group()
    all_sprites = pygame.sprite.OrderedUpdates([entities])
    for sprite in all_sprites:
        layers.add(sprite)
    player = Player(64, 675)
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P                                                    P",
        "P               Q                                    P",
        "P                                                    P",
        "P                                                    P",
        "                                                     P",
        "                J                   E              E P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    entities.add(player)
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "Q":
                e = Ramp(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "J":
                e = Jumppixel(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "T":
                e = Tracktile(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
   # entities.add(player)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                rotleft = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                rotright = True
            if e.type == KEYDOWN and e.key == K_a:
                right = True
            if e.type == KEYDOWN and e.key == K_z:
                turbo = True

            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                rotleft = False
            if e.type == KEYUP and e.key == K_RIGHT:
                rotright = False
            if e.type == KEYUP and e.key == K_a:
                right = False
            if e.type == KEYUP and e.key == K_z:
                turbo = False


        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))
	screen.blit(bgOne,(0,(WIN_HEIGHT - 129 -32 )))

        #camera.update(player)

        # update player, draw everything else
        #player.update(up, down, left, right, rotleft, rotright, turbo, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
	#player.update(up, down, left, right, rotleft, rotright, turbo, platforms)
	#camera.update(player)
	entities.clear
	player.update(up, down, left, right, rotleft, rotright, turbo, platforms)
	camera.update(player)
	pygame.display.flip()
        #pygame.display.update()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
#        self.image = Surface((32,32))
	self.imageMaster = pygame.image.load("res/herobikea.png").convert_alpha()
	self.image = self.imageMaster
	self.rect = self.image.get_rect()
#        self.image.fill(Color("#0000FF"))
#        self.image.convert()
        self.rect = Rect(x, y, 64, 64)
    	self.dir = 0 #rotates too fast
	self.lane = 1
    def update(self, up, down, left, right, rotleft, rotright, turbo, platforms):
	self.dir = 0  #remove this to allow flips...but they are super fast.
		
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
	if rotleft:
		self.dir += 45
		if self.dir > 360:
			self.dir = 45
		
	if rotright:
		self.dir -=45
		if self.dir < 0:
			self.dir = 315
			print self.dir
	oldCenter = self.rect.center  #oldCenter is a tuple
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()

        #fix position of rotated sprite
#        if self.dir == 45 :

 #               rotcorrect = (0,-10)   #tuple to move sprite a bit
  #              rot45 = tuple(map(sum,zip(oldCenter,rotcorrect))) #combine two tuples into a third
   #             self.rect.center = rot45
  #      elif self.dir == 315 :
   #             rotcorrect = (0,-10)
    #            rot315 = tuple(map(sum,zip(oldCenter,rotcorrect)))
     #           self.rect.center = rot315
      #  else :
       #         self.rect.center = oldCenter
#        screen.blit(self.image,self.rect)
        self.rect.center = oldCenter





        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if turbo:
            self.xvel = (self.xvel *2)
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, right, oldCenter)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, right, oldCenter)
    def collide(self, xvel, yvel, platforms, right, oldCenter):
        for p in platforms:
	 #   if isinstance(p, Ramp):
                       # if self.onGround: self.yvel -= 10
	#	pass
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Jumppixel) and self.onGround:
			#print self.dir
			#if self.onGround: # and right:
	                #self.dir += 45
       		        #if self.dir > 360:
			#	self.dir = 45
			#print self.dir
        			#oldCenter = self.rect.center  #oldCenter is a tuple
        			#self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        			#self.rect = self.image.get_rect() 
				#self.rect.center = oldCenter
				#rampcorrect = (10,-10)
				#rampjump = tuple(map(sum,zip(oldCenter,rampcorrect)))
				#self.rect.center = rampjump
                        if xvel > 0:
                                self.rect.right = p.rect.left
                                print "collide right jump"
#                        if xvel < 0:
#                                self.rect.left = p.rect.right
#                                print "collide left"
#                        if yvel > 0:
#                                self.rect.bottom = p.rect.top
#                                self.onGround = True
#                                self.yvel = 0
#                        if yvel < 0:
#                                self.rect.top = p.rect.bottom
			#p.rect = p.rect.inflate(25,25)
			self.yvel -= 10
			self.xvel = 8
		else:
			if isinstance(p, ExitBlock):
				#pygame.event.post(pygame.event.Event(QUIT))
				main()
               	 	if xvel > 0:
                		self.rect.right = p.rect.left
                    		print "collide right"
                	if xvel < 0:
                    		self.rect.left = p.rect.right
                    		print "collide left"
                	if yvel > 0:
                    		self.rect.bottom = p.rect.top
                    		self.onGround = True
                    		self.yvel = 0
                	if yvel < 0:
                    		self.rect.top = p.rect.bottom
class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class Ramp(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("res/ramp1a.png").convert_alpha()
	self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 1, 1)#116, 160) #self.image.get_rect()

    def update(self):
        pass

class Jumppixel(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("res/jumppixel.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 1, 1) #self.image.get_rect()

    def update(self):
        pass



class Tracktile(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("res/tracktile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 32, 32) #self.image.get_rect()

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#000000"))

if __name__ == "__main__":
    main()
