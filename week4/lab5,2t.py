from dataclasses import dataclass
from unittest import TestCase, main


# Correct Singleton implementation
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If instance does not exist, create and store it
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # Return the existing instance
        return cls._instances[cls]


# Example class using Singleton
@dataclass
class Environment(metaclass=Singleton):
    name: str = "Production"
    version: int = 1


# Unit test to verify Singleton behavior
class TestSingleton(TestCase):

    def test_singleton_should_return_same_instance(self):
        @dataclass
        class A(metaclass=Singleton):
            a: int = 0

        instance1 = A(2)
        instance2 = A()

        # Both should refer to the same instance
        self.assertEqual(instance1, instance2)


if __name__ == "__main__":
    main()