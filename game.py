import sys

import pygame
from pygame.locals import *

from math import cos, sin, pi, radians

from random import randint, random

from ai import match_ball, smooth_match, match_w_random, move_to_collision, cheater

width, height = 1000, 700

ball_start=width/2

ball_size = 25

ball_x,ball_y=ball_start-(ball_size/2),height/2

base_ball_speed=.5
#.5
ball_speed=base_ball_speed
ball_speed_x, ball_speed_y = -ball_speed,ball_speed
speed_increase=.25
#.25

last_impact=width/2
impact_sx,impact_sy=ball_speed_x,ball_speed_y

frame_cooldown=30
def update_ball(dt):
    global ball_x,ball_y
    global ball_speed_x,ball_speed_y,ball_speed
    global p1_wins,p2_wins
    global frame_cooldown
    global paddle1_pos,paddle2_pos
    global last_impact
    global impact_sx,impact_sy
    
    # detect vertical collisions
    if ball_y <= 0:
        ball_speed_y=abs(ball_speed_y)
    if ball_y >= height-ball_size:
        ball_speed_y=abs(ball_speed_y)*-1
    
    won=False
    # player 1 collision
    ball_center=ball_y+(ball_size/2)
    if ball_x <= paddle_width:
        if ball_center > paddle1_pos and ball_center < paddle1_pos+paddle1_length:
            ball_speed+=speed_increase*random()
            ball_speed_x,ball_speed_y = calc_new_speed(ball_y,paddle1_pos,paddle1_length)
            last_impact=ball_y
            impact_sx,impact_sy=ball_speed_x,ball_speed_y
        elif ball_x <= paddle_width-grace:
            won=True
            print("player 2 win")
            p2_wins+=1
    
    # player 2 collision
    if ball_x >= width-(paddle_width*2):
        if ball_center > paddle2_pos and ball_center < paddle2_pos+paddle1_length:
            ball_speed+=speed_increase*random()
            ball_speed_x,ball_speed_y = calc_new_speed(ball_y,paddle2_pos,paddle2_length,-1)
            last_impact=ball_y
            impact_sx,impact_sy=ball_speed_x,ball_speed_y
        elif ball_x >= width-(paddle_width*2)+grace:
            won=True
            print("player 1 win")
            p1_wins+=1
    
    if won:
        ball_x,ball_y=ball_start-(ball_size/2),(0.8*random()+0.1)*height
        ball_speed=base_ball_speed
        ball_speed_x,ball_speed_y=((randint(0,1)*2)-1)*ball_speed,0
        paddle1_pos=(height-paddle1_length)/2
        paddle2_pos=(height-paddle2_length)/2
        frame_cooldown=30
        last_impact=ball_y
        impact_sx,impact_sy=ball_speed_x,ball_speed_y
    else:
        ball_x+=ball_speed_x*dt
        ball_y+=ball_speed_y*dt

max_bounce_angle=radians(75)
def calc_new_speed(ball_y,paddle_y,paddle_height,x_mult=1):
    center_y=paddle_y+(paddle_height/2)
    relative_intersect=center_y-ball_y 
    normalized=relative_intersect/(paddle_height/2)
    # print(f"normalized: {normalized}")
    bounce_angle=normalized * max_bounce_angle
    return ball_speed*cos(bounce_angle)*x_mult,ball_speed*-sin(bounce_angle)

grace=25

paddle_width=25

paddle1_length=200
paddle1_pos=(height-paddle1_length)/2

paddle2_length=200
paddle2_pos=(height-paddle2_length)/2

paddle_speed=.4
# .4

size_decrease = 10+(ball_size/2) #so the paddle seems smaller then it actually is
double_size_decrease=size_decrease*2

pygame.init()

line_width,line_height=10,66
dashed_line=[pygame.rect.Rect((width-line_width)/2,2*n*line_height,line_width,line_height) for n in range(int(width/line_height)+1)]

fps = 60
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

getTicksLastFrame=0     

p1_bot=False
p2_bot=True
ai1=1
ai2=1

# if the ai should move to the center when stopped
ai1_center=True
ai2_center=True

# if the ai should stop when the ball is moving away
ai1_stop_turn=True
ai2_stop_turn=True

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
            paddle1_pos-=paddle_speed*dt if paddle1_pos+size_decrease > 0 else 0
        elif pressed[pygame.K_s] and not pressed[pygame.K_w]:
            paddle1_pos+=paddle_speed*dt if paddle1_pos-size_decrease < height-paddle1_length else 0
    if not p2_bot:
        if pressed[pygame.K_i] and not pressed[pygame.K_k]:
            paddle2_pos-=paddle_speed*dt if paddle2_pos+size_decrease > 0 else 0
        elif pressed[pygame.K_k] and not pressed[pygame.K_i]:
            paddle2_pos+=paddle_speed*dt if paddle1_pos-size_decrease < height-paddle2_length else 0


    # Update.
    if frame_cooldown <= 0:
        update_ball(dt)
    else:
        frame_cooldown-=1
    pygame.display.set_caption(f"Score: {p1_wins} to {p2_wins}, {round(fpsClock.get_fps()*100)/100} fps")
    
    # basic ai
    if p1_bot:
        if ball_speed_x <= 0 or not ai1_stop_turn:
            if ai1 == 1:
                paddle1_pos+=move_to_collision(paddle1_pos,paddle1_length,paddle_speed,last_impact,-impact_sx,impact_sy,width-paddle_width+ball_speed if ball_speed > 0.5 else (width-paddle_width)/2,height)*dt
            elif ai1 == 2:
                paddle1_pos+=match_ball(ball_y,paddle1_pos,paddle1_length,height,paddle_speed)*dt
            elif ai1 == 3:
                paddle1_pos+=match_w_random(ball_y,paddle1_pos,paddle1_length,height,paddle_speed)*dt
            elif ai1 == 4:
                paddle1_pos+=cheater(paddle1_pos+(paddle1_length/2),ball_y)
        elif ai1_center:
            paddle1_pos+=match_ball(height/2,paddle1_pos,paddle1_length,height,paddle_speed)*dt
    if p2_bot:
        if ball_speed_x >= 0 or not ai1_stop_turn:
            if ai2 == 1:
                paddle2_pos+=move_to_collision(paddle2_pos,paddle2_length,paddle_speed,last_impact,impact_sx,impact_sy,width-paddle_width+ball_speed  if ball_speed > 0.5 else (width-paddle_width)/2,height)*dt
            elif ai2 == 2:
                paddle2_pos+=match_ball(ball_y,paddle2_pos,paddle2_length,height,paddle_speed)*dt
            elif ai2 == 3:
                paddle2_pos+=match_w_random(ball_y,paddle2_pos,paddle2_length,height,paddle_speed)*dt
            elif ai2 == 4:
                paddle2_pos+=cheater(paddle2_pos+(paddle2_length/2),ball_y)
        elif ai2_center:
            paddle2_pos+=match_ball(height/2,paddle2_pos,paddle2_length,height,paddle_speed)*dt
    
    # draw dashed line
    for segment in dashed_line:
        pygame.draw.rect(screen,(255,255,255),segment)
    
    # draw ball
    # ball_rectangle=pygame.rect.Rect(ball_x,ball_y,ball_size,ball_size)
    # pygame.draw.rect(screen,(255,255,255),ball_rectangle)
    ball_radius=(ball_size/2)
    pygame.draw.circle(screen,(255,255,255),(ball_x+ball_radius,ball_y+ball_radius),ball_radius)
    
    # draw paddles
    paddle1_rect=pygame.rect.Rect(0,paddle1_pos+size_decrease,paddle_width,paddle1_length-double_size_decrease)
    paddle2_rect=pygame.rect.Rect(width-paddle_width,paddle2_pos+size_decrease,paddle_width,paddle2_length-double_size_decrease)
    pygame.draw.rect(screen,(255,255,255),paddle1_rect)
    pygame.draw.rect(screen,(255,255,255),paddle2_rect)
    
    pygame.display.flip()
    fpsClock.tick(fps)