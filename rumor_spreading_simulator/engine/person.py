import enum
import random


class Person:
    """
    This class describes a single people state in the population
    """
    def __init__(self, skepticism):
        self._current_cool_down = 0                                 # current cool down until next spread
        self._rumor_count = 0                                       # number of times hearing rumor right now
        self._has_rumor = False                                     # is keeping rumor right now
        self._ever_has_rumor = False                                # is getting rumor until now (all generations)

        self._base_skepticism = skepticism                          # basic skepticism level
        self._current_skepticism = skepticism                       # current skepticism level
        self._should_spread = self._randomize_spread_decision()     # should spread rumor in current generation

    def notify_generation_start(self):
        """
        Notify the person that a new generation have started.
        """
        # Update cool down time
        if self._current_cool_down != 0:
            self._current_cool_down -= 1

        if self._rumor_count == 0:
            self._has_rumor = False                             # Update no rumors to spread
        elif self._rumor_count > 1:
            self._current_skepticism = self._base_skepticism    # Decrease skepticism - more than 1 friend spread me

        self._rumor_count = 0                                       # Initialize rumor count
        self._should_spread = self._randomize_spread_decision()     # Regenerating spread probability

    def should_spread_rumor(self):
        """
        Check whether the person should spread a rumor in current generation.
        """
        # If we are in cool down no spread is approved
        if self._current_cool_down != 0:
            return

        return self.has_rumor and self._should_spread

    def notify_rumor(self):
        """
        Notify the person in a new rumor by a friend.

        :returns: True if it the first time the rumor spread to the person, otherwise false
        :rtype: bool
        """
        # If we are in cool down rumor is irrelevant
        if self._current_cool_down != 0:
            return False

        # More that one friend already spread to me the rumor - decrease skepticism
        if self._rumor_count:
            self._current_skepticism = _decrease_skepticism(self._base_skepticism)

        self._rumor_count += 1          # Update rumor count
        self._has_rumor = True          # Update rumor is spread to me right now

        ever_has_rumor_before = self._ever_has_rumor
        self._ever_has_rumor = True     # Update rumor is spread to me ever

        return ever_has_rumor_before != self._ever_has_rumor

    def notify_spread_rumor(self, rumor_cool_down):
        """
        Notify the person that rumor spread to his friend.
        """
        # Update the cool down to max
        self._current_cool_down = rumor_cool_down

    def force_optimistic(self):
        """
        Force the person to spread the rumor for the current generation.
        """
        self._current_skepticism = SkepticismLevel.S1

    def _randomize_spread_decision(self):
        return random.random() < self._current_skepticism.value

    @property
    def has_rumor(self):
        return self._has_rumor

    @property
    def curr_skepticism(self):
        return self._current_skepticism

    @property
    def ever_has_rumor(self):
        return self._ever_has_rumor


class SkepticismLevel(enum.Enum):
    S1 = 1          # Believe all
    S2 = 1/2
    S3 = 1/3
    S4 = 0          # Believe Nothing


def _decrease_skepticism(skepticism_level):
    return {
        SkepticismLevel.S1: SkepticismLevel.S1,
        SkepticismLevel.S2: SkepticismLevel.S1,
        SkepticismLevel.S3: SkepticismLevel.S2,
        SkepticismLevel.S4: SkepticismLevel.S3,
    }.get(skepticism_level)
