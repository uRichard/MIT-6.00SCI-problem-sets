
def main():
    #poly = (-13.39, 0.0, 17.5, 3.0, 1.0)
    poly = (0.0,0.0,1.0)

    print(f" Derivative: {compute_deriv(poly)}") 
    pass


def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function
    poly: tuple of numbers, length>0
    returns: tuple of numbers
    """
    #makes a copy of the tuple from the one-th element to the last element of tuple.python way
    poly_copy = poly[1:]
       
    result = ()
    #start from index 1, this is the python way.It just works.
    index = 1
    for coef in poly_copy:
        ans = index * coef
        result = result + (ans,)
        index += 1 
    return result



if __name__ =="__main__":
    main()