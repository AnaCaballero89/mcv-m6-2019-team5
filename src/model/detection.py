from typing import Tuple

from model import Rectangle


class Detection(Rectangle):
    """
        id: int. For tracking objects
        label: str. Class of the object
    """

    def __init__(self, id: str, label: str, top_left=(0, 0), width=0, height=0):
        super().__init__(top_left, width, height)
        self.id = id
        self.label = label

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Detection(id={0}, label={1}, rectangle={2})'.format(self.id, self.label, super().__str__())

    def to_sort_format(self) -> Tuple[int, int, int, int]:
        return self.top_left + self.get_bottom_right()
