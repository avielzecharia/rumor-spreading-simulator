import time
import argparse
import matplotlib.pyplot as plt

from rumor_spreading_simulator.engine.person import SkepticismLevel
from rumor_spreading_simulator.engine.simulator import RumorSpreadingSimulator


def simulation_loop(simulator, rate, generations):
    print(info_message(simulator))
    for _ in range(generations):
        message = board_message(simulator)
        print(board_message(simulator), end="")
        time.sleep(rate)
        print("\x1b[1A\x1b[2K" * (message.count('\n') + 1))

        simulator.next_generation()


def info_message(simulator):
    skepticism_dist_message = {skepticism.name: dist for skepticism, dist in simulator.skepticism_dist.items()}
    return "\n".join((
        f"World size: {simulator.world_board.size}",
        f"Population density: {simulator.world_board.population_density}",
        f"Rumor cool down time: {simulator.rumor_cool_down}",
        f"Skepticism distribution: {skepticism_dist_message}",
        "\n"
        f"\x1b[93m*\033[0m - rumor, \x1b[91mred\033[0m - exposed to rumor, \x1b[92mgreen\033[0m - not exposed to rumor",
        "\n"
    ))


def board_message(simulator):
    board = "\n".join(
        " ".join(
            person_message(people) for people in row
        )
        for row in simulator.world_board._board
    )
    return "\n".join((
        f"Generation number: {simulator.generation}",
        f"Rumor Count: {simulator.rumor_count}",
        f"Rumor Relative: {simulator.rumor_relative}",
        board
    ))


def person_message(person):
    if not person:
        return " "

    if person.has_rumor:
        return '\x1b[93m' + '*' + '\033[0m'

    visualize = person.curr_skepticism.name[-1:]

    if person.ever_has_rumor:
        # coloring in red cells with rumor
        visualize = '\x1b[91m' + visualize + '\033[0m'
    else:
        visualize = '\x1b[92m' + visualize + '\033[0m'

    return visualize


def main():
    parser = argparse.ArgumentParser(
        description="Rumor Spreading Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-M', '--size', help='Size of the MxM world board', default=100, type=int)
    parser.add_argument('-P', '--density', help='Population density to randomize', default=0.8, type=float)
    parser.add_argument('-L', '--cool-down', help='Cool down time between spreading rumor again', default=5, type=int)
    parser.add_argument('-S', '--rumor-dist', nargs='+', help='Population spread types distribution <S1 S2 S3 S4>',
                        default=[0.25, 0.25, 0.25, 0.25], type=float)
    parser.add_argument('-R', '--rate', help='Number of second to the next generation', default=0.5, type=float)
    parser.add_argument('-G', '--generations', help='Number of generation to simulate', default=60, type=int)
    args = parser.parse_args()

    simulator = RumorSpreadingSimulator(
        world_size=args.size,
        population_density=args.density,
        rumor_cool_down=args.cool_down,
        skepticism_dist=dict(zip(SkepticismLevel, args.rumor_dist))
    )

    simulation_loop(simulator, args.rate, args.generations)

    plt.title("Spread rumor process by generation")
    plt.xlabel('Generations')
    plt.ylabel('Spread Process')
    plt.plot(range(len(simulator.rumors_spread_count)), simulator.rumors_spread_count)
    plt.show()


if __name__ == '__main__':
    main()
