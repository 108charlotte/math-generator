from main import calc_full_equation
# NOTE: does not currently support multiple types of grouping symbols :(
def gen_dataset(size): 
    equations = []
    for _ in range(size): 
        equations.append(calc_full_equation(20, 1000, ["()"], ["+", "-", "/", "*", "**", "%"], 10))
    return equations

if __name__ == "__main__": 
    result = gen_dataset(100)
    print(result)
    print("len: " + str(len(result))) # if this len is less than the size you passed, try increasing num retries or decreasing either of the first two parameters