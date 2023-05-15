import random
from collections import namedtuple

from rumor_spreading_simulator.engine.person import Person, SkepticismLevel

PersonWorldID = namedtuple("PersonWorldID", ["row", "col"])


class WorldBoard2D:
    """
    This class implemented the 2D population world.
    """
    _FRIENDS_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, size):
        """
        Creates an empty 2D world board.

        :type size: int
        """
        self._size = size                                       # size of the matrix
        self._board = [[None] * size for _ in range(size)]      # matrix of world's person objects
        self._ids = []                                          # list of existing person ids in the world

    @classmethod
    def generate_board(cls, size, density, skepticism_dist):
        """
        Generate a new board based on basic population attributes.

        :type size: int
        :type density: float
        :type skepticism_dist: dict[SkepticismLevel, float]
        """
        world_board = cls(size)
        world_board._ids = [
            PersonWorldID(row=index//size, col=index%size)
            for index in random.sample(
                range(world_board.board_size),
                int(density * world_board.board_size)
            )
        ]

        ids_scanner = iter(world_board._ids)
        for skepticism_level, skepticism_density in skepticism_dist.items():
            for _ in range(int(skepticism_density * world_board.population_size)):
                next_id = next(ids_scanner)
                world_board._board[next_id.row][next_id.col] = Person(skepticism_level)

        return world_board

    @classmethod
    def generate_slow_board(cls, size, density, skepticism_dist):
        """
        Generate a new *slow* board based on basic population attributes.

        :type size: int
        :type density: float
        :type skepticism_dist: dict[SkepticismLevel, float]
        """
        world_board = cls(size)
        world_board._ids = [
            PersonWorldID(row=index//size, col=index%size)
            for index in sorted(random.sample(
                range(world_board.board_size),
                int(density * world_board.board_size)
            ))
        ]

        s1_count = int(skepticism_dist[SkepticismLevel.S1] * world_board.population_size)
        s2_count = int(skepticism_dist[SkepticismLevel.S2] * world_board.population_size)
        s3_count = int(skepticism_dist[SkepticismLevel.S3] * world_board.population_size)
        s4_count = int(skepticism_dist[SkepticismLevel.S4] * world_board.population_size)

        for person_id in world_board._ids:
            if person_id.row % 4 == 0 and s1_count:
                s1_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S1)
            elif person_id.row % 4 == 1 and s2_count:
                s2_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S2)
            elif person_id.row % 4 == 2 and s3_count:
                s3_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S3)
            elif person_id.row % 4 == 3 and s4_count:
                s4_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S4)
            elif s1_count:
                s1_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S1)
            elif s2_count:
                s2_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S2)
            elif s3_count:
                s3_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S3)
            elif s4_count:
                s4_count -= 1
                world_board._board[person_id.row][person_id.col] = Person(SkepticismLevel.S4)

        return world_board

    def get_random_person(self):
        """
        Get random person from the world.

        :rtype: PersonWorldID
        """
        return random.choice(self._ids)

    def person_by_id(self, person_id):
        """
        Get person object by person ID.

        :type person_id: PersonWorldID
        :rtype: rumor_spreading_simulator.engine.person.Person
        """
        if 0 <= person_id.row < self.size and 0 <= person_id.col < self.size:
            return self._board[person_id.row][person_id.col]

        return None

    def get_person_friends(self, person_id):
        """
        Get list of existing friend of a given person.

        :type person_id: PersonWorldID
        :rtype: list[PersonWorldID]
        """
        optional_friends_ids = [
            PersonWorldID(person_id.row + row, person_id.col + col)
            for (row, col) in self._FRIENDS_OFFSETS
        ]

        return [
            friend_id for friend_id in optional_friends_ids
            if self.person_by_id(friend_id)
        ]

    def world_iterator(self):
        """
        Iterate over all persons in the world.

        :rtype: iter
        """
        return iter(self._ids)

    @property
    def size(self):
        return self._size

    @property
    def board_size(self):
        return self._size ** 2

    @property
    def population_size(self):
        return len(self._ids)

    @property
    def population_density(self):
        return self.population_size / self.board_size
