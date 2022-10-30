import sys, pygame, time

pygame.init()

size = width, height = 450, 450
color = (255,255, 255)

x_image = pygame.image.load("x.png")
o_image = pygame.image.load("o.png")
board_image = pygame.image.load("board.png")
line_image = pygame.image.load("line.png")
screen = pygame.display.set_mode(size)

player = 0
filled_boxes = 0
matrix = []


def tick():

    x = y = x_click = y_click = -1
    global player, filled_boxes

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_click, y_click = event.pos
            x, y = find_x_y(x_click, y_click)
            
            if(matrix[y][x] != -1):
                continue

            if player == 0:
                screen.blit(x_image, (x*width/3, y*height/3))
                matrix[y][x] = player
            else:
                screen.blit(o_image, (x*width/3, y*height/3))
                matrix[y][x] = player

            pygame.display.flip()

            status, line_x, line_y, angle = if_win() 
            if(status):
                if(player):
                    print(f"Player O Wins!!")
                else:
                    print(f"Player X Wins!!")
                for i in range(3):
                    for j in range(3):
                        print(matrix[i][j], end=" ")
                    print()
                print(line_x, line_y, angle)
                rotated_line_image = pygame.transform.rotate(line_image, angle)
                screen.blit(rotated_line_image, (line_x*width/3, line_y*height/3))
                pygame.display.flip()
                time.sleep(2)
                refresh()
            else:
                filled_boxes += 1
                if(player):
                    player = 0
                else:
                    player = 1
                if(filled_boxes == 9):
                    print("Game Over!!")
                    time.sleep(1)
                    refresh() 


def find_x_y(x_click, y_click):
    x = -1
    if(x_click < width/3):
        x = 0
    elif(x_click < 2*width/3):
        x = 1
    else:
        x = 2

    y = -1
    if(y_click < height/3):
        y = 0
    elif(y_click < 2*height/3):
        y = 1
    else:
        y = 2

    return(x,y)


def if_win():
    global player

    if(matrix[0][0] == player):
        if(matrix[0][1] == matrix[0][2] == player):
            return(True, 0, 0, 0)
        elif(matrix[1][0] == matrix[2][0] == player):
            return(True, 0, 0, -90)
        elif(matrix[1][1] == matrix[2][2] == player):
            return(True, 0, 0, -45)
    if(matrix[1][0] == matrix[1][1] == matrix[1][2] == player):
        return(True, 0, 1, 0)
    if(matrix[2][0] == player):
        if(matrix[2][1] == matrix[2][2] == player):
            return(True, 0, 2, 0)
        elif(matrix[1][1] == matrix[0][2] == player):
            return(True, 0, 0, 225)
    if(matrix[0][1] == matrix[1][1] == matrix[2][1] == player):
        return(True, 1, 0, -90)
    if(matrix[0][2] == matrix[1][2] == matrix[2][2] == player):
        return(True, 2, 0, -90)
            
    return(False, 0, 0, 0)


def refresh():
    global player, filled_boxes, matrix
    player = 0
    filled_boxes = 0
    matrix = []
    for i in range(3):
        temp = []
        for j in range(3):
            temp.append(-1)
        matrix.append(temp)

    screen.fill(color)
    screen.blit(board_image, (0,0))
    pygame.display.flip()


refresh()
while True:
    tick()