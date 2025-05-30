#!/bin/env python3
import streamlit as st
import pandas as pd
import warnings
from io import BytesIO

# Suppress all warnings, for now this is just to ignore a spam message from pandas to make the console output more readable
warnings.simplefilter(action='ignore', category=FutureWarning)

#TODO: add ad functionality
#TODO: make a website for this instead of using localhost
#TODO: update such that the output spreadsheet has the correct number of columns for every single type of situation (right now just printing 0s for columns that aren't relevant)
#TODO: Convert this implementation from streamlit to django

def initialize_webpage():
    """
    Initializes the Streamlit web interface and collects all user inputs for property profit calculations.
    
    This function creates a comprehensive form that gathers property details, financial parameters,
    and scenario-specific information needed to calculate mortgage payments, property appreciation,
    and various profit scenarios. The function handles conditional input collection based on
    property type (primary residence vs rental) and user circumstances.
    
    Returns:
        dict: A dictionary containing all user inputs with the following key categories:
            - Basic property info: house_price, down_payment_percentage, interest_rate
            - Property details: is_condo, condo_fees, property_taxes
            - Rental scenarios: rental_income, occupancy_rate, property_management_fees
            - Personal circumstances: moving_from_rent, monthly_help, utilities_difference
            - Financial projections: appreciation_rate, amortization_period
            - Tax considerations: is_taxed, tax_percentage, factor
    """
    inputs = {}

    # Collect numeric inputs using text boxes
    primary_residence = st.radio("Is this property going to be your primary residence?", ("Yes", "No"))
    inputs["primary_residence"] = primary_residence
    if primary_residence == "No":
        rental_income_expected = st.radio("Is there expected rental income?", ("Yes", "No"))
        inputs["rental_income_expected"] = rental_income_expected
        if rental_income_expected == "Yes":
            rental_income = st.text_input("How much rental income is expected per month?", value="0")
            inputs["rental_income"] = float(rental_income) if rental_income else 0.0
            rental_income_annual_increase = st.text_input("How much will you increase the rent for your new property each year (in %)?", value="0")
            inputs["rental_income_annual_increase"] = float(rental_income_annual_increase) if rental_income_annual_increase else 0.0
            occupancy_rate = st.text_input("What is the occupancy rate of your new rental (in %, 95 is the max allowed)?", value="0")
            inputs["occupancy_rate"] = float(occupancy_rate) if occupancy_rate else 0.0
            is_property_managed = st.radio("Are you going to pay someone to manage your property for you?", ("Yes", "No"))
            inputs["is_property_managed"] = is_property_managed
            if is_property_managed == "Yes":
                property_management_fees = st.text_input("How much are you going to pay your property manager (as a % of your rental income, standard is 10)?", value="0")
                inputs["property_management_fees"] = float(property_management_fees) if property_management_fees else 0.0
            are_utilities_paid_by_renter = st.radio("Are there utilities that your renter is not paying for?",("Yes", "No"))
            inputs["are_utilities_paid_by_renter"] = are_utilities_paid_by_renter
            if are_utilities_paid_by_renter == "Yes":
                total_utilities_not_paid_by_occupant = st.text_input("How much are you paying in utilities per month that your renter is not responsible for?",value="0")
                inputs["total_utilities_not_paid_by_occupant"] = float(total_utilities_not_paid_by_occupant) if total_utilities_not_paid_by_occupant else 0.0
    else:
        # Check if the user is moving from a rental property
        moving_from_rent = st.radio("Are you moving from a property which you currently rent?", ("Yes", "No"))
        inputs["moving_from_rent"] = moving_from_rent
        if moving_from_rent == "Yes":
            current_rent = st.text_input("What is the monthly rent paid?", value="0")
            inputs["current_rent"] = float(current_rent) if current_rent else 0.0
            annual_rent_increase = st.text_input("How much do you estimate your current rent will go up each year (in %)?", value="0")
            inputs["annual_rent_increase"] = float(annual_rent_increase) if annual_rent_increase else 0.0
        utilities_difference = st.text_input(
            "How much more do you expect to pay in utilities compared to your current residence? (Negative value if less, 0 if same)",
            value="0")
        inputs["utilities_difference"] = float(utilities_difference) if utilities_difference else 0.0

    # Check if the property is a condo
    is_condo = st.radio("Is the property a condo?", ("Yes", "No"))
    inputs["is_condo"] = is_condo
    if is_condo == "Yes":
        condo_fees = st.text_input("What are the monthly condo fees?", value="0")
        inputs["condo_fees"] = float(condo_fees) if condo_fees else 0.0
        condo_fee_annual_increase = st.text_input("How much do the condo fees increase each year (in %)?", value="0")
        inputs["condo_fee_annual_increase"] = float(condo_fee_annual_increase) if condo_fee_annual_increase else 0.0

    # Check if user is getting help from someone monthly to pay for their mortgage
    if_help = st.radio("Are you getting assistance from someone each month (renting a room, from parents, a partner, etc)?", ("Yes", "No"))
    inputs["help"] = if_help
    if if_help == "Yes":
        monthly_help = st.text_input("How much are you getting each month?", value="0")
        inputs["monthly_help"] = float(monthly_help) if monthly_help else 0.0

    interest_rate = st.text_input("Interest rate of your loan (in %)", value="0")
    inputs["interest_rate"] = float(interest_rate) if interest_rate else 0.0

    house_price = st.text_input("House price", value="0")
    inputs["house_price"] = float(house_price) if house_price else 0.0

    down_payment_percentage = st.text_input("Down payment (as a % of house price)", value="0")
    inputs["down_payment_percentage"] = float(down_payment_percentage) if down_payment_percentage else 0.0

    appreciation_rate = st.text_input("Expected annual appreciation rate of your new property (in %)", value="0")
    inputs["appreciation_rate"] = float(appreciation_rate) if appreciation_rate else 0.0

    amortization_period = st.text_input("What is the amortization period (in years)?", value="0")
    inputs["amortization_period"] = int(amortization_period) if amortization_period else 0

    property_taxes = st.text_input("What are the annual property taxes?", value="0")
    inputs["property_taxes"] = float(property_taxes) if property_taxes else 0.0

    annual_property_tax_increase = st.text_input("How much do you estimate your property tax will go up each year (in %)?", value="0")
    inputs["annual_property_tax_increase"] = float(annual_property_tax_increase) if annual_property_tax_increase else 0.0

    real_estate_agent_fee = st.text_input("What is your real estate agent fee when you sell (in %)?", value="0")
    inputs["real_estate_agent_fee"] = float(real_estate_agent_fee) if real_estate_agent_fee else 0.0

    land_transfer_tax = st.text_input("What is the land transfer tax when you buy your new property?", value="0")
    inputs["land_transfer_tax"] = float(land_transfer_tax) if land_transfer_tax else 0.0

    maintenance_budget = st.text_input("What is your expected monthly maintenance fee budget?", value="0")
    inputs["monthly_maintenance"] = float(maintenance_budget) if maintenance_budget else 0.0

    is_taxed = st.radio("Will there be a tax on the sale of the property?", ("Yes", "No"))
    inputs["is_taxed"] = is_taxed
    if is_taxed == "Yes":
        tax_percentage = st.text_input("What is the tax percentage on the capital gain?", value="0")
        inputs["tax_percentage"] = float(tax_percentage) if tax_percentage else 0.0
        factor = st.text_input("What is the factor at which the capital gain is taxed (e.g., 0.5 for 50% taxable)?", value="0")
        inputs["factor"] = float(factor) if factor else 0.0

    return inputs

def are_inputs_valid(inputs):
    """
    Validates all user inputs to ensure they meet the required criteria for property profit calculations.
    
    This function performs comprehensive validation on all input parameters, checking for:
    - Required field presence and non-empty values
    - Numeric ranges appropriate for each parameter type
    - Conditional validation based on property type and user scenarios
    - Logical consistency between related parameters
    
    The function uses debug print statements to help identify validation failures,
    which can be useful for troubleshooting input issues.
    
    Args:
        inputs (dict): Dictionary containing all user inputs from the web form
        
    Returns:
        bool: True if all inputs are valid and within acceptable ranges, False otherwise
        
    Validation Rules:
        - Interest rate: 0-20%
        - House price: $50,000-$50,000,000
        - Down payment: 5-75% of house price
        - Appreciation rate: 0-10% annually
        - Amortization period: 1-30 years
        - Property taxes: $0-$50,000 annually
        - Monthly maintenance: $100-$5,000
        - Land transfer tax: $0-$50,000
        - Real estate agent fee: 0-10%
        - Additional scenario-specific validations for rental properties, condos, etc.
    """
    # Check all required fields and print their values for debugging
    #print("Debug: Checking input values:", inputs)

    required_keys = [
        "interest_rate", "house_price", "down_payment_percentage", "appreciation_rate", "amortization_period", "property_taxes",
        "monthly_maintenance", "land_transfer_tax", "real_estate_agent_fee", "annual_property_tax_increase"
    ]
    # TODO: nothing recognizes a 0 input, this is an issue for parameters where 0 is valid...maybe an issue with the way it's initially defined
    # TODO: make these print statements st.write statements
    return_val = True
    # Check if any required field is missing or empty
    for key in required_keys:
        value = inputs.get(key)
        if value is None or value == "":
            print(f"Debug: Missing or empty input for {key}")
            return_val = False

    if not inputs.get("interest_rate") or (inputs.get("interest_rate") <= 0 or inputs.get("interest_rate") > 20):
        print("Debug: Missing interest_rate, or not above 0 and below or equal to 20")
        return_val = False

    if not inputs.get("house_price") or (inputs.get("house_price") < 50000 or inputs.get("house_price") > 50000000):
        print("Debug: Missing house price, or it's not between 50000 and 50000000")
        return_val = False

    if not inputs.get("down_payment_percentage") or (inputs.get("down_payment_percentage") < 5 or inputs.get("down_payment_percentage") > 75):
        print("Debug: Missing down payment %, or not above between 5 and 75%")
        return_val = False

    if not inputs.get("appreciation_rate") or (inputs.get("appreciation_rate") <= 0 or inputs.get("appreciation_rate") > 10):
        print("Debug: Missing appreciation rate, or not above 0 and below or equal to 10")
        return_val = False

    if not inputs.get("amortization_period") or (inputs.get("amortization_period") < 1 or inputs.get("amortization_period") > 30):
        print("Debug: Missing amortization period, or not between 1 and 30 years")
        return_val = False

    if not inputs.get("property_taxes") or (inputs.get("property_taxes") < 0 or inputs.get("property_taxes") > 50000):
        print("Debug: Missing property taxes, or not between 0 and 50000/year")
        return_val = False

    if not inputs.get("monthly_maintenance") or (inputs.get("monthly_maintenance") < 100 or inputs.get("monthly_maintenance") > 5000):
        print("Debug: Missing monthly maintenance, or not between 100 and 5000/month")
        return_val = False

    if not inputs.get("land_transfer_tax") or (inputs.get("land_transfer_tax") < 0 or inputs.get("land_transfer_tax") > 50000):
        print("Debug: Missing land transfer tax, or it's negative or less than or more than 50000")
        return_val = False

    if not inputs.get("real_estate_agent_fee") or (inputs.get("real_estate_agent_fee") < 0 or inputs.get("real_estate_agent_fee") > 10):
        print("Debug: Missing real estate agent fee, or it's not between 0 and 10%")
        return_val = False

    if not inputs.get("annual_property_tax_increase") or (inputs.get("annual_property_tax_increase") < 0 or inputs.get("annual_property_tax_increase") > 10):
        print("Debug: Missing annual property tax increase, or not above 0 and below or equal to 10")
        return_val = False

    # Check if rental income is expected and if the value is provided
    if inputs.get("expected_rental_income") == "Yes":
        if not inputs.get("rental_income_amount") or (inputs.get("rental_income_amount")<=500 or inputs.get("rental_income_amount")>=50000):
            print("Debug: Missing rental income amount, or not between 500 and 500000")
            return_val = False
        if not inputs.get("occupancy_rate") or (inputs.get("occupancy_rate")<50 or inputs.get("occupancy_rate")>95):
            print("Debug: Missing rental income property occupancy rate, or not between 50 and 95%")
            return_val = False
        if not inputs.get("rental_income_annual_increase") or (inputs.get("rental_income_annual_increase")<=0 or inputs.get("rental_income_annual_increase")>20):
            print("Debug: Missing rental income annual increase, or it's below/equal to 0 or >20%")
            return_val = False
        if inputs.get("is_property_managed") == "Yes" and (not inputs.get("property_management_fees") or (inputs.get("property_management_fees")<1 or inputs.get("property_management_fees")>20)):
            print("Debug: Missing property management fees, or the fees are not in between 1 and 20%")
            return_val = False
        if not inputs.get("total_utilities_not_paid_by_occupant") or (inputs.get("total_utilities_not_paid_by_occupant") < 50 or inputs.get("total_utilities_not_paid_by_occupant") > 2500):
            print("Debug: Missing utilities not paid by the renter, or not between 50 and 2500")
            return_val = False


    # Check if the property is a condo and if the condo fees are provided
    if inputs.get("is_condo") == "Yes":
        if not inputs.get("condo_fees") or (inputs.get("condo_fees")<100 or inputs.get("condo_fees")>3500):
            print("Debug: Missing condo fees, or it's not between 100 and 3500")
            return_val = False
        if not inputs.get("condo_fee_annual_increase") or (inputs.get("condo_fee_annual_increase")<=0 or inputs.get("condo_fee_annual_increase")>10):
            print("Debug: Missing condo fee annual increase, or less than/equal 0 or >10%")
            return_val = False

    # Check if moving from rent and if the monthly rent amount is provided
    if inputs.get("moving_from_rent") == "Yes":
        if not inputs.get("current_rent") or (inputs.get("current_rent")<200 or inputs.get("current_rent")>5000):
            print("Debug: Missing monthly rent, or not between 200 and 5000")
            return_val = False
        if not inputs.get("annual_rent_increase") or (inputs.get("annual_rent_increase")<=0 or inputs.get("annual_rent_increase")>5000):
            print("Debug: Missing annual rent increase, or not above 0 or less than or equal to 5000")
            return_val = False
        if not inputs.get("utilities_difference") or (inputs.get("utilities_difference") < -2500 or inputs.get("utilities_difference") > 2500):
            print("Debug: Missing utilities difference, or between -2500 and 2500")
            return_val = False

    # Check if there is help from family, partner, etc
    if inputs.get("help") == "Yes":
        if not inputs.get("monthly_help") or (inputs.get("monthly_help")<50 or inputs.get("monthly_help")>20000):
            print("Debug: Missing monthly help, or not between allowable range of 50 and 20000")
            return_val = False

    if inputs.get("is_taxed") == "Yes":
        if not inputs.get("tax_percentage") or (inputs.get("tax_percentage") <= 0 or inputs.get("tax_percentage") >= 100):
            print("Debug: Invalid tax percentage, must be greater than 0 and less than 100")
            return_val = False
        if not inputs.get("factor") or (inputs.get("factor") <= 0 or inputs.get("factor") > 1):
            print("Debug: Invalid factor, must be greater than 0 and less than or equal to 1")
            return_val = False

    print("\n\n\n\n\n")

    if return_val: print("Debug: All inputs are valid")
    return return_val

def calculate_mortgage_payment(principal, annual_interest_rate, years):
    """
    Calculates the fixed monthly mortgage payment using the standard amortization formula.
    
    This function implements the standard mortgage payment calculation formula that determines
    the fixed monthly payment amount required to fully amortize a loan over a specified period.
    The calculation assumes equal monthly payments throughout the loan term.
    
    Args:
        principal (float): The loan amount (house price minus down payment)
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
    opportunity_cost_base = inputs.get("house_price") * down_payment_multiplier
    opportunity_cost = opportunity_cost_base #opportunity cost accounting for money lost by not investing the down payment in the S&P500
    sp500_return = 1.0057 #assuming historical rate of 0.57% per month, using this to model opportunity cost lost from down payment
    principal = inputs.get("house_price") * (1-down_payment_multiplier)
    monthly_payment = calculate_mortgage_payment(principal, inputs.get("interest_rate"), inputs.get("amortization_period"))
    outstanding_balance = principal
    annual_property_tax_base = inputs.get("property_taxes")
    annual_property_tax_increase = 1 + inputs.get("annual_property_tax_increase") * 0.01
    land_transfer_tax = inputs.get("land_transfer_tax")
    agent_fee_multiplier = 1 - (inputs.get("real_estate_agent_fee")*0.01)
    current_house_value = inputs.get("house_price") #will increment based on appreciation rate monthly
    appreciation_rate = (1+(inputs.get("appreciation_rate")*0.01))**(1/12) #converting user input to increment on a monthly equivalent basis

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

        opportunity_cost *= sp500_return
        interest_payment = calculate_interest_payment(outstanding_balance, inputs.get("interest_rate"))
        principal_payment = monthly_payment - interest_payment
        outstanding_balance -= principal_payment
        total_interest_paid += interest_payment
        total_property_management_fees += property_management_fee_base
        total_property_tax_paid += annual_property_tax_base/12 #converting annual property tax to monthly
        total_extra_monthly_expenses_paid += extra_monthly_expenses
        total_utilities_not_paid_by_renter += utilities_not_paid_by_occupant
        total_maintenance_fees_paid += inputs.get("monthly_maintenance")
        if inputs.get("help") == "Yes": total_help += inputs.get("monthly_help")
        current_house_value *= appreciation_rate
        if inputs.get("is_taxed") == "Yes":
            capital_gain = current_house_value - inputs["house_price"]
            capital_gains_tax = capital_gain * inputs["factor"] * (inputs["tax_percentage"] / 100)
        else:
            capital_gains_tax = 0
        profit_if_sold = ((current_house_value * agent_fee_multiplier) - land_transfer_tax - total_interest_paid -
                          opportunity_cost - outstanding_balance - total_extra_monthly_expenses_paid -
                          total_maintenance_fees_paid - total_utilities_not_paid_by_renter - capital_gains_tax)
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
            st.write(f"With no help, rental income, or saving rent from moving, you are profitable after {month} months")
        if inputs.get("moving_from_rent")=="Yes" and not is_profitable_saving_rent and profit_if_sold_with_rent_saved > 0:
            is_profitable_saving_rent = True
            st.write(f"With only saving ${inputs.get("current_rent"):.2f}/month from your previous rental, you are profitable after {month} months")
        if inputs.get("help")=="Yes" and not is_profitable_with_help and profit_if_sold_with_help > 0:
            is_profitable_with_help = True
            st.write(f"With getting ${inputs.get("monthly_help"):.2f} in help/month, you are profitable after {month} months")
        if inputs.get("moving_from_rent")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_saverent_help and profit_if_sold_rentsaved_help > 0:
            is_profitable_saverent_help = True
            st.write(f"With saving ${inputs.get("current_rent"):.2f}/month from your previous rental and getting {inputs.get("monthly_help"):.2f} in help/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and not is_profitable_renting and profit_if_sold_with_rental_income > 0:
            is_profitable_renting = True
            st.write(f"With renting your new property at ${inputs.get("rental_income"):.2f}/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_renting_help and profit_if_sold_rentalincome_help > 0:
            is_profitable_renting_help = True
            st.write(f"With renting your new property at ${inputs.get("rental_income"):.2f}/month and getting {inputs.get("monthly_help"):.2f} of help/month, you are profitable after {month} months")

        if inputs.get("is_condo") == "Yes":
            schedule.append((month, monthly_payment, interest_payment, principal_payment, round(outstanding_balance,2),
                             round((opportunity_cost-opportunity_cost_base),2), round(total_property_tax_paid,2),
                             round(current_house_value,2), total_extra_monthly_expenses_paid, total_maintenance_fees_paid,
                             round(total_condo_fees_paid,2), round(profit_if_sold,2), total_help, round(profit_if_sold_with_help,2),
                             round(total_rent_saved,2), round(total_rental_income,2), round(profit_if_sold_with_rent_saved,2),
                             round(profit_if_sold_rentsaved_help,2), round(profit_if_sold_with_rental_income,2),
                             round(profit_if_sold_rentalincome_help,2)))
        else:
            schedule.append((month, monthly_payment, interest_payment, principal_payment, round(outstanding_balance,2),
                             round((opportunity_cost-opportunity_cost_base),2), round(total_property_tax_paid,2),
                             round(current_house_value,2), total_extra_monthly_expenses_paid, total_maintenance_fees_paid,
                             round(profit_if_sold,2), total_help, round(profit_if_sold_with_help,2),
                             round(total_rent_saved,2), round(total_rental_income,2), round(profit_if_sold_with_rent_saved,2),
                             round(profit_if_sold_rentsaved_help,2), round(profit_if_sold_with_rental_income,2),
                             round(profit_if_sold_rentalincome_help,2)))

            # Calculate if the property is cash flowing (for rental properties)
            if not is_cash_flowing and inputs.get("primary_residence") == "No" and inputs.get("rental_income_expected") == "Yes":
                monthly_cash_flow = (rental_income_base * occupancy_rate) - monthly_payment - (annual_property_tax_base / 12) - inputs.get("monthly_maintenance") - condo_fee_base - property_management_fee_base - utilities_not_paid_by_occupant
                if inputs.get("help") == "Yes":
                    monthly_cash_flow += inputs.get("monthly_help")
                if monthly_cash_flow > 0:
                    is_cash_flowing = True
                    st.write(f"The property is cash flowing with an initial monthly cash flow of ${monthly_cash_flow:.2f} in month {month}")
                elif month == inputs.get("amortization_period") * 12:
                    st.write(f"The property is not cash flowing, with an initial monthly loss of ${-monthly_cash_flow:.2f}")

    return schedule

def generate_monthly_property_profit_spreadsheet(inputs):
    """
    Generates and provides a downloadable Excel spreadsheet containing the complete amortization schedule and profit analysis.
    
    This function creates a comprehensive Excel file with month-by-month financial projections for the property investment.
    The spreadsheet includes all calculated values from the amortization schedule, formatted for easy analysis and
    presentation. The function handles different column structures for condo vs non-condo properties and provides
    automatic column width adjustment for optimal readability.
    
    Args:
        inputs (dict): Validated user inputs containing all property and financial parameters
        
    Returns:
        None: The function generates a Streamlit download button for the Excel file
        
    Excel File Contents:
        - Monthly mortgage payment breakdown (principal/interest)
        - Property value appreciation over time
        - Cumulative costs (taxes, maintenance, fees, opportunity cost)
        - Multiple profit scenarios (base, with help, with rental income, etc.)
        - Properly formatted sheet names based on property parameters
        - Auto-sized columns for optimal viewing
        
    File Naming:
        Sheet name format: ${house_price}_{interest_rate}%_{amortization_period}years
        Download filename: amortization_schedule.xlsx
    """
    house_value = inputs.get("house_price")
    annual_interest_rate = inputs.get("interest_rate")
    amortization_period = inputs.get("amortization_period")

    to_download = BytesIO()

    #ignore to_download warning
    with pd.ExcelWriter(to_download, engine='xlsxwriter') as writer:
        amortization_schedule = calculate_amortization_schedule(inputs)
        if inputs.get("is_condo") == "Yes":
            # Convert to DataFrame
            df = pd.DataFrame(amortization_schedule,
                              columns=['Month After Purchase', 'Monthly Payment', 'Interest Payment', 'Principal Payment',
                                       'Remaining Balance', 'Opportunity Cost', 'Property Tax', 'House Value',
                                       'Expenses Compared to Last Home', 'Maintenance Fees', 'Condo Fees',
                                       'Profit', 'Help', 'Profit with Help', 'Rent Saved', 'Rental Income',
                                       'Profit if Saving Rent', 'Profit with Rent Saved&Help', 'Profit with Rental Income',
                                       'Profit with Rental Income&Help'])
        else:
            # Convert to DataFrame
            df = pd.DataFrame(amortization_schedule,
                              columns=['Month After Purchase', 'Monthly Payment', 'Interest Payment', 'Principal Payment',
                                       'Remaining Balance', 'Opportunity Cost', 'Property Tax', 'House Value',
                                       'Expenses Compared to Last Home', 'Maintenance Fees', 'Profit', 'Help',
                                       'Profit with Help', 'Rent Saved', 'Rental Income', 'Profit if Saving Rent',
                                       'Profit with Rent Saved&Help', 'Profit with Rental Income',
                                       'Profit with Rental Income&Help'])
        # Save to Excel
        sheet_name = f'${house_value}_{annual_interest_rate}%_{amortization_period}years'
        df.to_excel(writer, sheet_name, index=False)

        # Access the worksheet object to set column width
        worksheet = writer.sheets[sheet_name]
        # Set column widths based on content
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(),  # Length of largest item
                          len(col)) + 1 # Length of column name/header
            worksheet.set_column(idx, idx, max_len)

    # Adding button to download the generated spreadsheet
    to_download.seek(0)
    st.write("Click the button below to download the spreadsheet:")
    st.download_button(
        label="Download Spreadsheet",
        data=to_download,
        file_name="amortization_schedule.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def main():
    """
    Main application entry point that orchestrates the Streamlit web application flow.
    
    This function serves as the primary controller for the property profit calculator application.
    It manages the overall user experience by coordinating input collection, validation,
    and result generation. The function implements a typical web application pattern:
    form display -> input validation -> processing -> result presentation.
    
    Application Flow:
        1. Configure Streamlit page settings (title, layout)
        2. Initialize and display the input form via initialize_webpage()
        3. Validate all user inputs using are_inputs_valid()
        4. Present a calculation button to the user
        5. Process calculations and generate downloadable results if inputs are valid
        6. Display appropriate success/error messages based on validation results
        
    Session State Management:
        - Maintains input validation state across Streamlit reruns
        - Ensures consistent user experience during form interaction
        
    Error Handling:
        - Provides clear feedback for invalid inputs
        - Prevents calculation execution with incomplete/invalid data
        - Guides users to correct input issues before proceeding
    """
    # Set page configuration
    st.set_page_config(
        page_title="Property Profit Calculator",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🏠 Property Profit Calculator")
    st.markdown("### Calculate month by month profit for your property investment")
    st.markdown("""
    This tool helps you analyze the profitability of your property purchase by considering:
    - Mortgage payments and amortization
    - Property appreciation
    - Rental income (if applicable)
    - Various expenses and scenarios
    """)
    
    inputs = initialize_webpage()

    # Initialize session state for input validation
    if "inputs_valid" not in st.session_state:
        st.session_state.inputs_valid = False

    # Validate inputs and update session state
    st.session_state.inputs_valid = are_inputs_valid(inputs)

    # Display a submit button
    calculate_button = st.button("Calculate Profit if Sold on Monthly Basis")

    # Only call the calculation function if inputs are valid and the button is clicked
    if calculate_button:
        if st.session_state.inputs_valid:
            st.success("All inputs are valid. Performing calculations...")
            generate_monthly_property_profit_spreadsheet(inputs)
        else:
            st.error("Please fill out all required fields correctly before calculating.")
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ About This Tool")
    
    with st.expander("How the Calculations Work"):
        st.markdown("""
        **Mortgage Amortization:**
        - Uses standard amortization formula for monthly payments
        - Tracks principal and interest portions each month
        - Accounts for property appreciation and opportunity costs
        
        **Profit Scenarios:**
        - Calculates multiple scenarios including rental income, help, and rent savings
        - Includes taxes, maintenance, and other expenses
        """)
    
    with st.expander("Important Assumptions"):
        st.markdown("""
        - S&P 500 return of 0.57% monthly for opportunity cost (based on 8% historical annual gain)
        - Annual increases applied monthly where appropriate
        """)
    
    with st.expander("Disclaimers"):
        st.markdown("""
        **⚠️ Important Notes:**
        - This is for informational purposes only
        - Actual results may vary based on market conditions
        - Consult a financial advisor for personalized advice
        """)

    # PayPal donation button at the bottom of the page
    st.markdown("---")  # Add a separator line
    st.markdown("### Support This Tool")
    st.markdown("If you find this property profit calculator helpful, consider supporting the development and hosting costs:")
    
    # PayPal donation form
    paypal_html = """
    <form action="https://www.paypal.com/donate" method="post" target="_top">
    <input type="hidden" name="business" value="ZF94BFC7ZMLNG" />
    <input type="hidden" name="no_recurring" value="0" />
    <input type="hidden" name="item_name" value="Support this page to help pay for hosting fees." />
    <input type="hidden" name="currency_code" value="CAD" />
    <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
    <img alt="" border="0" src="https://www.paypal.com/en_CA/i/scr/pixel.gif" width="1" height="1" />
    </form>
    """
    
    st.markdown(paypal_html, unsafe_allow_html=True)
    st.markdown("*Thank you for your support!*")

if __name__ == '__main__':
    main()
