#!/bin/env python3
import pandas as pd
import warnings
from io import BytesIO

# Suppress all warnings, for now this is just to ignore a spam message from pandas to make the console output more readable
warnings.simplefilter(action='ignore', category=FutureWarning)

def calculate_mortgage_payment(principal, annual_interest_rate, years):
    """
    Calculates the fixed monthly mortgage payment using the standard amortization formula.
    
    This function implements the standard mortgage payment calculation formula that determines
    the fixed monthly payment amount required to fully amortize a loan over a specified period.
    The calculation assumes equal monthly payments throughout the loan term.
    
    Args:
        principal (float): The loan amount (property price minus down payment)
        annual_interest_rate (float): Annual interest rate as a percentage (e.g., 5.5 for 5.5%)
        years (int): Loan amortization period in years
        
    Returns:
        float: Monthly mortgage payment amount rounded to 2 decimal places
        
    Formula:
        M = P * [r(1+r)^n] / [(1+r)^n - 1]
        Where:
        - M = Monthly payment
        - P = Principal loan amount
        - r = Monthly interest rate (annual rate / 12 / 100)
        - n = Total number of payments (years * 12)
    """
    monthly_interest_rate = annual_interest_rate / 12 / 100
    number_of_payments = years * 12
    monthly_payment = ((principal * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) /
                       ((1 + monthly_interest_rate) ** number_of_payments - 1))
    return round(monthly_payment,2)

def calculate_interest_payment(outstanding_balance, annual_interest_rate):
    """
    Calculates the interest portion of a monthly mortgage payment based on the current outstanding balance.
    
    This function determines how much of a monthly payment goes toward interest charges
    based on the remaining loan balance. The interest is calculated as a simple monthly
    interest charge on the outstanding principal.
    
    Args:
        outstanding_balance (float): Current remaining loan balance
        annual_interest_rate (float): Annual interest rate as a percentage
        
    Returns:
        float: Monthly interest payment amount rounded to 2 decimal places
        
    Note:
        The principal payment for the month would be: monthly_payment - interest_payment
        This creates the amortization effect where early payments are mostly interest
        and later payments are mostly principal.
    """
    monthly_interest_rate = annual_interest_rate / 12 / 100
    interest_payment = outstanding_balance * monthly_interest_rate
    return round(interest_payment,2)

def get_current_rate(month, fixed_rate_mortgage, interest_rate, rate_periods):
    """Returns interest rate for given month based on rate periods"""
    if fixed_rate_mortgage:
        return interest_rate
    
    current_month = 1
    for period in rate_periods:
        if current_month <= month <= current_month + (period["term_length"] * 12) - 1:
            return period["interest_rate"]
        current_month += period["term_length"] * 12
    return rate_periods[-1]["interest_rate"] if rate_periods else 5.0

def should_recalculate_payment(month, fixed_rate_mortgage, rate_periods):
    """Determines if payment needs recalculation due to new loan term starting"""
    if fixed_rate_mortgage:
        return month == 1  # Only calculate once for fixed rate
    
    if month == 1:
        return True  # Always calculate for first month
    
    # Check if this month starts a new rate period/loan term
    current_month = 1
    for period in rate_periods:
        term_start = current_month
        term_end = current_month + (period["term_length"] * 12) - 1
        
        if month == term_start and month > 1:
            return True  # New term is starting
        
        current_month = term_end + 1
    
    return False

def calculate_amortization_schedule(inputs):
    """
    Calculates a comprehensive month-by-month amortization schedule with profit analysis for various scenarios.
    
    This is the core calculation function that simulates property ownership over the entire amortization period,
    tracking mortgage payments, property appreciation, rental income, expenses, and multiple profit scenarios.
    The function models complex real estate investment scenarios including:
    - Primary residence vs rental property scenarios
    - Opportunity cost of down payment (modeled as S&P 500 returns)
    - Property appreciation and tax implications
    - Various income sources (rental, assistance, rent savings)
    - Multiple expense categories (taxes, maintenance, condo fees, utilities)
    
    Args:
        inputs (dict): Validated user inputs containing all property and financial parameters
        
    Returns:
        list: A list of tuples, each representing one month's financial data including:
            - Month number, mortgage payment breakdown (principal/interest)
            - Running totals for all expense and income categories
            - Current property value and remaining mortgage balance
            - Profit calculations for multiple scenarios (base, with help, with rental income, etc.)
            
    Key Financial Modeling:
        - Uses 0.57% monthly S&P 500 return for opportunity cost calculation
        - Converts annual rates to monthly equivalents for accurate compounding
        - Tracks profitability breakeven points for different scenarios
        - Handles both condo and non-condo properties with different column structures
        - Calculates cash flow analysis for rental properties
    """
    down_payment_multiplier = inputs.get("down_payment_percentage")*0.01
    opportunity_cost_base = inputs.get("property_price") * down_payment_multiplier
    opportunity_cost = opportunity_cost_base #opportunity cost accounting for money lost by not investing the down payment in the S&P500
    sp500_return = 1.0057 #assuming historical rate of 0.57% per month, using this to model opportunity cost lost from down payment
    principal = inputs.get("property_price") * (1-down_payment_multiplier)
    outstanding_balance = principal
    
    # Initialize payment variables for variable rate support
    monthly_payment = None
    current_rate = None
    annual_property_tax_base = inputs.get("property_taxes")
    annual_property_tax_increase = 1 + inputs.get("annual_property_tax_increase") * 0.01
    land_transfer_tax = inputs.get("land_transfer_tax")
    agent_fee_multiplier = 1 - (inputs.get("real_estate_agent_fee")*0.01)
    current_property_value = inputs.get("property_price") #will increment based on appreciation rate monthly
    appreciation_rate = (1+(inputs.get("appreciation_rate")*0.01))**(1/12) #converting user input to increment on a monthly equivalent basis
    legal_fees = inputs.get("legal_fees")
    breaking_mortgage_early_fee = inputs.get("breaking_mortgage_early_fee")

    #condo specific
    if inputs.get("is_condo") == "Yes":
        condo_fee_annual_increase = 1 + inputs.get("condo_fee_annual_increase") * 0.01
        condo_fee_base = inputs.get("condo_fees")
    else:
        condo_fee_annual_increase = 1
        condo_fee_base = 0
    #rent from old place before moving to new property
    if inputs.get("moving_from_rent") == "Yes":
        rent_increase_rate = 1 + inputs.get("annual_rent_increase") * 0.01
        rent_base = inputs.get("current_rent") #updating this base value later as it changes every year
    else:
        rent_increase_rate = 1
        rent_base = 0
    #rental information for the new property if it is a non principal residence income property
    if inputs.get("rental_income_expected") == "Yes":
        rental_income_increase_rate = 1 + inputs.get("rental_income_annual_increase") * 0.01
        rental_income_base = inputs.get("rental_income")
        occupancy_rate = inputs.get("occupancy_rate") * 0.01
        if inputs.get("are_utilities_paid_by_renter") == "Yes":
            utilities_not_paid_by_occupant = 0
        else:
            utilities_not_paid_by_occupant = inputs.get("total_utilities_not_paid_by_occupant")
    else:
        rental_income_increase_rate = 1
        rental_income_base = 0
        occupancy_rate = 0
        utilities_not_paid_by_occupant = 0
    if inputs.get("is_property_managed") == "Yes":
        property_management_fee_base = rental_income_base * inputs.get("property_management_fees") * 0.01
    else:
        property_management_fee_base = 0

    if inputs["primary_residence"] == "Yes":
        extra_monthly_expenses = inputs.get("utilities_difference")
    else:
        extra_monthly_expenses = 0

    #used for profit calculation
    total_interest_paid = 0
    total_property_tax_paid = 0
    total_extra_monthly_expenses_paid = 0
    total_maintenance_fees_paid = 0
    total_condo_fees_paid = 0
    total_help = 0
    total_rent_saved = rent_base
    total_rental_income = rental_income_base
    total_property_management_fees = property_management_fee_base
    total_utilities_not_paid_by_renter = 0

    #covering all possibilities for profitability given user inputs
    profitability_messages = []
    is_profitable = False
    is_profitable_saving_rent = False
    is_profitable_with_help = False
    is_profitable_saverent_help = False
    is_profitable_renting = False
    is_profitable_renting_help = False
    is_cash_flowing = False

    schedule = []
    
    for month in range(1, inputs.get("amortization_period") * 12 + 1):
        if (month % 12) == 0: #increments costs which increase on an annual basis
            rent_base *= rent_increase_rate
            annual_property_tax_base *= annual_property_tax_increase
            if inputs.get("rental_income_expected") == "Yes":
                rental_income_base *= rental_income_increase_rate
                if inputs.get("is_property_managed") == "Yes": property_management_fee_base = rental_income_base * inputs.get("property_management_fees") * 0.01
            condo_fee_base *= condo_fee_annual_increase
        if month != 1:
            total_rent_saved += rent_base
            total_rental_income += rental_income_base

        # Check if we need to recalculate payment (only at term boundaries)
        if should_recalculate_payment(month, inputs.get("fixed_rate_mortgage", True), inputs.get("rate_periods", [])):
            current_rate = get_current_rate(month, inputs.get("fixed_rate_mortgage", True), 
                                          inputs.get("interest_rate"), inputs.get("rate_periods", []))
            
            # Calculate remaining years for this calculation
            remaining_years = (inputs.get("amortization_period") * 12 - month + 1) / 12
            monthly_payment = calculate_mortgage_payment(outstanding_balance, current_rate, remaining_years)

        opportunity_cost *= sp500_return
        interest_payment = calculate_interest_payment(outstanding_balance, current_rate)
        principal_payment = monthly_payment - interest_payment
        outstanding_balance -= principal_payment
        total_interest_paid += interest_payment
        total_property_management_fees += property_management_fee_base
        total_property_tax_paid += annual_property_tax_base/12 #converting annual property tax to monthly
        total_extra_monthly_expenses_paid += extra_monthly_expenses
        total_utilities_not_paid_by_renter += utilities_not_paid_by_occupant
        total_maintenance_fees_paid += inputs.get("monthly_maintenance")
        if inputs.get("help") == "Yes": total_help += inputs.get("monthly_help")
        current_property_value *= appreciation_rate
        if inputs.get("is_taxed") == "Yes":
            capital_gain = current_property_value - inputs["property_price"]
            capital_gains_tax = capital_gain * inputs["factor"] * (inputs["tax_percentage"] / 100)
        else:
            capital_gains_tax = 0
        profit_if_sold = ((current_property_value * agent_fee_multiplier) - land_transfer_tax - total_interest_paid -
                          opportunity_cost - outstanding_balance - total_extra_monthly_expenses_paid - legal_fees -
                          total_maintenance_fees_paid - total_utilities_not_paid_by_renter - capital_gains_tax)
        if month != inputs.get("amortization_period") * 12:
            profit_if_sold -= breaking_mortgage_early_fee
        if inputs.get("is_condo") == "Yes":
            total_condo_fees_paid += condo_fee_base
            profit_if_sold -= total_condo_fees_paid
        profit_if_sold_with_rent_saved = profit_if_sold + total_rent_saved
        profit_if_sold_with_help = profit_if_sold + total_help
        profit_if_sold_rentsaved_help = profit_if_sold + total_rent_saved + total_help
        profit_if_sold_with_rental_income = profit_if_sold + (total_rental_income * occupancy_rate) - total_property_management_fees
        profit_if_sold_rentalincome_help = profit_if_sold_with_rental_income + total_help
        if outstanding_balance<0: outstanding_balance = 0 #due to rounding it can be negative at the end

        #outputting month of profitability for each combination selling
        if not is_profitable and profit_if_sold > 0:
            is_profitable = True
            profitability_messages.append(f"With no help, rental income, or saving rent from moving, you are profitable after {month} months")
        if inputs.get("moving_from_rent")=="Yes" and not is_profitable_saving_rent and profit_if_sold_with_rent_saved > 0:
            is_profitable_saving_rent = True
            profitability_messages.append(f"Saving ${inputs.get('current_rent'):.2f}/month from your previous rental, you are profitable after {month} months")
        if inputs.get("help")=="Yes" and not is_profitable_with_help and profit_if_sold_with_help > 0:
            is_profitable_with_help = True
            profitability_messages.append(f"With ${inputs.get('monthly_help'):.2f} in help/month, you are profitable after {month} months")
        if inputs.get("moving_from_rent")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_saverent_help and profit_if_sold_rentsaved_help > 0:
            is_profitable_saverent_help = True
            profitability_messages.append(f"Saving ${inputs.get('current_rent'):.2f}/month from your previous rental and getting {inputs.get('monthly_help'):.2f} in help/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and not is_profitable_renting and profit_if_sold_with_rental_income > 0:
            is_profitable_renting = True
            profitability_messages.append(f"Renting your new property at ${inputs.get('rental_income'):.2f}/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_renting_help and profit_if_sold_rentalincome_help > 0:
            is_profitable_renting_help = True
            profitability_messages.append(f"Renting your new property at ${inputs.get('rental_income'):.2f}/month and getting {inputs.get('monthly_help'):.2f} of help/month, you are profitable after {month} months")

        if inputs.get("is_condo") == "Yes":
            row = {
                'Month': month,
                'Current Rate': current_rate,
                'Monthly Payment': monthly_payment,
                'Interest Payment': interest_payment,
                'Principal Payment': principal_payment,
                'Loan Balance': outstanding_balance,
                'Opportunity Cost': opportunity_cost - opportunity_cost_base,
                'Property Tax': total_property_tax_paid,
                'Property Value': current_property_value,
                'Expenses Compared to Last Home': total_extra_monthly_expenses_paid,
                'Maintenance Fees': total_maintenance_fees_paid,
                'Condo Fees': total_condo_fees_paid,
                'Profit': profit_if_sold,
                'Help': total_help,
                'Profit with Help': profit_if_sold_with_help,
                'Rent Saved': total_rent_saved,
                'Rental Income': total_rental_income,
                'Profit if Saving Rent': profit_if_sold_with_rent_saved,
                'Profit with Rent Saved&Help': profit_if_sold_rentsaved_help,
                'Profit with Rental Income': profit_if_sold_with_rental_income,
                'Profit with Rental Income&Help': profit_if_sold_rentalincome_help
            }
        else:
            row = {
                'Month': month,
                'Current Rate': current_rate,
                'Monthly Payment': monthly_payment,
                'Interest Payment': interest_payment,
                'Principal Payment': principal_payment,
                'Loan Balance': outstanding_balance,
                'Opportunity Cost': opportunity_cost - opportunity_cost_base,
                'Property Tax': total_property_tax_paid,
                'Property Value': current_property_value,
                'Expenses Compared to Last Home': total_extra_monthly_expenses_paid,
                'Maintenance Fees': total_maintenance_fees_paid,
                'Profit': profit_if_sold,
                'Help': total_help,
                'Profit with Help': profit_if_sold_with_help,
                'Rent Saved': total_rent_saved,
                'Rental Income': total_rental_income,
                'Profit if Saving Rent': profit_if_sold_with_rent_saved,
                'Profit with Rent Saved&Help': profit_if_sold_rentsaved_help,
                'Profit with Rental Income': profit_if_sold_with_rental_income,
                'Profit with Rental Income&Help': profit_if_sold_rentalincome_help
            }

        # Round all numeric values in one step
        row = {
            key: round(value, 2) if isinstance(value, (int, float)) else value
            for key, value in row.items()
        }

        schedule.append(row)

        # Calculate if the property is cash flowing (for rental properties)
        if not is_cash_flowing and inputs.get("primary_residence") == "No" and inputs.get("rental_income_expected") == "Yes":
            monthly_cash_flow = (rental_income_base * occupancy_rate) - monthly_payment - (annual_property_tax_base / 12) - inputs.get("monthly_maintenance") - condo_fee_base - property_management_fee_base - utilities_not_paid_by_occupant
            if inputs.get("help") == "Yes":
                monthly_cash_flow += inputs.get("monthly_help")
            if monthly_cash_flow > 0:
                is_cash_flowing = True
                profitability_messages.append(f"The property is cash flowing with an initial monthly cash flow of ${monthly_cash_flow:.2f} in month {month}")
            elif month == inputs.get("amortization_period") * 12:
                profitability_messages.append(f"The property is not cash flowing, with an initial monthly loss of ${-monthly_cash_flow:.2f}")

    return pd.DataFrame(schedule), profitability_messages

def generate_monthly_property_profit_spreadsheet(amortization_schedule, property_value, annual_interest_rate, amortization_period):
    """
    Generates and provides a downloadable Excel spreadsheet containing the complete amortization schedule and profit analysis.
    
    This function creates a comprehensive Excel file with month-by-month financial projections for the property investment.
    The spreadsheet includes all calculated values from the amortization schedule, formatted for easy analysis and
    presentation. The function handles different column structures for condo vs non-condo properties and provides
    automatic column width adjustment for optimal readability.
    
    Args:
        amortization_schedule (dict): amortization schedule to be added to the spreadsheet
        property_value (int): value of the purchased property
        annual_interest_rate (float): interest rate of the loan used to purchase the property
        amortization_period (int): length of the term of the loan used to purchase the property
        
    Returns:
        BytesIO: The Excel file as a BytesIO object ready for download
        
    Excel File Contents:
        - Monthly mortgage payment breakdown (principal/interest)
        - Property value appreciation over time
        - Cumulative costs (taxes, maintenance, fees, opportunity cost)
        - Multiple profit scenarios (base, with help, with rental income, etc.)
        - Properly formatted sheet names based on property parameters
        - Auto-sized columns for optimal viewing
        
    File Naming:
        Sheet name format: ${property_value}_{interest_rate}%_{amortization_period}years
        Download filename: amortization_schedule.xlsx
    """

    to_download = BytesIO()

    #ignore to_download warning
    with pd.ExcelWriter(to_download, engine='xlsxwriter') as writer:
        # Save to Excel
        sheet_name = f'${property_value}_{annual_interest_rate}%_{amortization_period}years'
        amortization_schedule.to_excel(writer, sheet_name, index=False)

        # Access the worksheet object to set column width
        worksheet = writer.sheets[sheet_name]
        # Set column widths based on content
        for idx, col in enumerate(amortization_schedule.columns):
            max_len = max(amortization_schedule[col].astype(str).map(len).max(),  # Length of largest item
                          len(col)) + 1 # Length of column name/header
            worksheet.set_column(idx, idx, max_len)

    # Return the BytesIO object
    to_download.seek(0)
    return to_download
