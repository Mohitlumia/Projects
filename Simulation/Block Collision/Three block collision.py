'''import pygame_sdl2
pygame_sdl2.import_as_pygame()'''
import pygame
import math

class Square(object):
	def __init__(self, size, XY, mass, velocity):
		self.x = XY[0]
		self.y = XY[1]
		self.mass = mass
		self.v = velocity
		self.size = size
		
	def collision(self, otherblock):
		if self.x + self.size < otherblock.x or self.x > otherblock.x + otherblock.size:
			return False
		else:
			return True

	def NewVelocity(self, otherblock):
		sumM = self.mass + otherblock.mass
		newV = (self.mass - otherblock.mass)/ sumM * self.v
		newV += (2 * otherblock.mass/ sumM) * otherblock.v
		return newV

	def Newvelocity(self, otherblock):
		sumM = self.mass + otherblock.mass
		newV = (self.mass - otherblock.mass)/ sumM * self.v
		newV += (2 * otherblock.mass/ sumM) * otherblock.v
		return newV

	def collide_wall(self):
		if self.x <= 0:
			self.v *= -1
			return True

	def update(self):
		self.x += self.v

	def draw(self, background, otherblock, anotherblock):
		if self.x < 0:
			pygame.draw.rect(background, red, [0, self.y, self.size, self.size])
			pygame.draw.rect(background, red, [10, otherblock.y, otherblock.size, otherblock.size])
		else:
			pygame.draw.rect(background, red, [self.x, self.y, self.size, self.size])
			pygame.draw.rect(background, red, [otherblock.x, otherblock.y, otherblock.size, otherblock.size])
			pygame.draw.rect(background, red, [anotherblock.x, anotherblock.y, anotherblock.size, anotherblock.size])


def redraw():
	background.fill(white)
	pygame.draw.rect(background, gray, [0,0, 800, 250])
	SquareBig.draw(background, SquareSmall, SquareMid)
	font = pygame.font.SysFont(None, 50)
	text = font.render(str(count), True, (0,0,0))
	background.blit(text, [100, 270])
	pygame.display.update()

width, height = 800, 400
white = (255, 255, 255)
gray = (190, 190, 190)
red = (200, 0, 0)

pygame.init()
power = math.pow(100, 2)
background = pygame.display.set_mode((width, height))

SquareBig = Square(50, (320, 200), power, -0.9/1000)
SquareMid = Square(30, (250, 220), 50, 0)
SquareSmall = Square(10, (150, 240), 10, 0)


count = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	for i in range(1000):
		if (SquareSmall.collision(SquareMid)):
			count += 1
			v1 = SquareSmall.NewVelocity(SquareMid)
			v2 = SquareMid.NewVelocity(SquareSmall)
			SquareSmall.v = v1
			SquareMid.v = v2

		if (SquareMid.collision(SquareBig)):
			count += 1
			v2 = SquareMid.Newvelocity(SquareBig)
			v3 = SquareBig.Newvelocity(SquareMid)
			SquareMid.v = v2
			SquareBig.v = v3
		
		if SquareSmall.collide_wall():
			count += 1
		SquareBig.update()
		SquareMid.update()
		SquareSmall.update()
	redraw()


pygame.quit()