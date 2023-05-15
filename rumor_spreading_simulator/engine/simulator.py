import copy

from rumor_spreading_simulator.engine.WorldBoard2D import WorldBoard2D
from rumor_spreading_simulator.engine.person import SkepticismLevel


class RumorSpreadingSimulator:
    """
    Simulator engine for spreading rumors in a 2D population world.
    """
    def __init__(
            self,
            world_size=100,
            population_density=0.8,
            rumor_cool_down=5,
            skepticism_dist=None
    ):
        """
        :type world_size: int
        :type population_density: float
        :type rumor_cool_down: int
        :type skepticism_dist: dict[SkepticismLevel, float]
        """
        if skepticism_dist is None:
            skepticism_dist = {s: 1 / len(SkepticismLevel) for s in SkepticismLevel}

        self._generation = 0                # Current generation number
        self._rumor_count = 1               # Number of person the rumor spread to
        self._rumors_spread_count = [1]     # Count of spread rumors per generation

        self._rumor_cool_down = rumor_cool_down
        self._skepticism_dist = skepticism_dist
        self._world_board = WorldBoard2D.generate_board(world_size, population_density, skepticism_dist)

        # Force a random person to be the first one to spread the rumor for all friends
        root_person = self.world_board.person_by_id(self.world_board.get_random_person())
        root_person.notify_rumor()
        root_person.force_optimistic()

    def generate_new_age(self):
        """
        Generate new simulator with same parameters.

        :rtype: RumorSpreadingSimulator
        """
        return RumorSpreadingSimulator(
            world_size=self.world_board.size,
            population_density=self.world_board.population_density,
            rumor_cool_down=self.rumor_cool_down,
            skepticism_dist=self.skepticism_dist
        )

    def next_generation(self):
        """
        Simulate a single generation evaluation.
        """
        new_board = copy.deepcopy(self._world_board)

        spread_rumor_count = 0
        for person_id in self.world_board.world_iterator():
            spread_rumor_count += self._evaluate_next_gen(person_id, new_board)

        self._rumors_spread_count.append(spread_rumor_count)
        self._world_board = new_board
        self._generation += 1

    def jump_generation(self, steps):
        """
        Simulate X steps generation evaluation.
        """
        for _ in range(steps):
            self.next_generation()

    def _evaluate_next_gen(self, person_id, new_board):
        person = new_board.person_by_id(person_id)
        person.notify_generation_start()

        rumors_spread_count = 0
        for friend_id in self._world_board.get_person_friends(person_id):
            friend = self._world_board.person_by_id(friend_id)
            if friend.should_spread_rumor():
                rumors_spread_count += person.notify_rumor()
                new_friend = new_board.person_by_id(friend_id)
                new_friend.notify_spread_rumor(self.rumor_cool_down)

        self._rumor_count += rumors_spread_count
        return rumors_spread_count

    @property
    def generation(self):
        return self._generation

    @property
    def world_board(self):
        return self._world_board

    @property
    def skepticism_dist(self):
        return self._skepticism_dist

    @property
    def rumor_cool_down(self):
        return self._rumor_cool_down

    @property
    def rumor_count(self):
        return self._rumor_count

    @property
    def rumor_relative(self):
        return self.rumor_count / self.world_board.population_size

    @property
    def rumors_spread_count(self):
        return self._rumors_spread_count
