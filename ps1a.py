
"""Solution to problem set 1a.
"""

def main():
    """Uses readVal method to get input from the user.
       Then use the calculate method to determine the monthly payment.
    """
    try:
       creditcard_purchase = readVal(int,"Enter Outstanding  Balance on your credit card e.g 1000  ", "Not an int ")
    except TypeError:
         print("Error")
    try:
        annual_interest_rate = readVal(float,"Enter the annual credit card interest rate as a decimal ","Not a float")
    except TypeError :
        print("Error. use numbers with decimal points")
    try:   
        minimum_monthly_payment_rate = readVal(float,"Enter the minimum monthly payment rate as a decimal ","Not a float")
    except TypeError:
        print("Error")    
    

    #print(f"TOTAL AMOUNT PAID: {calculate(creditcard_purchase,annual_interest_rate,minimum_monthly_payment_rate)}")
    total_amount_paid, remaining_balance = calculate(creditcard_purchase,annual_interest_rate,minimum_monthly_payment_rate)
    print(f"RESULT\nTotal amount paid: {round(total_amount_paid,2)}\nRemaining balance: {round(remaining_balance,2)}")
    

def readVal(valType,requestMsg, errorMsg):
    numTries = 0
    while numTries < 4:
        val = input(requestMsg)
        try:
            val = valType(val)
            return val
        except ValueError:
            print(errorMsg)
            numTries += 1
    raise TypeError("Number of tries exceeded") 





def calculate(creditcard_purchase,annual_interest_rate,minimum_monthly_payment_rate):
    """Calculates the monthly payment, interest paid and principal paid
    """
    number_of_months = 12
    total = 0.0 #TOTAL AMOUNT PAID
    for i in range(number_of_months):
        monthly_payment = creditcard_purchase * minimum_monthly_payment_rate
        interest_paid = annual_interest_rate/12 * creditcard_purchase
        principal_paid = monthly_payment - interest_paid
        remaining_balance = creditcard_purchase - principal_paid
        print(f"Month: {i + 1}\nMinimum Monthly Payment: ${round(monthly_payment,2)}\nPrincipal Paid: ${round(principal_paid,2)}\nRemaining Balance: ${round(remaining_balance,2)} ")
        total = total + principal_paid + interest_paid
        #update the balance on the credit card
        creditcard_purchase = remaining_balance
    return total , remaining_balance
   

if __name__ == "__main__":
    main()