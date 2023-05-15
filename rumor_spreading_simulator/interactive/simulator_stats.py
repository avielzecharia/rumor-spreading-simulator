import argparse
import matplotlib.pyplot as plt

from rumor_spreading_simulator.engine.person import SkepticismLevel
from rumor_spreading_simulator.engine.simulator import RumorSpreadingSimulator


def simulation_loop(simulator, times, generations):
    rumors_spread_count_summary = None
    rumors_spread_count_size = 0
    for t in range(times):
        print(f"Simulating round #{t+1}...")
        simulator.jump_generation(generations)

        # Keep the spread rumor sum of all previous simulations
        if rumors_spread_count_summary:
            rumors_spread_count_summary = [
                x + y for x, y in zip(rumors_spread_count_summary, simulator.rumors_spread_count)
            ]
        else:
            rumors_spread_count_summary = simulator.rumors_spread_count
            rumors_spread_count_size = len(simulator.rumors_spread_count)

        simulator = simulator.generate_new_age()

    # Plot the average graph
    rumors_spread_count_summary = [x / times for x in rumors_spread_count_summary]
    plt.title("Spread rumor process by generation")
    plt.xlabel('Generations')
    plt.ylabel('Spread Process')
    plt.plot(range(rumors_spread_count_size), rumors_spread_count_summary)
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Rumor Spreading Statistics Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-M', '--size', help='Size of the MxM world board', default=100, type=int)
    parser.add_argument('-P', '--density', help='Population density to randomize', default=0.8, type=float)
    parser.add_argument('-L', '--cool-down', help='Cool down time between spreading rumor again', default=5, type=int)
    parser.add_argument('-S', '--rumor-dist', nargs='+', help='Population spread types distribution <S1 S2 S3 S4>',
                        default=[0.25, 0.25, 0.25, 0.25], type=float)
    parser.add_argument('-T', '--times', help='Number of times to simulate execution', default=1, type=int)
    parser.add_argument('-G', '--generations', help='Number of generation to simulate', default=60, type=int)
    args = parser.parse_args()

    simulator = RumorSpreadingSimulator(
        world_size=args.size,
        population_density=args.density,
        rumor_cool_down=args.cool_down,
        skepticism_dist=dict(zip(SkepticismLevel, args.rumor_dist))
    )

    simulation_loop(simulator, args.times, args.generations)


if __name__ == '__main__':
    main()
