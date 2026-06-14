import unittest
from main import generate_no_latex

class TestEquationGenerator(unittest.TestCase): 
    def test_one_number(self): 
        equation = generate_no_latex(1, 100)
        print(equation)
        self.assertTrue(equation is not None) # will also check if it raises an error
    
    def test_two_numbers(self): 
        equation = generate_no_latex(2, 100)
        print("\n" + equation)
        self.assertTrue(equation is not None)
    
    def test_fifty_numbers_no_exponentation(self): # don't want to worry about overflow 
        equation = generate_no_latex(50, 100, operations=["+", "-", "/", "*", "%"])
        print("\n" + equation)
        self.assertTrue(equation is not None)
    
    def test_no_grouping_no_exponentation(self): # checking that choosing to not have any grouping symbols does not result in errors
        equation = generate_no_latex(50, 100, [])
        print("\n" + equation)
        self.assertTrue(equation is not None)
    
    def test_no_operations(self): # making sure that no operations will just return the number's identity (n=n) so long as there's only one number
        equation = generate_no_latex(1, 100, ["()"], [])
        print("\n" + equation)
        self.assertTrue(equation is not None)
    
    def test_no_operations_too_many_nums(self): # making sure this fails, since you can't have multiple numbers in an equation without operators
        with self.assertRaises(ValueError) as context: 
            equation = generate_no_latex(50, 100, ["()"], [])
        print("\n" + str(context.exception))
        self.assertTrue(context.exception == "You cannot create an equation with multiple numbers without an operator. Either add at least one operator or restrict the equation to one number only")