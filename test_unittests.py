import main
import solver
import unittest # Test framework
import math

class Test_TestFileLoad(unittest.TestCase):
    def test_guesses(self):
        self.assertEqual(main.loadGuesses()[0], "aahed")

    def test_answers(self):
        self.assertEqual(main.loadAnswers()[0], "aback")

class Test_TestSolver(unittest.TestCase):
    def test_expectedInformation(self):
        self.assertAlmostEqual(solver.uExpectedInformation("weary", main.loadGuesses()), 4.902, delta=3)

    def test_generatePattern(self):
        self.assertEqual(solver.generatePattern("weary", "wordy"), [2, 0, 0, 1, 2])

    def test_generatePatternDuplicateLetters(self):
        self.assertEqual(solver.generatePattern("babes", "abbey"), [1, 1, 2, 2, 0])
        self.assertEqual(solver.generatePattern("speed", "abide"), [0, 0, 1, 0, 1])
        self.assertEqual(solver.generatePattern("speed", "erase"), [1, 0, 1, 1, 0])
        self.assertEqual(solver.generatePattern("speed", "steal"), [2, 0, 2, 0, 0])
        self.assertEqual(solver.generatePattern("speed", "crepe"), [0, 1, 2, 1, 0])

if __name__ == '__main__':
    unittest.main()