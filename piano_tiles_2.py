import numpy as np
import mss
import pyautogui
import cv2
import mouse

sct = mss.mss()


def mouse_coor(A, delta_d, mouse_height):
    #In progress- creating bounding box by with mouse
    result1 = []
    result2 = []
    for i in range(0,4):
        result1.append([A[0] + int(delta_d/2) + i * delta_d, A[1] + mouse_height])
        result2.append([int(delta_d / 2) + i * delta_d, mouse_height])
    return result1, result2


def check_pixel(img, pixel_points, mouse_points):
    """Searching and returning black piano key coordinate"""
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if img[pixel_points[0][1],pixel_points[0][0]] < 10:
        return mouse_points[0]
    elif img[pixel_points[1][1],pixel_points[1][0]] < 10:
        return mouse_points[1]
    elif img[pixel_points[2][1],pixel_points[2][0]] < 10:
        return mouse_points[2]
    elif img[pixel_points[3][1],pixel_points[3][0]] < 10:
        return mouse_points[3]
    else:
        return [15,646]


def mouse_movement(coor, prev_coor, score):
    """Moves mouse to loation from coor and clicks"""
    additional_step = 0
    score_step = 60
    if score == score_step:
        additional_step += int(score_step/10) + 10
        score_step += 70
        print(score_step, additional_step)
    if coor[0] != prev_coor[0]:
        pyautogui.click(x=coor[0], y=coor[1] + additional_step)
        score += 1
    else:
        pass


def engage():
    """Prints 'CLICK!!!' to signal algorythm is ready"""
    print("CLICK!!!")
    while True:
        if mouse.is_pressed(mouse.LEFT):
            break


if __name__ == "__main__":
    # bbox starf-finish points, [from left, from top]
    A = [15, 430]
    B = [471, 460]

    score = 0 #score counter, controls game speed

    width = abs(A[0]-B[0])
    height = abs(A[1]-B[1])
    delta_d = int(width/4) # width of one piano line
    mouse_height = int(height/2) # half height of the bounding box

    # bounding box for grab screenshot
    bbox = {"top": A[1], "left": A[0], "width": width, "height": height}

    prev_coor = [0,0]

    mouse_points, pixel_points = mouse_coor(A, delta_d, mouse_height)

    engage() # waits for the "START" click

    while True:
        img = np.array(sct.grab(monitor= bbox))

        coor = check_pixel(img,pixel_points,mouse_points)

        mouse_movement(coor, prev_coor, score)

        prev_coor = coor

        if cv2.waitKey(10) == ord('q'):
            break
