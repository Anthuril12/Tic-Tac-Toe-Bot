import pygame
import math
import sys
import random
import time
from pygame.locals import *
tick = 1
win=pygame.display.set_mode((1000,1000))
pygame.init()
Font = pygame.font.SysFont
mouse = pygame.mouse.get_pos()




def squareDetection(mouse):

    #Erstmal 'Koordinaten' des Feldes bestimmen

    for i in range (side_length):
        if mouse[0] > (xc + i*width) and mouse[0] < xc+(((i+1)*5-1)*width/5):
            newx=i
        if mouse[1] > (yc + i*width) and mouse[1] < yc+(((i+1)*5-1)*width/5):
            newy=i

    #Zu einer Feldnummer zusammenrechnen

    try:
        feldnr=(newy-1)*side_length+newx-1
    except UnboundLocalError:
        return False

    #sofern das Feld frei ist, anwenden
    
    try:
        if board[newy][newx]==0:
            board[newy][newx]=2
            return True
    except UnboundLocalError:
        pass

def victorycheck():



    counter=0
    for i in range (side_length):
        for j in range (side_length):

            #Horizontaler victorytest    

            for k in range (triumph-1):
                if j+k+1 < side_length:
                    if board[i][j+k] == board[i][j+k+1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                    #print ("Rot hat gewonnen")
                    return float('inf')
                else:
                    #print ("Blau hat gewonnen")
                    return float('-inf')
                
            counter=0

            #Vertikaler victorytest

            for k in range (triumph-1):
                if i+k+1 < side_length:
                    if board[i+k][j] == board[i+k+1][j] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                   # print ("Rot hat gewonnen")
                    return float('inf')
                else:
                    #print ("Blau hat gewonnen")
                    return float('-inf')
            counter=0

            #Diagonal (nach rechts unten) victorytest

            for k in range (triumph-1):
                if i+k+1 < side_length and j+k+1 < side_length:
                    if board[i+k][j+k] == board[i+k+1][j+k+1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                   # print ("Rot hat gewonnen")
                    return float('inf')
                else:
                   # print ("Blau hat gewonnen")
                    return float('-inf')
            counter=0

            #Diagonal (nach links unten) victorytest

            for k in range (triumph-1):
                if i+k+1 < side_length and j-k-1 >= 0:
                    if board[i+k][j-k] == board[i+k+1][j-k-1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                   # print ("Rot hat gewonnen")
                    return float('inf')
                else:
                   # print ("Blau hat gewonnen")
                    return float('-inf')
            counter=0
    
       

    return 1


def minimax(bot,depth,alpha,beta):
    victory=victorycheck()

    if True:
        check = False
        for i in range (side_length):
            for j in range (side_length):
                if board[i][j] == 0:
                    check = True
        if check == False and abs(victory) != float('inf'):
            victory = 0
                    
    #Abbruchbedingung: Entweder depth erreicht oder einer hat gewonnen, dann wird victory, Niederlage oder Neutral ausgegeben

    if depth==0 or victory != 1:
        if victory == float('inf') or victory == float('-inf'):
            return victory
        else:
            return evaluation()


    #Zuerst die side_length für den COM: Erstmal alle möglichen Züge generieren und nacheinander durchgehen

    if bot == True:

        maxvalue=float('-inf')
        possibleMoveList=possibleMoves(0,False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])

            #Dann rekursiv herausfinden, wie gut der Move war

            value=minimax(False,depth-1,alpha,beta)

            #Ist die Abbruchbedingung oft genug erreicht, Move rückgängig doen und als neuen besten Move eintragen (oder auch nicht)

            undoMove(possibleMoveList[i])

            #Durch die Maximierung kommt hier der beste Move für den COM raus, also der schlechteste für den Spieler

            maxvalue=max(maxvalue,value)
            alpha=max(alpha,value)

            #Alpha Beta Pruning: Falls der Gegner eh was anderes doen wird, muss der COM gar nicht weiter suchen

            if True:
                if beta <= alpha:
                    break

        return maxvalue

        #So und jetzt wird die mögliche Antwort untersucht

    else:

        #Wieder Züge generieren und ausprobieren

        minvalue=float('inf')
        possibleMoveList=possibleMoves(1,False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])

            #Jetzt wieder COM Züge prüfen

            value=minimax(True,depth-1,alpha,beta)
            undoMove(possibleMoveList[i])

            #Durch die Minimierung kommt hier der schlechteste Move für COM also der beste für den Spieler raus

            minvalue=min(minvalue,value)
            beta=min(beta,value)

            #Alpha Beta Pruning: Falls der Gegner eh was anderes doen wird, muss der COM gar nicht weiter suchen

            if True:
                if beta <= alpha:
                    break

        return minvalue
    
def possibleMoves(testturn,presorting):
    moveList=[]
    victory = victorycheck()
    if victory==1:
        for i in range(side_length):
            for j in range(side_length):
                if (board[i][j]==0):
                    move=[i,j,testturn+1]
                    moveList.append(move)
    if presorting:
        return presortingPossibleMoves(moveList)
    else:
        return moveList

    #Es ist langsamer zu presorten als es nicht zu tun, schade :(

def presortingPossibleMoves(moveList):
    quality=[]
    for i in range (len(moveList)):
        evaluationMoves(moveList[i])
        quality.append(moveList[i][3])
    quality=sorted(quality, reverse=True)
    betterListedArray=[]
    for j in range (len(quality)):
        for i in range (len(moveList)):
            if quality[j] == moveList[i][3]:
                betterListedArray.append(moveList[i])
    return betterListedArray

def doMove(move):
    y=move[0]
    x=move[1]
    board[y][x]=move[2]

def undoMove(move):
    y=move[0]
    x=move[1]
    board[y][x]=0

def evaluation():
    eval=0.0
    center=(side_length-1)/2
    for i in range (side_length):
        for j in range (side_length):
            if board[i][j] == 1:

                #Je näher an der center die eigenen Steine liegen, desto besser. Die Diagonalen sind auch vorteilhaft

                eval += 1/(math.sqrt((center-i)**2 + (center-j)**2)+1)
                if i==j or side_length-1-i == j or i == side_length-1 -j:
                    eval+=0.15
            elif board[i][j] == 2:

                #Umgekehrt sind mittige und diagonale Steine des Gegners schlecht

                eval -= 1/(math.sqrt((center-i)**2 + (center-j)**2)+1)
                if i==j or side_length-1-i == j or i == side_length-1 -j:
                    eval-=0.15
    return eval

def evaluationMoves(move):
    eval = 0.0
    center=(side_length-1)/2
    if move[0]==move[1] or side_length-1-move[0] == move[1] or move[0] == side_length-1 -move[1]:
        eval+=0.15
    eval += 1/(math.sqrt((center-move[0])**2 + (center-move[1])**2)+1)
    move=move.append(eval)
    return move


def settings(mouse):
    global side_length
    global circle_position
    global circle_position_turn
    global circle_position_depth
    global requesteddepth
    global turn
    if 245 < mouse[0] < 260 and 55 < mouse[1] < 70 and side_length != 3:
        side_length = 3
        requesteddepth = 5
        circle_position = 255
        reset_board()
    if 325 < mouse[0] < 340 and 55 < mouse[1] < 70 and side_length != 5:
        side_length = 5
        requesteddepth = 3
        circle_position = 330
        reset_board()
    if 415 < mouse[0] < 430 and 55 < mouse[1] < 70 and side_length != 7:
        side_length = 7
        requesteddepth = 3
        circle_position = 420
        reset_board()
    if 505 < mouse[0] < 520 and 55 < mouse[1] < 70 and side_length != 9:
        side_length = 9
        requesteddepth = 1
        circle_position = 512.5
        reset_board()
    if 800 < mouse[0] < 850 and 55 < mouse[1] < 70:
        circle_position_turn = 830
        reset_board()
    if 860 < mouse[0] < 900 and 55 < mouse[1] < 70:
        circle_position_turn = 870
        reset_board()
    if 565 < mouse[0] < 580 and 940 < mouse[1] < 960:
        circle_position_depth = 575
        requesteddepth = 1
        reset_board()
    if 655 < mouse[0] < 670 and 930 < mouse[1] < 950:
        circle_position_depth = 665
        requesteddepth = 2
        reset_board()
    if 740 < mouse[0] < 760 and 930 < mouse[1] < 950:
        circle_position_depth = 750
        requesteddepth = 3
        reset_board()
    
def reset_board():
    global board
    global triumph
    global width
    global bestMove
    global requesteddepth
    global mouse
    triumph=round(side_length/2+1.77)
    print ("Gewinngröße:",triumph)
    width=int(800/side_length)
    board = []
    xBoard = []
    for i in range (side_length):
        for t in range (side_length):
            xBoard.append(0)
        board.append(xBoard)
        xBoard=[]
    bestMove=[]
    win.fill((30,30,30))
    drawRectangles(win, side_length, mouse, width,xc,yc)
    drawCircles(win, side_length, board, xc, yc, width)
    drawUI(win, circle_position, circle_position_turn,triumph)

def drawUI(win, circle_position, circle_position_turn, triumph):
    pygame.draw.rect(win,("white"),(250,60,265,5))
    pygame.draw.rect(win,("white"),(820,60,60,5))
        #pygame.draw.rect(win,("white"),(575,940,175,5))
    pygame.draw.circle(win,("red"), (circle_position_turn,62.5) , 10 , 50)
    pygame.draw.circle(win,("red"), (circle_position,62.5) , 10 , 50)
        #pygame.draw.circle(win,("red"), (circle_position_depth,942.5) , 10 , 50)

    Font = pygame.font.SysFont
    font1=Font("Arial",24)
    numbers = font1.render("3         5           7           9", 1, ("white"))
    textAboutSideLength = font1.render("Side Length", 1, ("white"))
    textAboutTurn = font1.render("Whose Turn first?", 1, ("white"))
    turnText = font1.render("Bot  Human", 1, ("white"))
    depthText = font1.render("How deep to search?", 1, ("white"))
    depthText_2 = font1.render("1           2          3", 1, ("white"))
    triumphmessage_1 = "You need to connect "
    triumphmessage_2 = " to win"
    triumphmessage = triumphmessage_1 + str(triumph) + triumphmessage_2
    tellVictoryText = font1.render(triumphmessage,1,("white"))

    textrect_1 = numbers.get_rect()
    textrect_2 = textAboutSideLength.get_rect()
    textrect_3 = textAboutTurn.get_rect()
    textrect_4 = turnText.get_rect()
    textrect_5 = depthText.get_rect()
    textrect_6 = depthText_2.get_rect()
    textrect_10 = tellVictoryText.get_rect()

    textrect_1.topleft = (250, 20)
    textrect_2.topleft = (100, 30)
    textrect_3.topleft = (570, 30)
    textrect_4.topleft = (800, 20)
    textrect_5.topleft = (250, 900)
    textrect_6.topleft = (570, 900)
    textrect_10.topleft = (100, 900)

    win.blit(numbers,textrect_1)
    win.blit(textAboutSideLength,textrect_2)
    win.blit(textAboutTurn,textrect_3)
    win.blit(turnText,textrect_4)
        #win.blit(depthText,textrect_5)
        #win.blit(depthText_2,textrect_6)
    win.blit(tellVictoryText,textrect_10)

def drawCircles(win, side_length, board, xc, yc, width):
    for i in range (side_length):
        for t in range (side_length):
            if board[i][t] == 1:
                pygame.draw.circle(win,("red"), (int(xc+(0.4*width)+t*width) , int(yc+(0.4*width)+i*width)) , int(width/3) , int(width/3))
            if board[i][t] == 2:
                pygame.draw.circle(win,("blue"), (int(xc+(0.4*width)+t*width) , int(yc+(0.4*width)+i*width)) ,int(width/3), int(width/3))

def drawRectangles(win, side_length, mouse, width,x,y):
    for i in range (side_length):
        for t in range (side_length):
            if x <= mouse[0] <= x+(4*width/5) and y <= mouse[1] <= y+(4*width/5):
                pygame.draw.rect(win,("white"),(x,y,4*width/5,4*width/5))
          
            else:
                pygame.draw.rect(win,("light grey"),(x,y,4*width/5,4*width/5))
            x+=width
        x-=side_length*width
        y+=width

# Render the objects

#side_lengthnlänge, Gewinnlänge und Position des Spielbretts einstellen
if True:    
    hit=False
    feldnr = 0
    side_length=3
    circle_position = 255
    circle_position_turn = 830
    circle_position_depth = 750
    turn=-1
    board=[]
    requesteddepth=5
    presortingInitialMoves=False

    xc=100
    yc=100

    reset_board()


    bot=False
    presorting=False

run = True








while run:
    pygame.time.delay(tick)
    mouse = pygame.mouse.get_pos()
    win.fill((30,30,30))

    

    #Spielbrettquadrate zeichnen
    drawRectangles(win, side_length, mouse, width,xc,yc)

    #bereits gesetzte Kreise zeichnen
    
    drawCircles(win, side_length, board, xc, yc, width)

    
    #Slider zeichnen
    drawUI(win, circle_position, circle_position_turn, triumph)
    
    #Spielende
    
    if True:
        if turn==float('inf'):
            Font = pygame.font.SysFont
            font1=Font("Arial",250)
            redWins = font1.render("You lost", 1, ((200,50,50)))
            textrect_7 = redWins.get_rect()
            textrect_7.topleft = (25, 300)
            win.blit(redWins,textrect_7)
        if turn==float('-inf'):
            Font = pygame.font.SysFont
            font1=Font("Arial",250)
            blueWins = font1.render("You won", 1, ((100,0,255)))
            textrect_8 = blueWins.get_rect()
            textrect_8.topleft = (25, 300)
            win.blit(blueWins,textrect_8)

        if True:
            check = False
            for i in range (side_length):
                for j in range (side_length):
                    if board[i][j] == 0:
                        check = True
            if check == False and abs(turn) != float('inf'):
                Font = pygame.font.SysFont
                font1=Font("Arial",125)
                noWins = font1.render("Draw. No Winner", 1, ("white"))
                textrect_9 = noWins.get_rect()
                textrect_9.topleft = (25, 300)
                win.blit(noWins,textrect_9)

    #Mausklick aktiviert die Funktion 'squareDetection'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and turn == -1:
            hit=squareDetection(mouse)
            if hit:
                turn = victorycheck()
        if event.type == pygame.MOUSEBUTTONDOWN and (900 < mouse[1] or mouse[1] < 100) :
            settings(mouse)

    

            
    if True:
        check_turn = 0
        for i in range (side_length):
            for j in range (side_length):
                if board[i][j] != 0:
                    check_turn += 1
        if check_turn < 1:
            if circle_position_turn == 830:
                turn = 1
            else:
                turn = -1
    

    #COM ist turn

    if turn==1:

        #letzten Move abspeichern, Zeit messen, beste Situation auf minus unendlich setzten
        
        savedMove=bestMove
        zeitVorher=time.time()

        font1=Font("Arial",24)
        redWins = font1.render("Computing Move...", 1, ((200,50,50)))
        textrect_7 = redWins.get_rect()
        textrect_7.topleft = (500, 900)
        win.blit(redWins,textrect_7)
        pygame.display.update()
        bestSituation=float('-inf')
        check = 0
        for i in range (side_length):
            for j in range (side_length):
                if board[i][j] != 0:
                    check += 1
        print("Check:",check)
        if check > 0:
            

            #Mögliche Züge generieren, diese einem ersten Qualitäts-Check unterziehen und nach wahrscheinlicher Qualität sortieren

            betterListedArray = possibleMoves(0,presortingInitialMoves)


            #Move für Move Situation von minimax-Funktion einschätzen lassen, alpha wird dabei übertragen

            for i in range (len(betterListedArray)):
                doMove(betterListedArray[i])
                situation = minimax(False,requesteddepth,bestSituation,float('inf'))
                print("So gut siehts gerade aus:",situation)
                undoMove(betterListedArray[i])
                if situation > bestSituation:
                    bestSituation=situation
                    bestMove=betterListedArray[i]

            #Wenn kein Move besser war als verlieren, dann muss dem Gegner gratuliert werden
            check_turn = 0
            if bestMove==savedMove and len(betterListedArray) != 0:
                check_turn = float('-inf')
        else:
            center=int((side_length-1)/2)
            bestMove=[center,center,1]
        #Move doen, Zeit stoppen und victorycheck
        doMove(bestMove)
        zeitNachher=time.time()
        print ("Mega smarter AI Move",bestMove,"in ",zeitNachher-zeitVorher,"Sekunden")

        #Nur falls irgendwas schiefgeht, ein ZufallsMove

        if False:
            while True:
                yBot=random.randint(0,side_length-1)
                xBot=random.randint(0,side_length-1)
 
                if board[yBot][xBot]==0:
                    break
            board[yBot][xBot]=1

        turn=victorycheck()*-1
        if turn == float('-inf') or turn == float('-inf'):
            turn = turn * -1
        print ("Gewinngröße:",triumph)
        if check_turn == float('-inf'):
            turn = check_turn
    pygame.display.update()