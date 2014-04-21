''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''' Alphabet Bike!                                                                       '''
'''                                                                                      '''
''' Code: Jeremy Overbay  2013                                                           '''
''' www.energyresearchlabs.com                                                           '''
'''                                                                                      '''
'''                                                                                      '''
'''                                                                                      '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import pygame,sys,random, os
from collections import deque
from pygame.locals import *

#bgscrolling

bgOne = pygame.image.load('res/bg.png')
bgTwo = pygame.image.load('res/bg.png')
bgThree = pygame.image.load('res/bg2.png')
bgFour = pygame.image.load('res/bg3.png')


#bgOne_x = 0
#bgTwo_x = bgOne.get_width()



#global init
pygame.init()
size = 800,600
textcolor = 233,230,20
speed = -3
up = right = True 
down = left = False
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Alphabet Bike')
bg = pygame.image.load("res/bg.png")  #replace with scrolling background
bgrect = bg.get_rect()
pygame.key.set_repeat(65,65)
	
class Enemy:
    	'Doc: Class Enemy represents the enemy racers'
    	def __init__(self,lane):
        	self.img = pygame.image.load("res/bike.png")
        	self.rect = self.img.get_rect()
		if lane == 1:
			self.rect = self.rect.move(730,195)
		elif lane == 2:
			self.rect = self.rect.move(730,270)
		elif lane == 3:
			self.rect = self.rect.move(730,355)
                elif lane == 4:
                        self.rect = self.rect.move(730,440)
    	
	def left(self):
        	return self.rect.left
    	
	def right(self):
        	return self.rect.right
    	
	def top(self):
        	return self.rect.top
    	
	def bottom(self):
        	return self.rect.bottom
    	
	def move(self,x,y):
        	self.rect = self.rect.move(x,y)
    	
	def render(self):
        	screen.blit(self.img,self.rect)

	def get_rectangle(self):
		return self.rect


class Hero:
	'Doc: Your bike which will be dodging enemies that belong to the class Enemy'
	def __init__(self):
		self.imgMaster = pygame.image.load("res/herobike.png")
		#self.imgMaster = self.imgMaster.convert()
		self.img = self.imgMaster
		self.rect = self.img.get_rect()
		#self.rect = self.rect.move(240,270)
		self.rect.center = (272, 264)
		self.dir = 0
		self.lane = 2
	
	def left(self):
		return self.rect.left
	
	def right(self):
		return self.rect.right
	
	def top(self):
		return self.rect.top
	
	def bottom(self):
		return self.rect.bottom
	
	#some automata and states logic went here o_O
	def move(self,key):
	
		if key == up  and self.lane == 1:
			#self.rect = self.rect.move(0,0)
			self.lane = 1
		
		elif key == up and self.lane == 2:
			self.rect = self.rect.move(0,-32)
			self.lane = 1
		
		elif key == up and self.lane == 3:
			self.rect = self.rect.move(0,-32)
			self.lane = 2

                elif key == up and self.lane == 4:
                        self.rect = self.rect.move(0,-32)
                        self.lane = 3
		
		elif key == down and self.lane == 1:
			self.rect = self.rect.move(0,32)
			self.lane = 2
		
		elif key == down and self.lane == 2:
			self.rect = self.rect.move(0,32)
			self.lane = 3
		
		elif key == down and self.lane == 3:
			self.rect = self.rect.move(0,32)
			self.lane = 4

                elif key == down and self.lane == 4:
                        #self.rect = self.rect.move(0,0)
                        self.lane = 4

	def render(self):
		oldCenter = self.rect.center
		self.img = pygame.transform.rotate(self.imgMaster, self.dir)
		self.rect = self.img.get_rect()
		self.rect.center = oldCenter
		screen.blit(self.img,self.rect)
	
	def shift(self, d):
		
		if d == right:
			if self.rect.right < 750:
				self.rect = self.rect.move(10,0)
		elif d == left:
			if self.rect.left > 20:
				self.rect = self.rect.move(-10,0)


#        def rot_center(self):
#                #loc = self.img.get_rect().center
#                #self.img = pygame.transform.rotate(self.img,5)
#                #self.img.get_rect().center = loc
#               # self.rect = self.img.get_rect() #this line puts image in upper left hand corner. :{
#                oldCenter = self.rect.center
#                self.img = pygame.transform.rotate(self.imgMaster, self.dir)
#                self.rect = self.img.get_rect()
#                self.rect.center = oldCenter
#                return self.img
#
	def rot_left(self):
		self.dir += 45
		if self.dir > 360:
			self.dir = 45

        def rot_right(self):
                self.dir -= 45
                if self.dir < 0:
                        self.dir = 315



	def jump(self):
		self.rect = self.rect.move(0,-25)
		
	def unjump(self):
		self.rect = self.rect.move(0,25)
	
	def get_lane(self):
		return self.lane


#def bgscroll():
	
#        bgOne_x = 0
#        bgTwo_x = bgOne.get_width()

# 	screen.blit(bgOne, (bgOne_x, 0))
#	screen.blit(bgTwo, (bgTwo_x, 0))

#	pygame.display.update()

#	bgOne_x -= 1
#	bgTwo_x -= 1

#	if bgOne_x <= -1 * bgOne.get_width():
#		bgOne_x = bgTwo_x + bgTwo.get_width()
#	if bgTwo_x <= -1 * bgTwo.get_width():
#		bgTwo_x = bgOne_x + bgOne.get_width()

#play again? :)
def re_play():
	gover = pygame.image.load("res/gover.png")
	grect = gover.get_rect()

	#Play again please :D
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		screen.fill((55,200,44))
		screen.blit(gover,grect)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE]: break
		if pressed[pygame.K_ESCAPE]: sys.exit()
		if pressed[pygame.K_q]: sys.exit()
		pygame.display.flip()
	begin()


#oops gameover condition
def gameover(x,y):
	tempscreen = pygame.image.load("res/gameover.jpeg")
	trect = tempscreen.get_rect()
	boom = pygame.image.load("res/crash.png")
	brect = boom.get_rect()
	brect = brect.move(x,y)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		screen.blit(tempscreen,trect)
		screen.blit(boom,brect)
		
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_RETURN]:break
                if pressed[pygame.K_ESCAPE]:break
                if pressed[pygame.K_q]:break

		pygame.display.flip()

	re_play()


#Lets BEGIN :D
def begin():
	
	#queues of cars in different lanes
	car1 = deque()
	car2 = deque()
	car3 = deque()
	
	#your car
	hero = Hero()

	score = 0
	timer = 32

	myfont = pygame.font.Font(None,18)	
	clock = pygame.time.Clock()
	bgOne_x = 0
	bgTwo_x = bgOne.get_width()
        bgThree_x = 0
        bgFour_x = bgThree.get_width()

	#the game loop
	while 1:
        	clock.tick(60)
#        	for event in pygame.event.get():
#            		if event.type == pygame.QUIT: sys.exit()
        
		#screen.blit(bg,bgrect)
		screen.blit(bgOne, (bgOne_x, 0))
		screen.blit(bgTwo, (bgTwo_x, 0))
                screen.blit(bgThree, (bgThree_x, 0))
                screen.blit(bgFour, (bgFour_x, 0))
#                bgOne_x -= 10
#                bgTwo_x -= 10


		if bgOne_x <= -1 * bgOne.get_width():
			 bgOne_x = bgTwo_x + bgTwo.get_width()
		if bgTwo_x <= -1 * bgTwo.get_width():
			bgTwo_x = bgOne_x + bgOne.get_width()
		
                if bgThree_x <= -1 * bgThree.get_width():
                         bgThree_x = bgFour_x + bgFour.get_width()
                if bgFour_x <= -1 * bgFour.get_width():
                        bgFour_x = bgThree_x + bgThree.get_width()

		#scoreboard
		if pygame.time.get_ticks()%200: score = score + 1
		scoreline = "DISTANCE: "+str(score)
		scoreboard = myfont.render(scoreline,1,textcolor)
		screen.blit(scoreboard,scoreboard.get_rect())
		 
		#car AI
#		if pygame.time.get_ticks() % (100*random.randint(2,6)) == 0:
#			car1.append(Enemy(1))
#		if pygame.time.get_ticks() % (100*random.randint(3,5)) == 0:
#			car2.append(Enemy(2))
#		if pygame.time.get_ticks() % (100*random.randint(1,5)) == 0:
#			car3.append(Enemy(3))

        	#move and render cars in diff lanes
#		for car in car1:
#            		car.move(speed,0)
#            		car.render()
#		for car in car2:
#			car.move(speed,0)
#			car.render()
#		for car in car3:
#			car.move(speed-1,0)
#			car.render()
			
		moved = 0

		#User Input
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_UP:
					hero.move(up)
			
				elif event.key == pygame.K_DOWN:
					hero.move(down)
				
				elif event.key == pygame.K_a:
					bgOne_x -= 25
					bgTwo_x -= 25
                                        bgThree_x -= 25
                                        bgFour_x -= 25



				elif event.key == pygame.K_RIGHT:
					#hero.shift(right)
                                        hero.rot_right()
	
				elif event.key == pygame.K_LEFT:
					#hero.shift(left)
					hero.rot_left()
                                elif event.key == pygame.K_ESCAPE:
                                        sys.exit()
				
				#elif event.key == pygame.K_SPACE:
				#	hero.jump()
				#	moved = 1
					
		
		hero.render()

		#Collision Detection
		for car in car1:
			if hero.get_lane()==1:
				if car.left() < hero.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
				
				if car.left() in range(hero.right()-2,hero.right()+2,1): 
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
		
				if car.right() == hero.left()+1:
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
		
		for car in car2:
			if hero.get_lane()==2:
		 		if car.left() < hero.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])

				if car.left() in range(hero.right()-2,hero.right()+2,1):
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

                        	if car.right() == hero.left()+1:
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])
		
		for car in car3:
			if hero.get_lane()==3:
		 		if car.left() < hero.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])

				if car.left() in range(hero.right()-2,hero.right()+2,1):
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

                        	if car.right() == hero.left()+1:
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

		#if moved == 1:
                        #hero.unjump()

		#memory cleanup
		if car1:
			if car1[0].right() < 0: car1.popleft()
		if car2:
			if car2[0].right() < 0: car2.popleft()
		if car3:
			if car3[0].right() < 0: car3.popleft()
	
		pygame.display.flip()

def main():

	#draw the welcome screen
	welcome = pygame.image.load("res/welcome.png")
	wrect = welcome.get_rect()
	wrect = wrect.move(40,40)

	#wait till the user presses "enter" key
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		screen.fill((55,200,44))
 		screen.blit(welcome,wrect)
		pressed = pygame.key.get_pressed()
		
		if pressed[pygame.K_RETURN]: break
                if pressed[pygame.K_ESCAPE]: sys.exit()
                if pressed[pygame.K_q]: sys.exit()

		pygame.display.flip()
	
	#BEGIN THE GAME :D
	begin()

if __name__ == "__main__":
	main()
