# The total number of rows in the pattern is 8
rows = 8

for i in range (1, 9):
    # For the first 5 rows, print stars matching the row number
    if i <= 5:
        print("*" * i)
    # For the remaining rows (6 , 7, 8), subtract the row number from 10 to count down
    else:
        print("*" * (10 - i) )    
