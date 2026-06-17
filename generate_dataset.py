from main import calc_full_equation

def gen_dataset(size): 
    equations = []
    for _ in range(size): 
        try: 
            equations.append(calc_full_equation())
        except OverflowError: 
            continue
    return equations

if __name__ == "__main__": 
    print(gen_dataset(100_000))