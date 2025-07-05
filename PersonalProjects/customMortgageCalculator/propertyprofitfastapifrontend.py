#!/bin/env python3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from propertyprofitbackend import calculate_amortization_schedule, generate_monthly_property_profit_spreadsheet

#TODO: add ad functionality
#TODO: make a website for this instead of using localhost
#TODO: update such that the output spreadsheet has the correct number of columns for every single type of situation (right now just printing 0s for columns that aren't relevant)
#TODO: Convert this implementation from streamlit to fastapi

def initialize_webpage(col2):
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

    primary_residence = st.radio("Is this property going to be your primary residence?", ("Yes", "No"))
    inputs["primary_residence"] = primary_residence
    if primary_residence == "No":
        rental_income_expected = st.radio("Is there expected rental income?", ("Yes", "No"))
        inputs["rental_income_expected"] = rental_income_expected
        if rental_income_expected == "Yes":
            rental_income = col2.number_input(
                "How much rental income is expected per month?",
                min_value=500.0,
                max_value=50000.0,
                value=2000.0,
                help="Expected monthly rental income in Canadian dollars"
            )
            inputs["rental_income"] = rental_income

            rental_income_annual_increase = col2.number_input(
                "How much will you increase the rent for your new property each year (in %)?",
                min_value=0.01,
                max_value=20.0,
                value=2.5,
                help="Expected annual percentage increase in rent"
            )
            inputs["rental_income_annual_increase"] = rental_income_annual_increase

            occupancy_rate = col2.number_input(
                "What is the occupancy rate of your new rental (in %, 95 is the max allowed)?",
                min_value=50.0,
                max_value=95.0,
                value=90.0,
                help="Expected occupancy rate of the rental unit"
            )
            inputs["occupancy_rate"] = occupancy_rate

            is_property_managed = st.radio("Are you going to pay someone to manage your property for you?", ("Yes", "No"))
            inputs["is_property_managed"] = is_property_managed
            if is_property_managed == "Yes":
                property_management_fees = col2.number_input(
                    "How much are you going to pay your property manager (as a % of your rental income, standard is 10)?",
                    min_value=1.0,
                    max_value=20.0,
                    value=10.0,
                    help="Percentage of rental income paid to the property manager"
                )
                inputs["property_management_fees"] = property_management_fees

            are_utilities_paid_by_renter = st.radio("Are there utilities that your renter is not paying for?",("Yes", "No"))
            inputs["are_utilities_paid_by_renter"] = are_utilities_paid_by_renter
            if are_utilities_paid_by_renter == "Yes":
                total_utilities_not_paid_by_occupant = col2.number_input(
                    "How much are you paying in utilities per month that your renter is not responsible for?",
                    min_value=50.0,
                    max_value=2500.0,
                    value=100.0
                )
                inputs["total_utilities_not_paid_by_occupant"] = total_utilities_not_paid_by_occupant

    else:
        moving_from_rent = st.radio("Are you moving from a property which you currently rent?", ("Yes", "No"), index=1)
        inputs["moving_from_rent"] = moving_from_rent
        if moving_from_rent == "Yes":
            current_rent = col2.number_input(
                "What is the monthly rent paid?",
                min_value=200.0,
                max_value=5000.0,
                value=2000.0
            )
            inputs["current_rent"] = current_rent

            annual_rent_increase = col2.number_input(
                "How much do you estimate your current rent will go up each year (in %)?",
                min_value=0.01,
                max_value=5000.0,
                value=2.5
            )
            inputs["annual_rent_increase"] = annual_rent_increase

        utilities_difference = col2.number_input(
            "How much more do you expect to pay in utilities/month compared to your current residence? (Negative value if less, 0 if same)",
            min_value=-2500.0,
            max_value=2500.0,
            value=0.0
        )
        inputs["utilities_difference"] = utilities_difference

    is_condo = st.radio("Is the property a condo?", ("Yes", "No"), index=1)
    inputs["is_condo"] = is_condo
    if is_condo == "Yes":
        condo_fees = col2.number_input(
            "What are the monthly condo fees?",
            min_value=100.0,
            max_value=3500.0,
            value=400.0
        )
        inputs["condo_fees"] = condo_fees

        condo_fee_annual_increase = col2.number_input(
            "How much do the condo fees increase each year (in %)?",
            min_value=0.01,
            max_value=10.0,
            value=2.0
        )
        inputs["condo_fee_annual_increase"] = condo_fee_annual_increase

    if_help = st.radio("Are you getting assistance from someone each month (renting a room, from parents, a partner, etc)?", ("Yes", "No"), index=1)
    inputs["help"] = if_help
    if if_help == "Yes":
        monthly_help = col2.number_input(
            "How much are you getting each month?",
            min_value=50.0,
            max_value=20000.0,
            value=500.0
        )
        inputs["monthly_help"] = monthly_help

    property_price = col2.number_input(
        "Property price",
        min_value=50000.0,
        max_value=50000000.0,
        value=500000.0
    )
    inputs["property_price"] = property_price

    down_payment_percentage = col2.number_input(
        "Down payment (as a % of property price)",
        min_value=5.0,
        max_value=75.0,
        value=20.0
    )
    inputs["down_payment_percentage"] = down_payment_percentage

    appreciation_rate = col2.number_input(
        "Expected annual appreciation rate of your new property (in %)",
        min_value=0.01,
        max_value=10.0,
        value=2.0
    )
    inputs["appreciation_rate"] = appreciation_rate

    amortization_period = col2.number_input(
        "What is the amortization period (in years)?",
        min_value=1,
        max_value=30,
        value=25
    )
    inputs["amortization_period"] = amortization_period

    fixed_or_variable = st.radio(
        "Select Mortgage Type:",
        ["Fixed Rate", "Variable Rate"],
        index=0,
        horizontal=True
    )

    fixed_rate_mortgage = fixed_or_variable == "Fixed Rate"
    inputs["fixed_rate_mortgage"] = fixed_rate_mortgage

    if fixed_rate_mortgage: #checks if rate is fixed
        interest_rate = col2.number_input(
            "Interest rate of your loan (in %)",
            min_value=0.01,
            max_value=20.0,
            value=5.0
        )
        inputs["interest_rate"] = interest_rate
        #pass  # Interest rate input is already defined above
    else:
        # Variable rate mortgage options
        st.write("**Variable Rate Mortgage Configuration**")
        
        rate_structure_preset = st.selectbox(
            "Choose a common structure or create custom:",
            ["Custom", "5-year renewable terms", "3-year renewable terms", "1-year renewable terms"],
            help="Select a preset to auto-populate common mortgage renewal patterns"
        )
        inputs["rate_structure_preset"] = rate_structure_preset
        
        # Initialize rate periods based on preset or custom
        if rate_structure_preset == "5-year renewable terms":
            # Calculate how many 5-year periods fit, plus remainder
            full_periods = amortization_period // 5
            remainder = amortization_period % 5
            default_periods = []
            for i in range(full_periods):
                default_periods.append({"term_length": 5, "interest_rate": 5.0})
            if remainder > 0:
                default_periods.append({"term_length": remainder, "interest_rate": 5.0})
        elif rate_structure_preset == "3-year renewable terms":
            full_periods = amortization_period // 3
            remainder = amortization_period % 3
            default_periods = []
            for i in range(full_periods):
                default_periods.append({"term_length": 3, "interest_rate": 5.0})
            if remainder > 0:
                default_periods.append({"term_length": remainder, "interest_rate": 5.0})
        elif rate_structure_preset == "1-year renewable terms":
            default_periods = []
            for i in range(amortization_period):
                default_periods.append({"term_length": 1, "interest_rate": 5.0})
        else:  # Custom
            default_periods = [{"term_length": amortization_period, "interest_rate": 5.0}]
        
        # Store the number of periods in session state to maintain across reruns
        if f"num_rate_periods_{amortization_period}_{rate_structure_preset}" not in st.session_state:
            st.session_state[f"num_rate_periods_{amortization_period}_{rate_structure_preset}"] = len(default_periods)
        
        num_periods = st.session_state[f"num_rate_periods_{amortization_period}_{rate_structure_preset}"]
        
        # Collect rate periods
        rate_periods = []
        total_years = 0
        
        st.write("**Define Rate Periods:**")
        
        for i in range(num_periods):
            col_a, col_b = st.columns(2)
            
            with col_a:
                if i < len(default_periods):
                    default_term = default_periods[i]["term_length"]
                else:
                    default_term = max(1, amortization_period - total_years)
                    
                term_length = st.number_input(
                    f"Period {i+1} - Term Length (years)",
                    min_value=1,
                    max_value=amortization_period,
                    value=default_term,
                    key=f"term_length_{i}"
                )
            
            with col_b:
                if i < len(default_periods):
                    default_rate = default_periods[i]["interest_rate"]
                else:
                    default_rate = 5.0
                    
                interest_rate_period = st.number_input(
                    f"Period {i+1} - Interest Rate (%)",
                    min_value=0.01,
                    max_value=20.0,
                    value=default_rate,
                    key=f"interest_rate_{i}"
                )
            
            rate_periods.append({
                "term_length": term_length,
                "interest_rate": interest_rate_period
            })
            total_years += term_length
        
        # Show running total and validation
        remaining_years = amortization_period - total_years
        if remaining_years > 0:
            st.info(f"⚠️ Remaining years to define: {remaining_years}")
        elif remaining_years < 0:
            st.error(f"❌ Total terms exceed amortization by {abs(remaining_years)} years")
        else:
            st.success(f"✅ All {amortization_period} years accounted for!")
        
        # Buttons to add/remove periods (only for custom)
        if rate_structure_preset == "Custom":
            col_add, col_remove = st.columns(2)
            with col_add:
                if st.button("➕ Add Rate Period"):
                    st.session_state[f"num_rate_periods_{amortization_period}_{rate_structure_preset}"] += 1
                    st.rerun()
            
            with col_remove:
                if st.button("➖ Remove Last Period") and num_periods > 1:
                    st.session_state[f"num_rate_periods_{amortization_period}_{rate_structure_preset}"] -= 1
                    st.rerun()
        
        inputs["rate_periods"] = rate_periods
        inputs["total_rate_period_years"] = total_years

    property_taxes = col2.number_input(
        "What are the annual property taxes?",
        min_value=0.0,
        max_value=50000.0,
        value=5000.0
    )
    inputs["property_taxes"] = property_taxes

    annual_property_tax_increase = col2.number_input(
        "How much do you estimate your property tax will go up each year (in %)?",
        min_value=0.01,
        max_value=10.0,
        value=2.0
    )
    inputs["annual_property_tax_increase"] = annual_property_tax_increase

    maintenance_budget = col2.number_input(
        "What is your expected monthly maintenance fee budget?",
        min_value=100.0,
        max_value=5000.0,
        value=300.0
    )
    inputs["monthly_maintenance"] = maintenance_budget

    real_estate_agent_fee = col2.number_input(
        "What is your real estate agent fee when you sell (in %)?",
        min_value=0.0,
        max_value=10.0,
        value=5.5
    )
    inputs["real_estate_agent_fee"] = real_estate_agent_fee

    land_transfer_tax = col2.number_input(
        "What is the land transfer tax when you buy your new property?",
        min_value=0.0,
        max_value=50000.0,
        value=8000.0
    )
    inputs["land_transfer_tax"] = land_transfer_tax

    legal_fees = col2.number_input(
        "What are the total legal fees you will pay when you BUY AND SELL your new property?",
        min_value=0.0,
        max_value=100000.0,
        value=5000.0
    )
    inputs["legal_fees"] = legal_fees

    breaking_mortgage_early_fee = col2.number_input(
        "What is the fee for breaking your mortgage loan early to sell before the amortization period is over (if none set to 0)?",
        min_value=0.0,
        max_value=0.5*(float(property_price-(down_payment_percentage*0.01*property_price))),
        value=0.0
    )
    inputs["breaking_mortgage_early_fee"] = breaking_mortgage_early_fee
    
    is_taxed = st.radio("Will there be a tax on the sale of the property?", ("Yes", "No"), index=1)
    inputs["is_taxed"] = is_taxed
    if is_taxed == "Yes":
        tax_percentage = col2.number_input(
            "What is the tax percentage on the capital gain?",
            min_value=0.01,
            max_value=99.99,
            value=35.0
        )
        inputs["tax_percentage"] = tax_percentage

        factor = col2.number_input(
            "What is the factor at which the capital gain is taxed (e.g., 0.5 for 50% taxable)?",
            min_value=0.01,
            max_value=1.0,
            value=1.0
        )
        inputs["factor"] = factor

    return inputs

#TODO: when everything else is done, update this function to return false instead of setting a return_val to False and remove debug prints
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
        - Property price: $50,000-$50,000,000
        - Down payment: 5-75% of property price
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
        "property_price", "down_payment_percentage", "appreciation_rate", "amortization_period", "property_taxes",
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

    # Validate interest rate for fixed rate mortgages
    if inputs.get("fixed_rate_mortgage", True):
        if not inputs.get("interest_rate") or (inputs.get("interest_rate") <= 0 or inputs.get("interest_rate") > 20):
            print("Debug: Missing interest_rate, or not above 0 and below or equal to 20")
            return_val = False
    else:
        # Validate variable rate mortgage inputs
        if not inputs.get("rate_periods"):
            print("Debug: Missing rate periods for variable rate mortgage")
            return_val = False
        else:
            rate_periods = inputs.get("rate_periods", [])
            total_years = inputs.get("total_rate_period_years", 0)
            amortization_period = inputs.get("amortization_period", 0)
            
            # Check if total years match amortization period
            if total_years != amortization_period:
                print(f"Debug: Rate periods total ({total_years}) doesn't match amortization period ({amortization_period})")
                return_val = False
            
            # Validate each rate period
            for i, period in enumerate(rate_periods):
                term_length = period.get("term_length", 0)
                interest_rate = period.get("interest_rate", 0)
                
                if term_length <= 0 or term_length > amortization_period:
                    print(f"Debug: Invalid term length for period {i+1}: {term_length}")
                    return_val = False
                
                if interest_rate <= 0 or interest_rate > 20:
                    print(f"Debug: Invalid interest rate for period {i+1}: {interest_rate}")
                    return_val = False

    if inputs.get("property_price") is None or (inputs.get("property_price") < 50000 or inputs.get("property_price") > 50000000):
        print("Debug: Missing property price, or it's not between 50000 and 50000000")
        return_val = False

    if inputs.get("down_payment_percentage") is None or (inputs.get("down_payment_percentage") < 5 or inputs.get("down_payment_percentage") > 75):
        print("Debug: Missing down payment %, or not above between 5 and 75%")
        return_val = False

    if inputs.get("appreciation_rate") is None or (inputs.get("appreciation_rate") <= 0 or inputs.get("appreciation_rate") > 10):
        print("Debug: Missing appreciation rate, or not above 0 and below or equal to 10")
        return_val = False

    if inputs.get("amortization_period") is None or (inputs.get("amortization_period") < 1 or inputs.get("amortization_period") > 30):
        print("Debug: Missing amortization period, or not between 1 and 30 years")
        return_val = False

    if inputs.get("property_taxes") is None or (inputs.get("property_taxes") < 0 or inputs.get("property_taxes") > 50000):
        print("Debug: Missing property taxes, or not between 0 and 50000/year")
        return_val = False

    if inputs.get("monthly_maintenance") is None or (inputs.get("monthly_maintenance") < 100 or inputs.get("monthly_maintenance") > 5000):
        print("Debug: Missing monthly maintenance, or not between 100 and 5000/month")
        return_val = False

    if inputs.get("land_transfer_tax") is None or (inputs.get("land_transfer_tax") < 0 or inputs.get("land_transfer_tax") > 50000):
        print("Debug: Missing land transfer tax, or it's negative or less than or more than 50000")
        return_val = False

    if inputs.get("real_estate_agent_fee") is None or (inputs.get("real_estate_agent_fee") < 0 or inputs.get("real_estate_agent_fee") > 10):
        print("Debug: Missing real estate agent fee, or it's not between 0 and 10%")
        return_val = False

    if inputs.get("annual_property_tax_increase") is None or (inputs.get("annual_property_tax_increase") < 0 or inputs.get("annual_property_tax_increase") > 10):
        print("Debug: Missing annual property tax increase, or not above 0 and below or equal to 10")
        return_val = False

    if inputs.get("legal_fees") is None or (inputs.get("legal_fees") < 0 or inputs.get("legal_fees") > 100000):
        print("Debug: Missing legal fees, or it's not between 0 and 100000")
        return_val = False

    if inputs.get("breaking_mortgage_early_fee") is None or (inputs.get("breaking_mortgage_early_fee") < 0.0 or inputs.get("breaking_mortgage_early_fee") > 0.5*(float(inputs.get("property_price")-(inputs.get("down_payment_percentage")*0.01*inputs.get("property_price"))))):
        print("Debug: Missing fee for breaking mortgage, or is <0 or >half of the loan value")
        return_val = False

    # Check if rental income is expected and if the value is provided
    if inputs.get("expected_rental_income") == "Yes":
        if inputs.get("rental_income_amount") is None or (inputs.get("rental_income_amount")<=500 or inputs.get("rental_income_amount")>=50000):
            print("Debug: Missing rental income amount, or not between 500 and 500000")
            return_val = False
        if inputs.get("occupancy_rate") is None or (inputs.get("occupancy_rate")<50 or inputs.get("occupancy_rate")>95):
            print("Debug: Missing rental income property occupancy rate, or not between 50 and 95%")
            return_val = False
        if inputs.get("rental_income_annual_increase") is None or (inputs.get("rental_income_annual_increase")<=0 or inputs.get("rental_income_annual_increase")>20):
            print("Debug: Missing rental income annual increase, or it's below/equal to 0 or >20%")
            return_val = False
        if inputs.get("is_property_managed") == "Yes" and (inputs.get("property_management_fees") is None or (inputs.get("property_management_fees")<1 or inputs.get("property_management_fees")>20)):
            print("Debug: Missing property management fees, or the fees are not in between 1 and 20%")
            return_val = False
        if inputs.get("total_utilities_not_paid_by_occupant") is None or (inputs.get("total_utilities_not_paid_by_occupant") < 50 or inputs.get("total_utilities_not_paid_by_occupant") > 2500):
            print("Debug: Missing utilities not paid by the renter, or not between 50 and 2500")
            return_val = False


    # Check if the property is a condo and if the condo fees are provided
    if inputs.get("is_condo") == "Yes":
        if inputs.get("condo_fees") is None or (inputs.get("condo_fees")<100 or inputs.get("condo_fees")>3500):
            print("Debug: Missing condo fees, or it's not between 100 and 3500")
            return_val = False
        if inputs.get("condo_fee_annual_increase") is None or (inputs.get("condo_fee_annual_increase")<=0 or inputs.get("condo_fee_annual_increase")>10):
            print("Debug: Missing condo fee annual increase, or less than/equal 0 or >10%")
            return_val = False

    # Check if moving from rent and if the monthly rent amount is provided
    if inputs.get("moving_from_rent") == "Yes":
        if inputs.get("current_rent") is None or (inputs.get("current_rent")<200 or inputs.get("current_rent")>5000):
            print("Debug: Missing monthly rent, or not between 200 and 5000")
            return_val = False
        if inputs.get("annual_rent_increase") is None or (inputs.get("annual_rent_increase")<=0 or inputs.get("annual_rent_increase")>5000):
            print("Debug: Missing annual rent increase, or not above 0 or less than or equal to 5000")
            return_val = False
        if inputs.get("utilities_difference") is None or (inputs.get("utilities_difference") < -2500 or inputs.get("utilities_difference") > 2500):
            if inputs.get("utilities_difference") != 0:
                print("Debug: Missing utilities difference, or between -2500 and 2500")
                return_val = False

    # Check if there is help from family, partner, etc
    if inputs.get("help") == "Yes":
        if inputs.get("monthly_help") is None or (inputs.get("monthly_help")<50 or inputs.get("monthly_help")>20000):
            print("Debug: Missing monthly help, or not between allowable range of 50 and 20000")
            return_val = False

    if inputs.get("is_taxed") == "Yes":
        if inputs.get("tax_percentage") is None or (inputs.get("tax_percentage") <= 0 or inputs.get("tax_percentage") >= 100):
            print("Debug: Invalid tax percentage, must be greater than 0 and less than 100")
            return_val = False
        if inputs.get("factor") is None or (inputs.get("factor") <= 0 or inputs.get("factor") > 1):
            print("Debug: Invalid factor, must be greater than 0 and less than or equal to 1")
            return_val = False

    print("-----------------------------")

    if return_val: print("Debug: All inputs are valid")
    return return_val

def create_visualization(amortization_schedule, variable_profit_columns):
    """
    Creates comprehensive matplotlib visualizations to display property profit calculation results.
    
    The visualizations are designed to clearly show month by month the profit if the property is sold
    without any extra monetary help and with monetary help from various sources including rental income,
    a partner, savings from moving from a rental, etc.
    
    Args:
        amortization_schedule (pandas.DataFrame): Results dataframe from profit calculations
            
    Returns:
        matplotlib.figure.Figure: Complete figure object with two subplots ready for display
    """
    fig, ((ax1, ax2)) = plt.subplots(2, 1, figsize=(18, 10))

    # Plot 1: Lifetime Loss by CPP Start Age
    ax1.plot(amortization_schedule['Month'], amortization_schedule['Profit'], linewidth=2)
    ax1.set_title('Profit if there is no rental income, help, or savings from renting before', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month property is sold')
    ax1.set_ylabel('Profit ($)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Lifetime Benefits Breakdown
    if len(variable_profit_columns) > 0:
        if 'Profit if Saving Rent' in variable_profit_columns:
            ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit if Saving Rent'], marker='^', label='Rent Saved', linewidth=2)
        if 'Profit with Help' in variable_profit_columns:
            ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit with Help'], marker='s', label='Help', linewidth=2)
        if 'Profit with Rent Saved&Help' in variable_profit_columns:
            ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit with Rent Saved&Help'], marker='x', label='Rent Saved+Help', linewidth=2)
        if 'Profit with Rental Income' in variable_profit_columns:
            ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit with Rental Income'], marker='*', label='Rental Income', linewidth=2)
        if 'Profit with Rent Saved&Help' in variable_profit_columns:
            ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit with Rent Saved&Help'], marker='D', label='Rental Income+Help', linewidth=2)
    ax2.plot(amortization_schedule['Month'], amortization_schedule['Profit'], marker='o', label='No modifiers', linewidth=2)
    ax2.set_title('Profit if there is...#TODO this plot should be based on different inputs, title and y axis should change based on this', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month property is sold')
    ax2.set_ylabel('Profit ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

    plt.tight_layout()
    return fig

def formatAndDisplayTable(amortization_schedule, variable_profit_columns):
    """
    Formats and displays a pandas DataFrame as a styled HTML table in Streamlit.
    
    This function converts a pandas DataFrame into a professionally styled HTML table
    that integrates seamlessly with the Streamlit interface. The function manually
    generates HTML to ensure consistent styling and proper formatting of financial
    data, providing better control over appearance than Streamlit's default table display.
    
    Args:
        amortization_schedule (pandas.DataFrame): DataFrame containing the optimization results to display.
                                     Expected to have formatted string values for financial columns
                                     and integer values for the month column.
                                     
    Returns:
        None: The function directly renders the HTML table in the Streamlit interface
              using st.markdown() with unsafe_allow_html=True
    """
    # Define always-included columns
    base_columns = ['Month', 'Loan Balance', 'Property Value', 'Profit']

    final_columns = base_columns + variable_profit_columns
    filtered_df = amortization_schedule[final_columns]

    headers = filtered_df.columns.tolist()
    rows = filtered_df.values.tolist()

    # Generate HTML table manually
    table_html = "<table><thead><tr>"
    for header in headers:
        table_html += f"<th>{header}</th>"
    table_html += "</tr></thead><tbody>"

    for row in rows:
        table_html += "<tr>"
        for i, item in enumerate(row):
            # Force 'month' (column index 0) to show as an integer
            if i == 0 and isinstance(item, (int, float)):
                table_html += f"<td>{int(item)}</td>"
            else:
                table_html += f"<td>{item}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table>"

    # Apply custom styling to make it look clean
    st.markdown("""
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #666;
            padding: 8px;
            text-align: right;
        }
        th {
            background-color: #333;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # Show the table
    st.markdown(table_html, unsafe_allow_html=True)

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

    # Create columns for layout: left ad, main content, right ad
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        if 'accepted_terms' not in st.session_state:
            st.session_state.accepted_terms = False

        if not st.session_state.accepted_terms:
            st.markdown("# Terms of Service")
            st.markdown("""
            **Disclaimer:** This tool is provided for informational purposes only and does not constitute financial advice. The calculations and outputs are based solely on the inputs provided by the user and may not account for all individual circumstances, changes in legislation, or other factors that could affect your financial situation.

            To obtain personalized financial advice, please consult a qualified financial advisor or professional. The author of this tool makes no representations or warranties about the accuracy, completeness, or suitability of the information provided. The outputs do not necessarily represent the views of the tool's author.

            By using this tool, you agree that the author is not liable for any decisions made based on the tool's output, and you assume all responsibility for any actions taken as a result of using this tool.
            """)
            if st.button("I Accept"):
                st.session_state.accepted_terms = True
                st.rerun()
            return

    # Left ad column
    with col1:
        st.header("Ads")
        # Placeholder for left ad
        # For real ads, replace with your ad code
        st.html("""
        <div style="background-color: #f0f0f0; padding: 10px; text-align: center;">
            <p>Finance Ad Placeholder</p>
            <p>Mortgage Rates Starting at 3.5%</p>
        </div>
        """)

    # Right ad column
    with col3:
        st.header("Ads")
        # Placeholder for right ad
        # For real ads, replace with your ad code
        st.html("""
        <div style="background-color: #f0f0f0; padding: 10px; text-align: center;">
            <p>Finance Ad Placeholder</p>
            <p>Get Your Mortgage Approved Today!</p>
        </div>
        """)

    # Main content in center column
    with col2:
        col2.title("🏠 Property Profit Calculator")
        col2.markdown("### Calculate month by month profit for your property investment")
        col2.markdown("""
        This tool helps you analyze the profitability of your property purchase by considering:
        - Mortgage payments and amortization
        - Property appreciation
        - Rental income (if applicable)
        - Various expenses and scenarios
        """)

        inputs = initialize_webpage(col2)
                                                                             
        # Initialize session state for input validation
        if "inputs_valid" not in st.session_state:
            st.session_state.inputs_valid = False

        # Validate inputs and update session state
        st.session_state.inputs_valid = are_inputs_valid(inputs)

        # Display a submit button
        calculate_button = col2.button("Calculate Profit if Sold on Monthly Basis")

        # Only call the calculation function if inputs are valid and the button is clicked
        if calculate_button:
            if st.session_state.inputs_valid:
                col2.success("All inputs are valid. Performing calculations...")
                
                # Get profitability messages and display them
                amortization_schedule, profitability_messages = calculate_amortization_schedule(inputs)

                # Store results in session state so they aren't removed after generating CSV
                st.session_state['amortization_schedule'] = amortization_schedule
                st.session_state['profitability_messages'] = profitability_messages
                st.session_state['inputs'] = inputs
            else:
                col2.error("Please fill out all required fields correctly before calculating.")

        if 'amortization_schedule' in st.session_state:
            amortization_schedule = st.session_state['amortization_schedule']
            profitability_messages = st.session_state['profitability_messages']
            inputs = st.session_state['inputs']

            # Filter profit columns where at least one value differs from 'Profit'
            profit_columns = [col for col in amortization_schedule.columns if col.startswith('Profit') and col != 'Profit']

            variable_profit_columns = [
                col for col in profit_columns
                if not (amortization_schedule[col] == amortization_schedule['Profit']).all()
            ]

            #displaying graphs and table
            st.subheader("📈 Profit over Time")
            fig = create_visualization(amortization_schedule, variable_profit_columns)
            st.pyplot(fig)
            
            formatAndDisplayTable(amortization_schedule, variable_profit_columns)

            for message in profitability_messages:
                col2.write(message)
            
            # Generate and provide download for spreadsheet
            spreadsheet_data = generate_monthly_property_profit_spreadsheet(amortization_schedule, inputs.get("property_price"), inputs.get("interest_rate"), inputs.get("amortization_period"))
            col2.write("Click the button below to download the spreadsheet:")
            col2.download_button(
                label="Download Spreadsheet",
                data=spreadsheet_data,
                file_name="amortization_schedule.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
        # Information section
        col2.markdown("---")
        col2.subheader("ℹ️ About This Tool")
 
        with col2.expander("How Property Investment Analysis Works"):
            col2.markdown("""
            **Mortgage Calculations:**
            - Uses standard amortization formula to calculate monthly payments
            - Tracks principal vs interest payments over time
            - Accounts for different down payment percentages and interest rates
            
            **Opportunity Cost Analysis:**
            - Compares property investment to S&P 500 historical returns (0.57% monthly)
            - Shows what your down payment could have earned in the stock market
            - Helps evaluate true investment performance
            
            **Multiple Scenarios:**
            - Primary residence vs rental property analysis
            - Accounts for rental income, property management, and vacancy rates
            - Includes assistance from family/partners and rent savings
            """)
        
        with col2.expander("Key Financial Assumptions"):
            col2.markdown("""
            **Property Appreciation:**
            - Annual appreciation rate is converted to monthly compounding
            - Property taxes and condo fees increase annually at specified rates
            - Rental income can increase annually to keep pace with market
            
            **Cost Considerations:**
            - Includes land transfer tax, real estate agent fees, and capital gains tax
            - Monthly maintenance budget and utility costs
            - Property management fees for rental properties
            - Opportunity cost of down payment investment
            """)
        
        with col2.expander("Important Disclaimers"):
            col2.markdown("""
            **⚠️ Important Notes:**
            - This tool provides estimates based on simplified calculations
            - Actual property values and rental markets can be volatile
            - Interest rates, taxes, and regulations may change over time
            - Consider consulting with a financial advisor for personalized advice
            - Property investment involves risks including market downturns and vacancy
            - Results are for educational purposes and should not be considered financial advice
            """)

        # PayPal donation button at the bottom of the page
        col2.markdown("---")  # Add a separator line
        col2.markdown("### Support This Tool")
        col2.markdown("If you find this property profit calculator helpful, consider supporting the development and hosting costs:")
        
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
        
        col2.markdown(paypal_html, unsafe_allow_html=True)
        col2.markdown("*Thank you for your support!*")

if __name__ == '__main__':
    main()