import pygame
from sudoku import Sudoku
import copy


pygame.init()

# ****************************** VARIABLES ******************************

win = pygame.display.set_mode( (500, 530) ) 
pygame.display.set_caption( "Sudoku" ) 
win.fill( (255, 255, 255) )
pygame.display.update()


sqr_ini = 25                         
sqr_ini = 25                          
sqr_len = 50                        
def_box_loc = []                    
is_selected = False 
col_box_w = ( 249, 72, 72 )        
col_box_c = ( 117, 235, 117 )       

col_fn_sel = ( 82, 82, 82 )        
col_fn_ent = ( 0, 0, 0 )           
col_fn_def = ( 51, 31, 151 )      

font_def = pygame.font.SysFont( "Comic Sans MS", 25 ) 
font_ent = pygame.font.SysFont( "Comic Sans MS", 17 )


# ****************************** PYGAME FUNCTIONS ****************************** 

def drawGrid():
    for i in range( 10 ):       
        for j in range( 10 ):
            width_h = 2         
            width_v = 2

            if( i % 3 == 0 ): 
                width_h = 3

            if( j % 3 == 0 ): 
                width_v = 3

            pygame.draw.line( win, ( 0, 0, 0 ), ( sqr_ini + (sqr_len * j), sqr_ini ), 
            ( sqr_ini + (sqr_len * j), sqr_ini + sqr_len * 9 ), width_v )

            pygame.draw.line( win, ( 0, 0, 0 ), ( sqr_ini, sqr_ini + (sqr_len * i) ), 
            ( sqr_ini + sqr_len * 9, sqr_ini + (sqr_len * i) ), width_h )

    pygame.display.update()


def generate():    
    grid = Sudoku(3).difficulty(0.5).board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == None:
                grid[i][j] = 0
    grid_solved = copy.deepcopy(grid)
    return [ grid, grid_solved ]


def drawSudoku( grid ):
    win.fill( (255, 255, 255) )
    drawGrid()

    for i in range( len( grid[0] ) ):       
        for j in range( len( grid[0] ) ):  
            pygame.time.delay( 3 )

            if grid[i][j] == 0: 
                value = font_def.render('', True, col_fn_def)   
            else: 
               value = font_def.render( str(grid[i][j]), True, col_fn_def )   
               def_box_loc.append( (sqr_ini + (i * sqr_len) , sqr_ini + (j * sqr_len))  )

            win.blit( value, ( 17 + sqr_ini + (j * sqr_len), 7 + sqr_ini + (i * sqr_len) ) ) 

            pygame.display.update() 


def locateRect( pos ):
    for i in range ( 9 ):      
        for j in range( 9 ):    
            if ( pos[0] > (sqr_ini + sqr_len * j) and           
            pos[0] < (sqr_ini + sqr_len + (sqr_len * j)) and 
            pos[1] > (sqr_ini + sqr_len * i) and 
            pos[1] < (sqr_ini + sqr_len + (sqr_len * i)) ):
                
                return (sqr_ini + sqr_len * i, sqr_ini + sqr_len * j)
  

def insertBubble( value, pos, brd ):
    if pos not in def_box_loc:
        brd[int((pos[0] - sqr_ini) / sqr_len)][int((pos[1] - sqr_ini) / sqr_len)] = value
    
        pygame.draw.rect( win, ( 255, 255, 255 ), ( pos[1] + 2, pos[0] + 2, sqr_len - 3, sqr_len - 3 ) )
    
        value = font_ent.render( str( value ), True, col_fn_sel )
        win.blit( value, ( pos[1] + 10, pos[0] + 7 ) )
    
        pygame.display.update()
        

def drawSelBox( pos, con ):
    if con == "sel":
        color = col_box_w
    if con == "cor":
        color = col_box_c

    pygame.draw.lines( win, color, True, [ (pos[1], pos[0]), (pos[1] + sqr_len, pos[0]), 
                     (pos[1] + sqr_len, pos[0] + sqr_len),  (pos[1], pos[0] + sqr_len) ], 2 ) 
    
    pygame.display.update() 


def insertFinal( pos, brd ): 
    print("Hello")
    row = int( (pos[0] - sqr_ini) / sqr_len )
    col = int( (pos[1] - sqr_ini) / sqr_len )

    if pos not in def_box_loc:
        if brd[0][row][col] == brd[1][row][col]:
            drawSelBox( pos, "cor" )  

            pygame.draw.rect( win, ( 255, 255, 255 ), ( pos[1] + 2, pos[0] + 2, sqr_len - 3, sqr_len - 3 ) )

            value = font_def.render( str( brd[0][row][col] ), True, col_fn_ent )
            win.blit( value, ( pos[1] + 17, pos[0] + 7 ) )

            pygame.display.update()

            def_box_loc.append( (pos[0], pos[1]) )

        else:
            brd[0][row][col] = 0

            pygame.draw.rect( win, ( 255, 255, 255 ), ( pos[1] + 2, pos[0] + 2, sqr_len - 3, sqr_len - 3 ) )
            pygame.display.update()


# ****************************** SOLVER FUNCTIONS ********************************

def find_empty( brd ):
    for i in range( len( brd ) ):
        for j in range( len( brd[0] ) ):
            if ( brd[i][j] == 0 ):
                return (i, j)   # row, column

    return None


def valid( brd, num, pos ):
    # Rows
    for i in range( len( brd[0] ) ):
        if ( brd[pos[0]][ i ] == num and pos[1] != i ):
            return False

    # Columns
    for i in range( len( brd ) ):
         if ( brd[ i ][ pos[1] ] == num and pos[0] != i ):
            return False

    # Box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range( box_y *3, box_y *3 + 3 ):
        for j in range( box_x *3, box_x *3 + 3 ):
            if( brd[ i ][ j ] == num and ( i, j ) != pos ):
                return False

    return True

def solve( brd ):
    find = find_empty( brd )
    if not find:
        return True
    else:
        row, col = find

    for i in range( 1, 10 ):
        if valid( brd, i, ( row, col ) ):
            brd[row][col] = i

            if solve( brd ):
                return True

            brd[row][col] = 0

    return False


def solveGUI( brd ):
    find = find_empty( brd )
    if not find:
        return True
    else:
        row, col = find
        
        drawSelBox( (sqr_ini + (sqr_len * row), sqr_ini + (sqr_len * col)), 'sel' )
        pygame.display.update()

    for i in range( 1, 10 ):
        pygame.time.delay( 5 )

        pygame.draw.rect( win, ( 255, 255, 255 ), ( sqr_ini + (sqr_len * col) + 2, sqr_ini + (sqr_len * row) + 2, sqr_len - 3, sqr_len - 3 ) )
        value = font_def.render( str( i ), True, col_fn_ent )
        win.blit( value, ( sqr_ini + (sqr_len * col) + 17, sqr_ini + (sqr_len * row) + 7 ) )
        pygame.display.update()

        if valid( brd, i, ( row, col ) ):
            brd[row][col] = i

            pygame.draw.rect( win, ( 255, 255, 255 ), ( sqr_ini + (sqr_len * col) + 2, sqr_ini + (sqr_len * row) + 2, sqr_len - 3, sqr_len - 3 ) )
            value = font_def.render( str( brd[row][col] ), True, col_fn_ent )
            win.blit( value, ( sqr_ini + (sqr_len * col) + 17, sqr_ini + (sqr_len * row) + 7 ) )
            pygame.display.update()

            if solveGUI( brd ):
                return True

            brd[row][col] = 0            
            

    return False


# ****************************** PYGAME MAIN LOOP ******************************

drawGrid()
board = generate()
drawSudoku( board[0] )
solve( board[1] )


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:            
            run = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:              
                pos = pygame.mouse.get_pos()   
                
                if not ( pos[0] < sqr_ini or pos[0] > sqr_ini + sqr_len* 9 or pos[1] < sqr_ini or pos[1] > sqr_ini + sqr_len* 9):
                    is_selected = True
                    drawGrid()
                    drawSelBox( locateRect( pos ), "sel" )
                    solve( board[1] )


        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_n: 
                board = generate()  
                drawSudoku( board[0] )      

            if event.key == pygame.K_SPACE:
                solveGUI( board[0] )
                is_selected = False
                drawGrid()    

            if is_selected:
                if event.type == pygame.KEYDOWN:
                    rec_pos = locateRect( pos )
                    if event.key == pygame.K_RETURN:
                        insertFinal( rec_pos, board )
                        
                    if 0 < event.key - 48 < 10:
                        value = event.key - 48
                        insertBubble( value, rec_pos, board[0] )
                    
                    
                    is_selected = False
            
pygame.quit()