import pygame
from easygui import multenterbox
from collections import namedtuple
import matplotlib.pyplot as plt

from rumor_spreading_simulator.engine.person import SkepticismLevel
from rumor_spreading_simulator.engine.simulator import RumorSpreadingSimulator


# GUI Consts
WINDOW_HEIGHT = 950
WINDOW_WIDTH = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (128, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)

UserParams = namedtuple(
    "UserParams",
    [
        "world_size",
        "population_density",
        "rumor_cool_down",
        "skepticism_dist",
        "rate",
        "rounds"
    ]
)


def parse_user_params(user_params):
    skepticism_dist_list = [float(prob) for prob in user_params.skepticism_dist.split(" ")]
    return UserParams(
        world_size=int(user_params.world_size),
        population_density=float(user_params.population_density),
        rumor_cool_down=int(user_params.rumor_cool_down),
        skepticism_dist=dict(zip(SkepticismLevel, skepticism_dist_list)),
        rate=float(user_params.rate),
        rounds=int(user_params.rounds)
    )


def receive_user_params():
    RumorSpreadingSimulator()
    window_title = "Rumor Spreading Simulator"
    message_to_user = "Please choose simulator execution parameters"
    user_params_desc = [
        "World Size (MxM)",
        "Population Density (0-1)",
        "Rumor Cool Down Generations",
        "Skepticism Distribution (S1 S2 S3 S4)",
        "Simulator Generations Rate (seconds)",
        "Simulator Generations Rounds"
    ]
    user_default_params = ["100", "0.8", "5", "0.25 0.25 0.25 0.25", "0.2", "150"]

    user_params = multenterbox(message_to_user, window_title, user_params_desc, user_default_params)
    return parse_user_params(UserParams(*user_params))


def simulation_loop(simulator, rate, rounds):
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    large_font = pygame.font.SysFont('arialblack', 35)
    small_font = pygame.font.SysFont('arialblack', 10)
    clock = pygame.time.Clock()

    should_run = True
    for _ in range(rounds):
        if not should_run:
            break
        clock.tick(1/rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False

        # rendering the screen with white color
        pygame.draw.rect(win, WHITE, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        generation_number_txt = large_font.render(f"Generation Number: {simulator.generation}", 1, (100, 100, 100))
        win.blit(generation_number_txt, ((WINDOW_WIDTH - generation_number_txt.get_width()) // 2, 0))

        different = 40
        x = 100
        # blit legend to the window
        for text, color in [("S1", GREEN), ("S2", YELLOW), ("S3", ORANGE), ("S4", RED), ("RUMOR", BLACK)]:
            text_box = large_font.render(text, 1, color)
            win.blit(text_box, (x + different, 50))
            x += different + text_box.get_width()

        parameters = f"Rumor Count: {simulator.rumor_count}, Rumor Relative: {simulator.rumor_relative}"
        parameters_text = small_font.render(parameters, 1, (100, 100, 100))
        win.blit(parameters_text, ((WINDOW_WIDTH - parameters_text.get_width()) // 2, WINDOW_HEIGHT - 50))

        skepticism_dist_message = {skepticism.name: dist for skepticism, dist in simulator.skepticism_dist.items()}
        parameters = f"size = {simulator.world_board.size}, density = {simulator.world_board.population_density}, cooldown = {simulator.rumor_cool_down}, skepticism = {skepticism_dist_message}, rate = {rate}, rounds = {rounds}"
        parameters_text = small_font.render(parameters, 1, (100, 100, 100))
        win.blit(parameters_text, ((WINDOW_WIDTH - parameters_text.get_width()) // 2, WINDOW_HEIGHT - 30))

        # rendering each cell into the window
        for person_id in simulator.world_board.world_iterator():
            person = simulator.world_board.person_by_id(person_id)
            if person.has_rumor:
                color = BLACK
            elif person.curr_skepticism == SkepticismLevel.S1:
                color = GREEN
            elif person.curr_skepticism == SkepticismLevel.S2:
                color = YELLOW
            elif person.curr_skepticism == SkepticismLevel.S3:
                color = ORANGE
            elif person.curr_skepticism == SkepticismLevel.S4:
                color = RED

            scale = WINDOW_WIDTH // simulator.world_board.size
            pygame.draw.rect(win, color, (person_id.row * scale, person_id.col * scale + 100, scale, scale))

        simulator.next_generation()
        pygame.display.update()


def simulate(simulator, rate, rounds):
    pygame.init()
    pygame.display.set_caption("Rumor Spreading Simulation")
    simulation_loop(simulator, rate, rounds)

    plt.title("Spread rumor process by generation")
    plt.xlabel('Generations')
    plt.ylabel('Spread Process')
    plt.plot(range(len(simulator.rumors_spread_count)), simulator.rumors_spread_count)
    plt.show()

    pygame.quit()


def main():
    user_params = receive_user_params()
    simulator = RumorSpreadingSimulator(
        world_size=user_params.world_size,
        population_density=user_params.population_density,
        rumor_cool_down=user_params.rumor_cool_down,
        skepticism_dist=user_params.skepticism_dist
    )
    simulate(simulator, user_params.rate, user_params.rounds)


if __name__ == '__main__':
    main()
