import sys
import pygame
import numpy as np

pygame.init()

# Constant values
WIDTH, HEIGHT = 1000, 600
cell_size = 10
grid_width = (WIDTH) // cell_size
generations = HEIGHT // cell_size
is_running = False

def get_color(gen_nr):
    # Folosim o culoare constantă pentru toate celulele
    return 255, 255, 255  # Alb pentru celule vii

def new_generation(generation, rule_binary):
    nextgen = np.zeros_like(generation)
    for i in range(1, len(generation) - 1):
        ruleset = (generation[i - 1], generation[i], generation[i + 1])
        index = 7 - (ruleset[0] * 4 + ruleset[1] * 2 + ruleset[2] * 1)
        nextgen[i] = rule_binary[index]
    return nextgen

def display_generation(surface, gen_nr, generation, cell_size):
    for x, cell in enumerate(generation):
        color = get_color(gen_nr) if cell == 1 else (0, 0, 0)
        pygame.draw.rect(surface, color, (x * cell_size, gen_nr * cell_size, cell_size, cell_size))

def binary_of(number, bits=8):
    return [int(bit) for bit in f"{number:0{bits}b}"]

def main():
    global cell_size, grid_width, generations, is_running, rule_number

    # Cerere regula din terminal
    try:
        rule_number = int(input("Introduceti regula (0-255): "))
        if not 0 <= rule_number <= 255:
            raise ValueError
    except ValueError:
        print("Regula nu este validă. Se va folosi valoarea 30.")
        rule_number = 30

    # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wolfram's Game of Life")
    clock = pygame.time.Clock()

    # Create a separate surface for the automaton
    automaton_surface = pygame.Surface((WIDTH, HEIGHT))
    automaton_surface.fill((30, 30, 30))  # Fundalul

    # Initialize simulation variables
    gen_nr = 0
    generation = np.zeros(grid_width, dtype=int)
    generation[grid_width // 2] = 1

    # Start simulation
    is_running = True
    while True:
        screen.fill((30, 30, 30))  # Fundalul

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Functia prin care se simulează automaata
        if is_running:
            if gen_nr < generations:
                display_generation(automaton_surface, gen_nr, generation, cell_size)
                gen_nr += 1
                generation = new_generation(generation, binary_of(rule_number))
            else:
                # Închidem simularea doar când utilizatorul apasă pe "X"
                print("Simularea s-a încheiat. Apasă X pentru a închide fereastra.")
                # Continuăm să afișăm generările anterioare
                display_generation(automaton_surface, gen_nr, generation, cell_size)

        # Blit the automaton surface onto the main screen
        screen.blit(automaton_surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
