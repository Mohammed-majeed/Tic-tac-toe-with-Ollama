from logging import exception
import ollama
import re

grid = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}

def show_grid():
    x = "|––––-|–-–––|––-––| \n"\
         f"|  {grid[1]}  |  {grid[2]}  |  {grid[3]}  | \n"\
          "|––-––|––-––|––-––| \n"\
          f"|  {grid[4]}  |  {grid[5]}  |  {grid[6]}  | \n"\
          "|––-––|––-––|––-––| \n"\
          f"|  {grid[7]}  |  {grid[8]}  |  {grid[9]}  | \n"\
          "|––-––|––-––|––-––| \n"
    print(x)
    return x

def draw_symbol(turn_count,the_grid):
    #count turns to determine if X or O should be drawn
    if(turn_count %2 == 0):
        player_symbol = 'X'
        #update "grid" dictionary to replace entered number with player's symbol
        move = int(input(f"Player {(turn_count)%2 +1}'s turn ({player_symbol}). make your move:"))
    else:
        move = int(llama(the_grid))
        player_symbol = 'O'
        #update "grid" dictionary to replace entered number with player's symbol
        print(f"Player {(turn_count)%2 +1}'s (Ollama) played: {move}" )
        # move = int()

    if int(move) in grid.keys():
        if grid[int(move)] == 'X' or grid[int(move)] == 'O': #if number entered already marked with X or O
            raise exception
        else:
            grid[int(move)] = player_symbol
    else:  #if it wasn't an integer 1-9
        raise exception

def eval_win():
    #0 if no one has won, and 1 if someone has
    winner_found = 0
    #horizontal winning patterns
    for square in (1,4,7):
        if grid[square]==grid[square+1] ==grid[square+2]:
            winner_found = 1
    #vertical winning patterns
    for square in (1,2,3):
        if grid[square] == grid[square+3] == grid[square+6]:
            winner_found = 1
    #diagonal winning patterns
    if grid[1] == grid[5] == grid[9] or grid[3] == grid[5] == grid[7]:
        winner_found = 1
    return winner_found

def play_game():
    print("welcome to tic tac toe \nType one of the numbers on the grid to draw there")
    the_grid = None
    the_grid = show_grid()
    turn_count =0
    while turn_count <9: #repeat until grid is filled up
        if eval_win() == 0: #if no one has won,
            try: #draw a new symbol
                draw_symbol(turn_count, the_grid)
                the_grid = show_grid()
                turn_count += 1
            except: #unless player entered something invalid– prompt again
                print("Enter one of the numbers on the grid")
                continue
        if eval_win() ==0 and turn_count ==9:
            # this can't be in the same loop as above, since we need to eval_win() again
            # otherwise it calls it a tie when someone wins on last possible move:/
            print("It's a tie!")
           # break
        if eval_win() == 1: #if someone has won
            #figure out who it was
            if turn_count %2 == 1:
                print("Player 1 (X) wins!")
                break
            elif turn_count % 2 == 0:
                print("Player 2 (O) wins!")
                break

def llama(text):

    print('Ollama thinking ...')    
    llm = ollama.chat(model='llama2-uncensored', messages=[
    {
        'role': 'user',
        'content': f"""You going to play tic-tac-toe . You are the 2 player. here is the envieronment {text} 
        it is 3x3 matrix with numbers in it. you should pick one of the numbers. give me just the number ID as integer """,
    },
    ])

    

    # print(llm['message']['content'])

    # Assuming llm is your dictionary
    content = llm['message']['content']
    try:
        # Extracting numbers using regular expressions
        numbers = re.findall(r'\d+', content)

    except Exception as e:
        print("An error occurred:", e)
        numbers = None



    return numbers[0]


play_game()