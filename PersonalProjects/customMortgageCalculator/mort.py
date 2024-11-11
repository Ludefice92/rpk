#!/bin/env python3
import argparse
import pandas as pd
import warnings
# Suppress all warnings, for now this is just to ignore a spam message from pandas to make the console output more readable
warnings.simplefilter(action='ignore', category=FutureWarning)

def calculate_mortgage_payment(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    number_of_payments = years * 12
    monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    return round(monthly_payment,2)

def calculate_interest_payment(outstanding_balance, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    interest_payment = outstanding_balance * monthly_interest_rate
    return round(interest_payment,2)

def calculate_amortization_schedule(house_value, down_payment_multiplier, annual_interest_rate, years, opportunity_cost_base, property_tax, rent_saved, help, monthly_expense_difference, maintenance_fees, is_condo):
    principal = house_value * down_payment_multiplier
    monthly_payment = calculate_mortgage_payment(principal, annual_interest_rate, years)
    outstanding_balance = principal
    opportunity_cost = opportunity_cost_base #opportunity cost accounting for money lost by not investing the down payment in the S&P500
    sp500_return = 1.0057 #assuming historical rate of 0.57% per month, using this to model opportunity cost lost from down payment
    #property_tax_annual_increase = ? #TODO: need to figure out a way to model this...looks like it's a % of the property value, but not sure how that % of the property value changes over time or how often it is updated due to property value increases/whether it tracks property value well or not
    rent_increase_rate = 1.025 #average increase in rent over time could be done per city based on historical data used ontario 2.5% per annum max for rent controlled units (only accurate if not moving ever and law unchanged)
    rent_base = rent_saved #updating this base value later as it changes every year
    land_transfer_tax = 5000 #assuming 5000, low because of first time home buyer incentive of 4000 could be 4000 higher
    agent_fee_multiplier = 0.9435 #assuming 5% agent fee to sell + HST, comes out of sale only
    current_house_value = house_value #will increment based on appreciation rate monthly
    appreciation_rate = 1.00327 #assuming 4% converted to monthly #TODO: make this an input
    condo_fees = 600 #assuming 600/month, slightly higher on average likely but reduced since it often covers things like water
    
    #used for profit calculation
    total_interest_paid = 0
    total_property_tax_paid = 0
    total_extra_monthly_expenses_paid = 0
    total_maintenance_fees_paid = 0
    total_condo_fees_paid = 0
    total_help = 0

    schedule = []
    
    for month in range(1, years * 12 + 1):
        if (month % 12) == 0: #increments costs which increase on an annual basis
            rent_base *= rent_increase_rate
            #property_tax *= property_tax_increase #TODO: update this when I find data on avg property tax changes
        if month != 1:
            rent_saved += rent_base
        opportunity_cost *= sp500_return
        interest_payment = calculate_interest_payment(outstanding_balance, annual_interest_rate)
        principal_payment = monthly_payment - interest_payment
        outstanding_balance -= principal_payment
        total_interest_paid += interest_payment
        total_property_tax_paid += property_tax
        total_extra_monthly_expenses_paid += monthly_expense_difference
        total_maintenance_fees_paid += maintenance_fees
        total_help += help
        current_house_value *= appreciation_rate
        profit_if_sold = (current_house_value * agent_fee_multiplier) - land_transfer_tax - total_interest_paid - opportunity_cost - outstanding_balance - total_extra_monthly_expenses_paid - total_maintenance_fees_paid + rent_saved + help #TODO: will need to update this as I add expenses/revenues
        if is_condo:
            total_condo_fees_paid += condo_fees
            profit_if_sold -= total_condo_fees_paid
            profit_if_sold_with_help = profit_if_sold + total_help
            schedule.append((month, monthly_payment, interest_payment, principal_payment, round(outstanding_balance,2), round((opportunity_cost-opportunity_cost_base),2),
                             round(total_property_tax_paid,2), round(rent_saved,2), round(current_house_value,2), total_extra_monthly_expenses_paid, total_maintenance_fees_paid,
                             total_condo_fees_paid, round(profit_if_sold,2), total_help, round(profit_if_sold_with_help,2)))
        else:
            profit_if_sold_with_help = profit_if_sold + total_help
            schedule.append((month, monthly_payment, interest_payment, principal_payment, round(outstanding_balance,2), round((opportunity_cost-opportunity_cost_base),2),
                             round(total_property_tax_paid,2), round(rent_saved,2), round(current_house_value,2), total_extra_monthly_expenses_paid, total_maintenance_fees_paid,
                             round(profit_if_sold,2), total_help, round(profit_if_sold_with_help,2)))
    
    return schedule

def main():
    #call a new function which pulls in all of the inputs needed and returns a dict or something which carries all of the info needed
    #to do the calculations necessary to get the profit on a month per month basis

    #need to update pandas columns to fit to the size they should be

    parser = argparse.ArgumentParser(description='This script finds out how much a mortgage really costs you in interest over a given amortization schedule and sends the outputs to an excel spreadsheet')

    parser.add_argument('-f', '--flaky-verdicts', action='store_true', help='Run only for flaky verdicts')
    args = parser.parse_args()

    #actual code starts here
    #defining lists of prices, rates, and amortization periods I care about
    house_value_list = [400000,425000,450000,475000,500000,525000,550000,575000,600000,625000,650000,675000,700000]  # Loan principal in dollars
    annual_interest_rate_list = [3,3.25,3.5,3.75,4,4.25,4.5,4.75,5,5.25,5.5,5.75,6,6.25,6.5,6.75,7]  # Annual interest rate in percent
    amortization_period_list = [25,30]  # total loan term in years
    down_payment_multiplier = 0.8 #assuming 20% down
    property_tax = 416.66666666666666666666666666667 #assuming 5000/yr, could be a list
    current_average_rent_2_bed_apartment = 1800 #accurate?
    my_apartment = 1261 #current rent/12
    help_from_others = 1500 #1500 #for the case where I were to get my dad to live with me and he pays this much
    is_condo = True #is a condo or not for condo fees
    maintenance_fees = 300 #assuming $300/month maintenance fees
    
    monthly_expense_difference = -55 + 120 + 70 + 120 #calculated using in order...hydro, water, gas

    #TODO: iscondo boolean which triggers use of condo_fees, could be script input then asks for it if its true
    #also need script input for everything else, should separate this from main so main can handle just the
    #user interaction and basic function calls

    with pd.ExcelWriter("mortgage_amortization_schedule.xlsx", engine='xlsxwriter') as writer:
        for house_value in house_value_list:
            opportunity_cost_base = house_value - (house_value*down_payment_multiplier) #down payment 
            for rate in annual_interest_rate_list:
                for loan_length in amortization_period_list:
                    amortization_schedule = calculate_amortization_schedule(house_value, down_payment_multiplier, rate, loan_length, opportunity_cost_base, property_tax, my_apartment, help_from_others, monthly_expense_difference, maintenance_fees, is_condo)
                    if is_condo:
                        # Convert to DataFrame
                        df = pd.DataFrame(amortization_schedule, columns=['Month', 'Monthly Payment', 'Interest Payment', 'Principal Payment', 'Remaining Balance', 'Opportunity Cost', 'Property Tax', 'Rent Saved', 'House Value', 'Expenses>Apartment', 'Maintenance Fees', 'Condo Fees', 'Profit Sold EoM', 'Help', 'Profit with Help'])
                    else:
                        # Convert to DataFrame
                        df = pd.DataFrame(amortization_schedule, columns=['Month', 'Monthly Payment', 'Interest Payment', 'Principal Payment', 'Remaining Balance', 'Opportunity Cost', 'Property Tax', 'Rent Saved', 'House Value', 'Expenses>Apartment', 'Maintenance Fees', 'Profit Sold EoM', 'Help', 'Profit with Help'])
                    # Save to Excel
                    sheet_name = f'{house_value}_{rate}_{loan_length}'
                    df.to_excel(writer, sheet_name, index=False)
                    # Access the worksheet object to set column width
                    workbook = writer.book
                    worksheet = writer.sheets[sheet_name]

                    # Set column widths based on content
                    for idx, col in enumerate(df.columns):
                        max_len = max(
                            df[col].astype(str).map(len).max(),  # Length of largest item
                            len(col)  # Length of column name/header
                        )  # Adding a little padding
                        worksheet.set_column(idx, idx, max_len)
            print(f'done {house_value}')

if __name__ == '__main__':
    main()
