"""Takes input information about income and 
calculates how much money should go to the main 
categories of a home budget"""

main_categories = ['rent/mortgage','utilities(water, electric, gas)' 
                   , 'savings',
                   ]

print('Home Budget Creator\n')
print('Main budget categories are as follows: ')
budget_breakdown = {}
for cat in main_categories:
    budget_breakdown[cat]=0
    
print("Default budget items :")
for cat in budget_breakdown.keys():
    print(cat)

while True:
    misc_cat = input("Enter another category/expense to add to budget(type 'Done' when finished: ")
    if misc_cat.lower() == 'done':
        break
    misc_dollar_amt = input("""Enter the dollar amount allocated monthly to this category/expense(0 will be allocated as 
    remainder after other budget items accounted for: $""")
    budget_breakdown[misc_cat] = float(misc_dollar_amt)
    
print()

monthly_income = {}
while True:
    income_source = input("Enter name of source of income(type 'Done' when finished: ")
    if income_source.lower()=='done':
        break
    income_amt = input("Enter amount of monthly income from this source: $")
    monthly_income[income_source] = float(income_amt)

"""
given bills and income, break down budget into recommended amounts based on standard percentages
"""
total_monthly_income = 0
for source in monthly_income.keys():
    total_monthly_income += monthly_income[source]
    
print("Total monthly income: $"+str(total_monthly_income))    

budget_breakdown['rent/mortgage']= .25 * total_monthly_income
budget_breakdown['utilities(water, electric, gas)'] = .1 * total_monthly_income
budget_breakdown['savings']= .2 * total_monthly_income
misc_spending_allocation = .45 * total_monthly_income
misc_categories = []

#TODO: probably better way to do this that doesn't involve looping over the list twice
for category in budget_breakdown.keys():
    if category not in ['rent/mortgage','utilities(water,electric,gas)','savings']:
        if budget_breakdown[category]==0:
            misc_categories.append(category)
        misc_spending_allocation -= budget_breakdown[category]

for category in misc_categories:
    if budget_breakdown[category] == 0:
        budget_breakdown[category] = misc_spending_allocation / len(misc_categories)
    
print("Max allowed monthly expenditure based on percentages and current unwaverable expenses is as follows: ")
for category in budget_breakdown.keys():
    print(category+" : $"+format(budget_breakdown[category],'.2f'))
        

