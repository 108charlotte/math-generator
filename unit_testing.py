import unittest
from main import calc_full_equation

class TestEquationGenerator(unittest.TestCase): 
    def test_one_number(self): 
        equation = calc_full_equation(1, 100)
        print("test_one_number: " + equation)
        self.assertTrue(equation is not None) # will also check if it raises an error
    
    def test_two_numbers(self): 
        equation = calc_full_equation(2, 100)
        print("\ntest_two_numbers: " + equation)
        self.assertTrue(equation is not None)
    
    def test_fifty_numbers_no_exponentation(self): # don't want to worry about overflow 
        equation = calc_full_equation(50, 100, operations=["+", "-", "/", "*", "%"])
        print("\ntest_fifty_numbers_no_exponential: " + equation)
        self.assertTrue(equation is not None)
    
    def test_no_grouping_no_exponentation(self): # checking that choosing to not have any grouping symbols does not result in errors
        equation = calc_full_equation(50, 100, [], operations=["+", "-", "/", "*", "%"])
        print("\ntest_no_grouping_no_exponentation: " + equation)
        self.assertTrue(equation is not None)
    
    def test_no_operations(self): # making sure that no operations will just return the number's identity (n=n) so long as there's only one number
        equation = calc_full_equation(1, 100, ["()"], [])
        print("\ntest_no_operations: " + equation)
        self.assertTrue(equation is not None)
    
    def test_no_operations_too_many_nums(self): # making sure this fails, since you can't have multiple numbers in an equation without operators
        with self.assertRaises(SyntaxError) as context: 
            equation = calc_full_equation(50, 100, ["()"], [])
        print("\ntest_no_operations_too_many_nums: " + str(context.exception))
        self.assertEqual(str(context.exception), "You cannot create an equation with multiple numbers without an operator. Either add at least one operator or restrict the equation to one number only")
    
    def test_no_nums(self): 
        equation = calc_full_equation(0, 100)
        print("\ntest_no_nums: " + equation)
        self.assertTrue(equation is not None)

    def test_big_nums(self): 
        with self.assertRaises(OverflowError) as context: 
            equation = calc_full_equation(100, 999999, num_reruns=2) # low number of reruns bc I don't want to handle many; since I'm trying to make it crash, and each time it crashes takes a while, I don't want to wait for this to happen many times
        print("\ntest_big_nums: " + str(context.exception))
        self.assertEqual(str(context.exception), f"After attempting 2 reruns, we were unable to generate an equation which didn't overflow python's float limit. Please either decrease the num length and/or num magnitude limit or remove ** from the operations list (if you want to keep the same num length limit and/or num magnitude limit the same). You can also increase your number of retries, but doing so will increase computation time and, at a certain equation size, will no longer work")