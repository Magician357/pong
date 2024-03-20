import sys

import pygame
from pygame.locals import *

from math import cos, sin, pi

from random import randint

ball_x,ball_y=300,300

ball_size = 25

ball_speed=0.5
ball_speed_x, ball_speed_y = ball_speed,ball_speed

frame_cooldown=30
def update_ball(dt):
    global ball_x,ball_y
    global ball_speed_x,ball_speed_y
    global p1_wins,p2_wins
    global frame_cooldown
    
    # detect vertical collisions
    if ball_y <= 0:
        ball_speed_y=abs(ball_speed_y)
    if ball_y >= height-ball_size:
        ball_speed_y=abs(ball_speed_y)*-1
    
    won=False
    # player 1 collision
    if ball_x <= paddle_width:
        if ball_y > paddle1_pos and ball_y < paddle1_pos+paddle1_length:
            ball_speed_x,ball_speed_y = calc_new_speed(ball_y,paddle1_pos,paddle1_length)
        elif ball_x <= paddle_width-grace:
            won=True
            print("player 2 win")
            p2_wins+=1
    
    # player 2 collision
    if ball_x >= width-(paddle_width*2):
        if ball_y > paddle2_pos and ball_y < paddle2_pos+paddle1_length:
            ball_speed_x,ball_speed_y = calc_new_speed(ball_y,paddle2_pos,paddle2_length,-1)
        elif ball_x >= width-(paddle_width*2)+grace:
            won=True
            print("player 1 win")
            p1_wins+=1
    
    if won:
        ball_x,ball_y=ball_start
        ball_speed_x,ball_speed_y=((randint(0,1)*2)-1)*ball_speed,((randint(0,1)*2)-1)*ball_speed
        frame_cooldown=30
    else:
        ball_x+=ball_speed_x*dt
        ball_y+=ball_speed_y*dt

max_bounce_angle=(5*pi)/12
def calc_new_speed(ball_y,paddle_y,paddle_height,x_mult=1):
    center_y=paddle_y+(paddle_height/2)
    relative_intersect=center_y-ball_y 
    normalized=relative_intersect/(paddle_height/2)
    bounce_angle=normalized * max_bounce_angle
    return ball_speed*cos(bounce_angle)*x_mult,ball_speed*-sin(bounce_angle)
grace=20

paddle_width=25

paddle1_pos=0
paddle1_length=200

paddle2_pos=0
paddle2_length=200

paddle_speed=.4

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480

ball_start=(width/2,height/2)

screen = pygame.display.set_mode((width, height))

getTicksLastFrame=0

p1_bot=False
p2_bot=True

p1_wins=0
p2_wins=0

print("""Controls:
w: player 1 up
S: player 1 down
I: player 2 up
K: player 2 down""")

# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    t = pygame.time.get_ticks()
    dt = (t - getTicksLastFrame)
    getTicksLastFrame = t
    
    pressed = pygame.key.get_pressed()
    if not p1_bot:
        if pressed[pygame.K_w] and not pressed[pygame.K_s]:
            paddle1_pos-=paddle_speed*dt if paddle1_pos > 0 else 0
        elif pressed[pygame.K_s] and not pressed[pygame.K_w]:
            paddle1_pos+=paddle_speed*dt if paddle1_pos < height-paddle1_length else 0
    if not p2_bot:
        if pressed[pygame.K_i] and not pressed[pygame.K_k]:
            paddle2_pos-=paddle_speed*dt if paddle2_pos > 0 else 0
        elif pressed[pygame.K_k] and not pressed[pygame.K_i]:
            paddle2_pos+=paddle_speed*dt if paddle1_pos < height-paddle2_length else 0


    # Update.
    if frame_cooldown <= 0:
        update_ball(dt)
    else:
        frame_cooldown-=1
    pygame.display.set_caption(f"Score: {p1_wins} to {p2_wins}")
    
    # basic ai
    if p1_bot:
        half_pos=paddle1_pos+(paddle1_length/2)
        if half_pos > ball_y and paddle2_pos > 0:
            paddle1_pos-=paddle_speed*dt
        elif half_pos < ball_y and paddle1_pos < height-paddle1_length:
            paddle1_pos+=paddle_speed*dt
    if p2_bot:
        half_pos=paddle2_pos+(paddle2_length/2)
        if half_pos > ball_y and paddle2_pos > 0:
            paddle2_pos-=paddle_speed*dt
        elif half_pos < ball_y and paddle2_pos < height-paddle2_length:
            paddle2_pos+=paddle_speed*dt
    
    # draw ball
    ball_rectangle=pygame.rect.Rect(ball_x,ball_y,ball_size,ball_size)
    pygame.draw.rect(screen,(255,255,255),ball_rectangle)
    
    # draw paddles
    paddle1_rect=pygame.rect.Rect(0,paddle1_pos,paddle_width,paddle1_length)
    paddle2_rect=pygame.rect.Rect(width-paddle_width,paddle2_pos,paddle_width,paddle2_length)
    pygame.draw.rect(screen,(255,255,255),paddle1_rect)
    pygame.draw.rect(screen,(255,255,255),paddle2_rect)
    
    pygame.display.flip()
    fpsClock.tick(fps)