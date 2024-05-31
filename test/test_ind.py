from enum import Enum

class TestInd(Enum):
    CONT = "continue with the next test"
    REDO = "restart the test"
    ABAN = "abandon the game"