import unittest
import subprocess
import os

class TestLinkState(unittest.TestCase):

    def setUp(self):
        """Clear the output file before each test."""
        with open('output.txt', 'w') as file:
            file.truncate(0)  # Truncate the file to zero length, effectively clearing it

    def run_link_state(self, topology, message, changes, expected_output):
        # Run the linkstate.py with the given input files
        subprocess.run(['py', 'linkstate.py', f'{topology}', f'{message}', f'{changes}'])

        # Open and read the output and expected output
        with open('output.txt', 'r') as file:
            actual_output = file.read()
        with open(f'{expected_output}', 'r') as file:
            expected_output = file.read()

        # Compare the actual output to the expected output
        self.assertEqual(actual_output, expected_output, "The outputs do not match")

    def test_case_1(self):
        self.run_link_state('topology.txt', 'message.txt', 'changes.txt', 'expected_outputls.txt')

    def test_case_2(self):
        self.run_link_state('topology.txt', 'message2.txt', 'changes.txt', 'expected_output2ls.txt')

    def test_case_3(self):
        self.run_link_state('topology2.txt', 'message3.txt', 'changes.txt', 'expected_output3ls.txt')

if __name__ == '__main__':
    unittest.main()
