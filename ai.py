def match_ball(ball_y,paddle_pos,paddle_length,height,paddle_speed):

    half_pos=paddle_pos+(paddle_length/2)
    difference=ball_y-half_pos
    threshold=(paddle_length/8)
    if difference < -threshold and paddle_pos > 0:
        return -paddle_speed
    elif difference > threshold and paddle_pos < height-paddle_length:
        return paddle_speed
    return 0

from random import random

cur_offset=0
def match_w_random(ball_y,paddle_pos,paddle_length,height,paddle_speed):
    global cur_offset

    cur_offset+=(random()*4)-2
    cur_offset/=3
    # print(cur_offset)
    half_pos=paddle_pos+(paddle_length/2)+(cur_offset*paddle_length)
    if half_pos > ball_y and paddle_pos > 0:
        return -paddle_speed
    elif half_pos < ball_y and paddle_pos < height-paddle_length:
        return paddle_speed
    return 0

cur_speed=0
def smooth_match(ball_y,paddle_pos,paddle_length,height,paddle_speed):
    global cur_speed
    half_pos=paddle_pos+(paddle_length/2)
    if half_pos > ball_y:
        cur_speed-=1
    elif half_pos < ball_y:
        cur_speed+=1
    cur_speed*=0.9
    
    new_speed = cur_speed*paddle_speed
    
    if new_speed > paddle_speed:
        return paddle_speed
    if new_speed+paddle_length < 0 or new_speed+paddle_length+paddle_length > height:
        return 0
    return new_speed


def calculate_trajectory(impact_y,x_speed,y_speed,width,height):
    straight_pos = impact_y + width * y_speed / x_speed
    
    final_pos = abs(straight_pos) % (2 * height)
    
    if final_pos > height:
        final_pos = 2 * height - final_pos
    
    return final_pos

def move_to_collision(paddle_pos,paddle_length,paddle_speed,impact_y,x_speed,y_speed,width,height):
    trajectory=calculate_trajectory(impact_y,x_speed,y_speed,width,height)
    
    half_pos=paddle_pos+(paddle_length/2)
    difference=trajectory-half_pos
    threshold=(paddle_length/8)
    if difference < -threshold and paddle_pos > 0:
        return -paddle_speed
    elif difference > threshold and paddle_pos < height-paddle_length:
        return paddle_speed
    return 0

def cheater(paddle_pos,ball_pos):
    return 0.5*(ball_pos-paddle_pos)+(random()*2)-1