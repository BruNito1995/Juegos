"""
Snake game
"""
import pygame
import numpy as np
import random
import os

height = 500
width = 500
rows = 25
gap = int(height/rows)
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 16)




screen = pygame.display.set_mode((width, height))

FPS = 15
fpsClock = pygame.time.Clock()

class cube(object):

    def __init__(self, pos, color):
        self.pos = pos 
        self.color = color

    def draw(self):
        square = pygame.Rect(self.pos[0]*gap,self.pos[1]*gap, gap, gap)
        pygame.draw.rect(screen, self.color, square)

    def copy(self):
        return cube(self.pos.copy(), self.color)



def move(snake, dirx, diry):
    
    for i in range(len(snake)-1,0,-1):
        snake[i].pos[0] = snake[i-1].pos[0]
        snake[i].pos[1] = snake[i-1].pos[1]
    
    snake[0].pos[0] += dirx
    snake[0].pos[1] += diry

    return snake

def generateFood(snake):
    foodPos = np.array([random.randint(0,rows-1), random.randint(0,rows-1)])
    color = (255, 0, 0)
    i = 0
    while i < len(snake):
        if (snake[i].pos == foodPos).all():
            i = -1
            foodPos = np.array([random.randint(0,rows-1), random.randint(0,rows-1)])
        i += 1
    return cube(foodPos, color)

def checkEat(food, snake):
    if (food.pos == snake[0].pos).all():
        snake.append(snake[-1].copy())
        food = generateFood(snake)
    
    return food

def checkAlive(snake):
    #morir por pasarse de la pantalla
    if snake[0].pos[0] < 0:
        return False
    
    elif snake[0].pos[0] >= rows:
        return False

    elif snake[0].pos[1] < 0:
        return False

    elif snake[0].pos[1] >= rows:
        return False

    #morir por chocar
    for i in snake[1:]:
        if (snake[0].pos == i.pos).all():
            return False

    return True


def main():
    global snake
    #init
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SANKE ---- SNAKE ---- SNAKE")
    dirx = 1
    diry = 0

    dirxOld = 1
    diryOld = 0


    snake = [] 

    snake.append(cube(np.array([10,10]), (0,255,0)))
    snake.append(cube(np.array([10,11]), (0,255,0)))
    snake.append(cube(np.array([10,12]), (0,255,0)))
    snake.append(cube(np.array([10,13]), (0,255,0)))
    snake.append(cube(np.array([10,14]), (0,255,0)))
    snake.append(cube(np.array([10,15]), (0,255,0)))

    food = generateFood(snake)

    running = True
    while running == True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            key_input = pygame.key.get_pressed()   
            if key_input[pygame.K_LEFT]:
                dirx = -1
                diry = 0

 

            elif key_input[pygame.K_UP]:
                dirx = 0
                diry = -1
                
                

            elif key_input[pygame.K_RIGHT]:
                dirx = 1
                diry = 0
                

            elif key_input[pygame.K_DOWN]:
                dirx = 0
                diry = 1
        
        
        screen.fill((0,0,0))

       

        #check that it is not goint to the opposite direction
        if dirx*dirxOld + diry*diryOld == -1:
            dirx = dirxOld
            diry = diryOld

        snake = move(snake, dirx, diry)

        if checkAlive(snake) == False:
            running = False


        dirxOld = dirx
        diryOld = diry

        food = checkEat(food,snake)
        
        for i in snake:
            i.draw()
            
        food.draw()
        score = len(snake)- 6
        scoretext = myfont.render('Score = ' + str(score), False, (0,255,255))
        screen.blit(scoretext,(0,0))

        FPS = int(15 + score/5)
        
        pygame.display.update()
        fpsClock.tick(FPS)



main()

#perdimos
screen.fill((0,0,0))
myfont2 = pygame.font.SysFont("arial", 40)
gameoverText = myfont2.render('GAME OVER: Score = ' + str(len(snake)), False, (255,255,255))
retryText = myfont2.render('PRESS ENTER TO RETRY', False, (255,255,255))
screen.blit(gameoverText,(20,20))
screen.blit(retryText,(20,250))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_RETURN]:
            pygame.quit()
            os.system('python snake.py')



            

