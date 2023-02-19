

def main():
    poly = (0.0, 0.0, 5.0, 9.3, 7.0)
    result = evaluate_poly(poly,-13)
    print(f"Result: {result}") 
    print("Hello Heaven")

def evaluate_poly(poly,x):
    """
    Computes a polynomial function a given value x. Returns that value.
    poly: a tuple of numbers.
    x: number
    returns: float 
    """ 
    #make a copy of the tuple
    poly_copy = poly[:]
    #represents the power
    index = 0
    total = 0.0
    for n in poly_copy:
        total = total + n * x **index
        index += 1
    return total   


if __name__ == "__main__":
    main()
