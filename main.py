import pygame

import random


pygame.init()

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

FPS = 50
clock = pygame.time.Clock()


BLUE =  (0, 0, 255)
RED =   (255, 0, 0)
# Save Game
def save_grid_to_file(file_name, grid):
    """Saves the grid to a file, representing empty cells as '*' and ships as 'S'."""
    with open(file_name, 'w') as file:
        for row in grid:
            row_symbols = ['S' if cell == 'S' else '*' for cell in row]  # Use 'S' for ships, '*' for empty cells
            file.write(" ".join(row_symbols) + "\n")

def save_ships_to_file(file_name, ships):
    """Saves ships' grid positions and orientations to a file."""
    with open(file_name, 'w') as file:
        for ship in ships:
            orientation = "H" if ship.is_vertical else "V"
            file.write(f"Ship: Length={ship.length}, Row={ship.grid_row}, Col={ship.grid_col}, Orientation={orientation}\n")

# Game Utility Functions
def create_game_grid(rows, cols, cellsize, pos):
    startX = pos[0]
    startY = pos[1]
    coordGrid = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append((startX, startY))
            startX += cellsize
        coordGrid.append(rowX)
        startX = pos[0]
        startY += cellsize
    return coordGrid

def update_game_logic(rows, cols):
    gameLogic = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append(' ')  # Initialize with empty cells
        gameLogic.append(rowX)
    return gameLogic

def show_grid_on_screen(window, cellsize, playerGrid, computerGrid):
    gameGrids = [playerGrid, computerGrid]
    for grid in gameGrids:
        for row in grid:
            for col in row:
                pygame.draw.rect(window, (255, 255, 255), (col[0], col[1], cellsize, cellsize), 1)

def get_clicked_tile(mouse_pos, grid, cellsize):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x, y = grid[row][col]
            if x < mouse_pos[0] < x + cellsize and y < mouse_pos[1] < y + cellsize:
                print(f"{row} & {col} is clicked ")
                return row, col
                
    return None, None 

   
#not yet implementing 
def display_message(window, message, position):
    """Displays a message on the game window."""
    text_surface = FONT.render(message, True, (255, 0, 0))  # Red color
    window.blit(text_surface, position)

#player fucntion
def clear_previous_position(ship, game_logic):
    """Clears the previous position of the ship from the game logic grid."""
    if ship.grid_row is not None and ship.grid_col is not None:
        if ship.is_vertical:
            for i in range(ship.length):
                game_logic[ship.grid_row + i][ship.grid_col] = '*'  # Clear vertical cells
        else:
            for i in range(ship.length):
                game_logic[ship.grid_row][ship.grid_col + i] = '*'  # Clear horizontal cells

def is_overlapping(ship, row, col, game_logic):
    """Checks if placing the ship at the given row and col will overlap with another ship."""
    if ship.is_vertical:
        # Check vertical overlap
        for i in range(ship.length):
            if row + i >= len(game_logic) or game_logic[row + i][col] == 'S':
                return True  # Overlap detected
    else:
        # Check horizontal overlap
        for i in range(ship.length):
            if col + i >= len(game_logic[0]) or game_logic[row][col + i] == 'S':
                return True  # Overlap detected
    return False  # No overlap

def snap_ship_to_grid(ship, grid, cellsize, game_logic):
    """Snaps the ship to the nearest grid cell, clears its previous position, and updates the game logic.
       Also prevents ship overlap."""
    # Clear previous position
    clear_previous_position(ship, game_logic)

    # Get the new position
    row, col = get_clicked_tile((ship.x, ship.y), grid, cellsize)

    if row is not None and col is not None:
        # Check if the ship fits and doesn't overlap with other ships
        if ship.is_vertical:
            if row + ship.length <= len(grid) and not is_overlapping(ship, row, col, game_logic):
                # Update ship position
                ship.x, ship.y = grid[row][col]
                ship.grid_row = row
                ship.grid_col = col
                # Mark the game logic grid with 'S'
                for i in range(ship.length):
                    game_logic[row + i][col] = 'S'
            else:
                display_message(GAME_SCREEN, "Overlap detected or out of bounds (horizontal).", (600, 600))
                print("Overlap detected or out of bounds (vertical).")
        else:
            if col + ship.length <= len(grid[0]) and not is_overlapping(ship, row, col, game_logic):
                # Update ship position
                ship.x, ship.y = grid[row][col]
                ship.grid_row = row
                ship.grid_col = col
                # Mark the game logic grid with 'S'
                for i in range(ship.length):
                    game_logic[row][col + i] = 'S'
            else:
                print("Overlap detected or out of bounds (horizontal).")

def player_attack(mouse_pos, grid, game_logic, file_name):
    """Handles the attack by checking the clicked tile, updating the game logic, and saving the result."""
    row, col = get_clicked_tile(mouse_pos, grid, CELLSIZE)

    if row is not None and col is not None:
        if game_logic[row][col] in ['H', 'M']:
            #print(f"The tile {row}, {col} is shoot before")
            return False
            
        if game_logic[row][col] == 'S':
            print(f"Hit at {row}, {col}")
            game_logic[row][col] = 'H'  
            gunshot.play()
            #fill_tile(GAME_SCREEN, row, col, RED, grid, CELLSIZE)
        else:
            print(f"Miss at {row}, {col}")
            game_logic[row][col] = 'M'
            splash.play()
            #fill_tile(GAME_SCREEN, row, col, BLUE, grid, CELLSIZE)

    with open(file_name, 'w') as file:
        for logic_row in game_logic:
            row_symbols = [cell if cell in ['S', 'H', 'M'] else '*' for cell in logic_row]
            file.write("".join(row_symbols) + "\n")  

def player_win(file_name):
    with open(file_name, 'r') as file:
        file_grid = [list(line.strip()) for line in file.readlines()]

    for row in file_grid:
        if 'S' in row:  # If there is still a ship, player has not won yet
            return False
            
    return True  # All ships have been hit, player wins!


            
    



#computer function 
def randomly_place_ship(ship, grid, game_logic):
    placed = False
    while not placed:
        # Randomly choose orientation (0 for horizontal, 1 for vertical)
        ship.is_vertical = bool(random.randint(0, 1))

        if ship.is_vertical:
            # Choose a random starting row and column for vertical placement
            row = random.randint(0, len(grid) - ship.length)
            col = random.randint(0, len(grid[0]) - 1)
        else:
            # Choose a random starting row and column for horizontal placement
            row = random.randint(0, len(grid) - 1)
            col = random.randint(0, len(grid[0]) - ship.length)

        # Check if the ship can be placed without overlapping
        if not is_overlapping(ship, row, col, game_logic):
            # Place the ship in the grid and update the game logic
            ship.grid_row = row
            ship.grid_col = col
            if ship.is_vertical:
                for i in range(ship.length):
                    game_logic[row + i][col] = 'S'
            else:
                for i in range(ship.length):
                    game_logic[row][col + i] = 'S'
            placed = True

def place_and_save_computer_ships(ships, grid, game_logic):
    for ship in ships:
        randomly_place_ship(ship, grid, game_logic)
    save_ships_to_file('computer.txt', ships)

def computer_attack(game_logic, file_name, attack_position):
    
    while True: 
        row = random.randint(0, len(game_logic) - 1)
        col = random.randint(0, len(game_logic) - 1)
         
        if (row, col) not in attack_position: 
            attack_position.add((row, col))
            break

    if row is not None and col is not None:
        
        if game_logic[row][col] == 'S':
            print(f"Hit at {row}, {col}")
            game_logic[row][col] = 'H'
            gunshot.play()

        else:
            print(f"Miss at {row}, {col}")
            game_logic[row][col] = 'M' 
            splash.play()

    with open(file_name, 'w') as file:
        for logic_row in game_logic:
            row_symbols = [cell if cell in ['S', 'H', 'M'] else '*' for cell in logic_row]
            file.write("".join(row_symbols) + "\n")  
        
def computer_win(file_name):
    with open(file_name, 'r') as file: 
        file_grid = [list(line.strip()) for line in file.readlines()]

    for row in file_grid:
        if 'S' in row: 
            return False
    return True
#game logic
def print_game_logic():
    print('Player Grid'.center(50, '#'))
    for row in pGameLogic:
        row_symbols = ['S' if cell == 'S' else '*' for cell in row]
        print(" ".join(row_symbols))
    print('Computer Grid:'.center(50, '#'))
    for row in cGameLogic:
        row_symbols = ['S' if cell == 'S' else '*' for cell in row]
        print(" ".join(row_symbols))

# Ship Class
class Ship:
    def __init__(self, image, length, x, y):
        self.image = image
        self.length = length
        self.x = x
        self.y = y
        self.is_vertical = True
        self.is_dragging = False
        self.grid_row = None
        self.grid_col = None

    def draw(self):
        if self.is_vertical:
            GAME_SCREEN.blit(self.image, (self.x, self.y))
        else:
            rotated_image = pygame.transform.rotate(self.image, 90)
            GAME_SCREEN.blit(rotated_image, (self.x, self.y))

    def toggle_orientation(self):
        self.is_vertical = not self.is_vertical

    def is_hovered(self, mouse_pos):
        if self.is_vertical:
            ship_rect = pygame.Rect(self.x, self.y, CELLSIZE , CELLSIZE * self.length)
        else:
            rotated_image = pygame.transform.rotate(self.image, 90)
            ship_rect = pygame.Rect(self.x, self.y, rotated_image.get_width(), rotated_image.get_height())
        return ship_rect.collidepoint(mouse_pos)

# Update the screen
def fill_tile(screen, row, col, color, grid, CELLSIZE):
    """Fills a specific tile on the grid with a given color."""
    x, y = grid[row][col]  # Get the top-left corner coordinates of the tile from the grid
    rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)  # Create the rectangle object
    pygame.draw.rect(screen, color, rect)  # Draw the filled rectangle
    pygame.display.update()  # Update the screen to reflect changes

def dispaly_winner_message(message):
    text = FONT.render(message, True, RED)
    text_rect = text.get_rect(center = (SCREEN_HEIGHT/ 2, SCREEN_WIDTH / 2))
    GAME_SCREEN.blit(text, text_rect)
    pygame.display.flip()


def update_game_screen(window):
    # Instead of filling the entire window, we can selectively redraw elements
    window.fill((0,0,0))
    # Draw the grids (assuming they stay consistent)
    show_grid_on_screen(window, CELLSIZE, pGameGrid, cGameGrid)  # Draw the grids first
    
    # Draw the ships on the player grid
    for ship in ships:
        ship.draw()

    # Only draw the tiles where hits or misses occurred
    for row in range(ROWS):
        for col in range(COLS):
            if pGameLogic[row][col] == 'H':  # Hit
                fill_tile(window, row, col, RED, pGameGrid, CELLSIZE)
            elif pGameLogic[row][col] == 'M':  # Miss
                fill_tile(window, row, col, BLUE, pGameGrid, CELLSIZE)
            
            if cGameLogic[row][col] == 'H':  # Hit on computer side
                fill_tile(window, row, col, RED, cGameGrid, CELLSIZE)
            elif cGameLogic[row][col] == 'M':  # Miss on computer side
                fill_tile(window, row, col, BLUE, cGameGrid, CELLSIZE)

    # Finally, update only the changed areas or the whole display if needed
    pygame.display.update()  # You can pass specific rects if you want partial updates



# Game Initialization
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ROWS = 10
COLS = 10
CELLSIZE = 40
GAME_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Battle Ship")

# Initialize grids
pGameGrid = create_game_grid(ROWS, COLS, CELLSIZE, (50, 50))
pGameLogic = update_game_logic(ROWS, COLS)
cGameGrid = create_game_grid(ROWS, COLS, CELLSIZE, (50 + (COLS * CELLSIZE) + 50, 50))
cGameLogic = update_game_logic(ROWS, COLS)

# Load ships
battleship_img = pygame.image.load('assets/images/ships/battleship/battleship.png')
carrier_img = pygame.image.load('assets/images/ships/carrier/carrier.png')
cruiser_img = pygame.image.load('assets/images/ships/cruiser/cruiser.png')
destroyer_img = pygame.image.load('assets/images/ships/destroyer/destroyer.png')
patrol_boat_img = pygame.image.load('assets/images/ships/patrol boat/patrol boat.png')

# Resize ship images
battleship_img = pygame.transform.scale(battleship_img, (CELLSIZE, CELLSIZE * 5))
carrier_img = pygame.transform.scale(carrier_img, (CELLSIZE, CELLSIZE * 4))
cruiser_img = pygame.transform.scale(cruiser_img, (CELLSIZE, CELLSIZE * 3))
destroyer_img = pygame.transform.scale(destroyer_img, (CELLSIZE, CELLSIZE * 3))
patrol_boat_img = pygame.transform.scale(patrol_boat_img, (CELLSIZE, CELLSIZE * 2))

# Create ship objects
battleship = Ship(battleship_img, 5, 50, 500)
carrier = Ship(carrier_img, 4, 150, 500)
cruiser = Ship(cruiser_img, 3, 250, 500)
destroyer = Ship(destroyer_img, 3, 350, 500)
patrol_boat = Ship(patrol_boat_img, 2, 450, 500)
ships = [battleship, carrier, cruiser, destroyer, patrol_boat]


# Load sounds

explosion = pygame.mixer.Sound('assets/sounds/explosion.wav')
gunshot = pygame.mixer.Sound('assets/sounds/gunshot.wav')
splash = pygame.mixer.Sound('assets/sounds/splash.wav')

print_game_logic()

computer_ships = [Ship(battleship_img, 5, 0, 0),
                  Ship(carrier_img, 4, 0, 0),
                  Ship(cruiser_img, 3, 0, 0),
                  Ship(destroyer_img, 3, 0, 0),
                  Ship(patrol_boat_img, 2, 0, 0)]
# Run game loop
# Run game loop
RUN_GAME = True
selected_ship = None

place_and_save_computer_ships(computer_ships, cGameGrid, cGameLogic)

#Store attacked position of computer
attack_position = set()


COMPUTER_DELAY = 500  # 2 seconds delay
computer_attack_time = None 
player_turn = True
while RUN_GAME:
    # Event loop
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            RUN_GAME = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for ship in ships:
                if ship.is_hovered(mouse_pos):
                    selected_ship = ship
                    ship.is_dragging = True
                    break
            if event.button == 3 and selected_ship:  # Right-click to toggle orientation
                selected_ship.toggle_orientation()

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_ship:
                selected_ship.is_dragging = False
                snap_ship_to_grid(selected_ship, pGameGrid, CELLSIZE, pGameLogic)
                save_ships_to_file('player.txt', ships)  # Save ships after placement
                save_grid_to_file("player.txt", pGameLogic)  # Save grid after update
                selected_ship = None
            elif player_turn:
                mouse_pos = pygame.mouse.get_pos()
                player_attack(mouse_pos, cGameGrid, cGameLogic, 'computer.txt')  # Player attacks
                save_grid_to_file("computer.txt", cGameLogic)  # Save the updated computer grid
                
                if player_win('computer.txt') == True: 
                    print("Player Win")
                    dispaly_winner_message("PLAYER WIN")
                    pygame.time.delay(5000)
                player_turn = False  # End player's turn, switch to computer's turn
                computer_attack_time = pygame.time.get_ticks()


    # Computer's turn logic
    if not player_turn and computer_attack_time:
        current_time = pygame.time.get_ticks()
        if current_time - computer_attack_time >= COMPUTER_DELAY:  # Check if delay has passed
            computer_attack(pGameLogic, 'player.txt', attack_position)  # Computer attacks
            save_grid_to_file("player.txt", pGameLogic)  # Save the updated player grid

            if player_win('player.txt') == True: 
                print("Computer Win")
                           

            player_turn = True  # Switch back to player's turn
            computer_attack_time = None  # Reset the timer

    # Dragging the ship with the mouse
    if selected_ship and selected_ship.is_dragging:
        mouse_pos = pygame.mouse.get_pos()
        selected_ship.x = mouse_pos[0] - CELLSIZE // 2
        selected_ship.y = mouse_pos[1] - CELLSIZE // 2

    # Redraw the game screen
    update_game_screen(GAME_SCREEN)
    
    # Limit frame rate
    clock.tick(FPS)

pygame.quit()

