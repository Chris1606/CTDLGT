import pygame

import random


pygame.init()

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)
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
def update_game_screen(window):
    window.fill((0, 0, 0))
    show_grid_on_screen(window, CELLSIZE, pGameGrid, cGameGrid)
    for ship in ships:
        ship.draw()
    pygame.display.update()

# Game Initialization
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ROWS = 10
COLS = 10
CELLSIZE = 40
GAME_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

print_game_logic()

# Run game loop
# Run game loop
RUN_GAME = True
selected_ship = None

while RUN_GAME:
    for event in pygame.event.get():
        # Save the logical grids (pGameLogic and cGameLogic)
        save_grid_to_file("player.txt", pGameLogic)
        save_grid_to_file("computer.txt", cGameLogic)

        if event.type == pygame.QUIT:
            RUN_GAME = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for ship in ships:
                if ship.is_hovered(mouse_pos):
                    selected_ship = ship
                    ship.is_dragging = True
                    break
            if event.button == 3:  # Right click to toggle orientation
                if selected_ship:
                    selected_ship.toggle_orientation()

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_ship:
                selected_ship.is_dragging = False
                # Snap ship to grid and update game logic
                snap_ship_to_grid(selected_ship, pGameGrid, CELLSIZE, pGameLogic)
                save_ships_to_file('player.txt', ships)
                selected_ship = None

    if selected_ship and selected_ship.is_dragging:
        # Update ship's position to follow the mouse
        mouse_pos = pygame.mouse.get_pos()
        selected_ship.x = mouse_pos[0] - CELLSIZE // 2
        selected_ship.y = mouse_pos[1] - CELLSIZE // 2

    # Update the game screen
    update_game_screen(GAME_SCREEN)

pygame.quit()

