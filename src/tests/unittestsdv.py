import unittest
import subprocess

class TestDistanceVector(unittest.TestCase):
    def run_distance_vector(self, topology, message, changes, expected_output):
        # Run the distancevector.py with the given input files
        subprocess.run(['py', 'distancevector.py', f'{topology}', f'{message}', f'{changes}']) # Change py to python or python 3 depending on your system

        # Open and read the output and expected output
        with open('output.txt', 'r') as file:
            actual_output = file.read()
        with open(f'{expected_output}', 'r') as file:
            expected_output = file.read()

        # Compare the actual output to the expected output
        self.assertEqual(actual_output, expected_output, "The outputs do not match")
    #print("Testing changes (new link and erasing link)")
    def test_case_1(self):
        self.run_distance_vector('topology.txt', 'message.txt', 'changes.txt', 'expected_output.txt')
    print("Testing message between unreachable nodes")
    def test_case_2(self):
       self.run_distance_vector('topology.txt', 'message2.txt', 'changes.txt', 'expected_output2.txt')
    
    def test_case_3(self):
       self.run_distance_vector('topology2.txt', 'message3.txt', 'changes.txt', 'expected_output3.txt')

if __name__ == '__main__':
    unittest.main()
