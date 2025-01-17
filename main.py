import pygame
import random
import math
pygame.init()

# Class to store constants, configurations, and data related to visualization
class DrawInformation:
    # Color constants for different visual elements
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    # Gradients for colors of the bars
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Fonts for titles and controls
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    # Padding for sides and top of the screen
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Create a window with the specified width and height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

        # Set the list to be visualized
        self.set_list(lst)

    def set_list(self, lst):
        # Store the list and calculate other visualization properties
        self.lst = lst
        self.min_val = min(lst)  # Find the minimum value in the list
        self.max_val = max(lst)  # Find the maximum value in the list

        # Calculate block width and height for bar visualization
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2  # Starting position of the first block


# Function to draw the window with current sorting state and controls
def draw(draw_info, algo_name, ascending):
    # Fill the window with the background color
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Draw the title of the sorting algorithm and its order (ascending or descending)
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    # Display controls for resetting, starting sorting, and changing sorting order
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    # Display sorting algorithm choices (Insertion Sort or Bubble Sort)
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    # Draw the list bars
    draw_list(draw_info)
    pygame.display.update()

# Function to draw the bars representing the list
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    # Clear the screen (background) if specified
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Loop through the list and draw each value as a bar
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width  # Position of the bar
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height  # Height of the bar

        color = draw_info.GRADIENTS[i % 3]  # Set gradient color for the bars

        # If there are specific positions to color, use the specified colors
        if i in color_positions:
            color = color_positions[i] 

        # Draw the rectangle representing the bar
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    # Update the display if the background was cleared
    if clear_bg:
        pygame.display.update()

# Function to generate the initial random list for sorting
def generate_starting_list(n, min_val, max_val):
    lst = []

    # Generate 'n' random numbers between 'min_val' and 'max_val'
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

# Bubble sort algorithm
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Loop through the list and compare adjacent elements
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # Swap elements if they are in the wrong order based on ascending/descending
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                # Highlight the swapped elements
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

# Insertion sort algorithm
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Loop through the list starting from the second element
    for i in range(1, len(lst)):
        current = lst[i]

        # Move the current element to the correct position in the sorted portion of the list
        while True:
            # Check if the current element should be inserted earlier in the list
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]  # Move the larger/smaller element
            i = i - 1
            lst[i] = current  # Insert the current element in its correct position

            # Highlight the moved elements
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

# Main function that controls the game loop and event handling
def main():
    run = True
    clock = pygame.time.Clock()

    # Initialize the list size and range of values
    n = 50
    min_val = 0
    max_val = 100

    # Generate the starting list and set up the visualization
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False  # Boolean to track if sorting is in progress
    ascending = True  # Boolean to track sorting order

    # Default sorting algorithm is Bubble Sort
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None  # Used to keep track of the sorting algorithm generator

    # Main game loop
    while run:
        clock.tick(60)  # Limit the frame rate to 60 FPS

        # If sorting is in progress, advance the sorting algorithm
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False  # Stop sorting when done
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # Key events for resetting, starting, and changing sorting algorithm/order
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()  # Quit Pygame when the loop ends

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
