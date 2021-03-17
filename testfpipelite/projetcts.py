import pytest
import fpipelite.data.project
import os

class TestProjects:

    def test_find_relative_dot(self):
        print("\nabs of dot: " + os.path.abspath("."))
        found, data = fpipelite.data.project.FindProjectFromPath(".")
        print("found: " + str(found))
        print("data: " + str(data))

