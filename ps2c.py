
def main():
    poly = (-13.39, 0.0, 17.5, 3.0, 1.0) 
    x_0 = 0.1 
    epsilon = .0001
    print(f"The Root is: {compute_root(poly,x_0,epsilon)}")
    print("Expected Answer: (0.80679075379635201, 8) ")



def compute_root(poly,x_0,epsilon):
    """Uses Newton's successive approximation to find roots
    poly: tuple of numbers
    x_0: initial guess
    epsilon: error bound
    returns:tuple, first element root of polynomial, second element number of iterations
    """
    #represents the number of iterations
    numIter = 1
    #assigns x_0 to the initial guess
    initial_guess = x_0
    while abs(evaluate_poly(poly,initial_guess) - 0) > epsilon:
        """Determine the using the formula:
           1. new guess from the formula.
           
        """
        #increment counter
        numIter += 1
        #returns float for value of given function
        f = evaluate_poly(poly, initial_guess)
        #compute the derivative of the function
        deriv = compute_deriv(poly)
        #compute value of the first derivative using deriv
        f1  = evaluate_poly(deriv,initial_guess)
        #f1 = evaluate_poly(compute_deriv(poly),initial_guess)
        new_guess = initial_guess - f/f1
        #assign new guess to initial guess
        initial_guess = new_guess

    return initial_guess, numIter


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

def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function
    poly: tuple of numbers, length>0
    returns: tuple of numbers
    """
    #makes a copy of the tuple from the one-th element to the last element of tuple
    poly_copy = poly[1:]
    result = ()
    #start from index 1, this is the python way.It just works.
    index = 1
    for coef in poly_copy:
        ans = index * coef
        result = result + (ans,)
        index += 1 
    return result

if __name__ == "__main__":
    main()