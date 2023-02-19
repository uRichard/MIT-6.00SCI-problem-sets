
"""Solution to problem set 1b. This uses exhaustive enumeration.
   Searches the search space to find the answer. 
   This program works faster with numbers below 2000. It is slower on other numbers > 20000
"""

initial_balance = 1200
annual_interest_rate = .18
monthly_interest_rate = annual_interest_rate /12.0

previous_balance = initial_balance
monthly_payment = 10
updated_balance = previous_balance * (1 + monthly_interest_rate) - monthly_payment

while updated_balance > 0:
    
    month = 0
    while updated_balance > 0 and month < 12:
        month += 1
        updated_balance = previous_balance * (1 + monthly_interest_rate) - monthly_payment
        print(f"Monthly payment of: {monthly_payment} Remaining balance {updated_balance} Month: {month}")
        previous_balance = updated_balance
    
    if updated_balance < 0:
        print(f"RESULT")
        print(f"Initial balance:{initial_balance}")
        print(f"Monthly payment to pay off debt in 1 year:{monthly_payment}")
        print(f"Number of months needed: {month}")
        print(f"Balance: {updated_balance}")
        break
    #reset and start over with original
    else:
        monthly_payment +=10
        previous_balance = initial_balance
        updated_balance = previous_balance * (1 + monthly_interest_rate) - monthly_payment


    



    