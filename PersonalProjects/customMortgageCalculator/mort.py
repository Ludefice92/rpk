#!/bin/env python3
import streamlit as st
import pandas as pd
import warnings
from io import BytesIO

# Suppress all warnings, for now this is just to ignore a spam message from pandas to make the console output more readable
warnings.simplefilter(action='ignore', category=FutureWarning)

#TODO: add ad functionality
#TODO: make a website for this instead of using localhost
#TODO: add proper handling to ensure inputs are valid
#TODO: update such that the output spreadsheet has the correct number of columns for every single type of situation (right now just printing 0s for columns that aren't relevant)

def initialize_webpage():
    inputs = {}
    st.title("Property monthly profit calculator")

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
    else:
        # Check if the user is moving from a rental property
        moving_from_rent = st.radio("Are you moving from a property which you currently rent?", ("Yes", "No"))
        inputs["moving_from_rent"] = moving_from_rent
        if moving_from_rent == "Yes":
            current_rent = st.text_input("What is the monthly rent paid?", value="0")
            inputs["current_rent"] = float(current_rent) if current_rent else 0.0
            annual_rent_increase = st.text_input("How much do you estimate your current rent will go up each year (in %)?", value="0")
            inputs["annual_rent_increase"] = float(annual_rent_increase) if annual_rent_increase else 0.0

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

    utilities_difference = st.text_input(
        "How much more do you expect to pay in utilities compared to your current property? (Negative value if less, 0 if same)",
        value="0")
    inputs["utilities_difference"] = float(utilities_difference) if utilities_difference else 0.0

    return inputs

def are_inputs_valid(inputs):
    # Check all required fields and print their values for debugging
    #print("Debug: Checking input values:", inputs)

    required_keys = [
        "interest_rate", "house_price", "down_payment_percentage",
        "appreciation_rate", "amortization_period",
        "property_taxes", "utilities_difference", "monthly_maintenance",
        "land_transfer_tax", "real_estate_agent_fee", "annual_property_tax_increase"
    ]

    return_val = True
    # Check if any required field is missing or empty
    for key in required_keys:
        value = inputs.get(key)
        if value is None or value == "":
            print(f"Debug: Missing or empty input for {key}")
            return_val = False

    # Check if rental income is expected and if the value is provided
    if inputs.get("expected_rental_income") == "Yes":
        if not inputs.get("rental_income_amount"):
            print("Debug: Missing rental income amount")
            return_val = False
        if not inputs.get("occupancy_rate"):
            print("Debug: Missing rental income property occupancy rate")
            return_val = False
        if not inputs.get("rental_income_annual_increase"):
            print("Debug: Missing rental income annual increase")
            return_val = False
        if inputs.get("is_property_managed") == "Yes" and not inputs.get("property_management_fees"):
            print("Debug: Missing property management fees")
            return_val = False


    # Check if the property is a condo and if the condo fees are provided
    if inputs.get("is_condo") == "Yes":
        if not inputs.get("condo_fees"):
            print("Debug: Missing condo fees")
            return_val = False
        if not inputs.get("condo_fee_annual_increase"):
            print("Debug: Missing condo fee annual increase")
            return_val = False

    # Check if moving from rent and if the monthly rent amount is provided
    if inputs.get("moving_from_rent") == "Yes":
        if not inputs.get("current_rent"):
            print("Debug: Missing monthly rent")
            return_val = False
        if not inputs.get("annual_rent_increase"):
            print("Debug: Missing annual rent increase")
            return_val = False

    # Check if there is help from family, partner, etc
    if inputs.get("help") == "Yes":
        if not inputs.get("monthly_help"):
            print("Debug: Missing monthly help")
            return_val = False

    if return_val: print("Debug: All inputs are valid")
    return return_val

def calculate_mortgage_payment(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    number_of_payments = years * 12
    monthly_payment = ((principal * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) /
                       ((1 + monthly_interest_rate) ** number_of_payments - 1))
    return round(monthly_payment,2)

def calculate_interest_payment(outstanding_balance, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    interest_payment = outstanding_balance * monthly_interest_rate
    return round(interest_payment,2)

def calculate_amortization_schedule(inputs):
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
    else:
        rental_income_increase_rate = 1
        rental_income_base = 0
        occupancy_rate = 0
    if inputs.get("is_property_managed") == "Yes":
        property_management_fee_base = rental_income_base * inputs.get("property_management_fees") * 0.01
    else:
        property_management_fee_base = 0

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

    #covering all possibilities for profitability given user inputs
    is_profitable = False
    is_profitable_saving_rent = False
    is_profitable_with_help = False
    is_profitable_saverent_help = False
    is_profitable_renting = False
    is_profitable_renting_help = False


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
        total_extra_monthly_expenses_paid += inputs.get("utilities_difference")
        total_maintenance_fees_paid += inputs.get("monthly_maintenance")
        if inputs.get("help") == "Yes": total_help += inputs.get("monthly_help")
        current_house_value *= appreciation_rate
        profit_if_sold = ((current_house_value * agent_fee_multiplier) - land_transfer_tax - total_interest_paid -
                          opportunity_cost - outstanding_balance - total_extra_monthly_expenses_paid -
                          total_maintenance_fees_paid)
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
            st.write(f"With only saving ${inputs.get("current_rent")}/month from your previous rental, you are profitable after {month} months")
        if inputs.get("help")=="Yes" and not is_profitable_with_help and profit_if_sold_with_help > 0:
            is_profitable_with_help = True
            st.write(f"With getting ${inputs.get("monthly_help")} in help/month, you are profitable after {month} months")
        if inputs.get("moving_from_rent")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_saverent_help and profit_if_sold_rentsaved_help > 0:
            is_profitable_saverent_help = True
            st.write(f"With saving ${inputs.get("current_rent")}/month from your previous rental and getting {inputs.get("monthly_help")} in help/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and not is_profitable_renting and profit_if_sold_with_rental_income > 0:
            is_profitable_renting = True
            st.write(f"With renting your new property at ${inputs.get("rental_income")}/month, you are profitable after {month} months")
        if inputs.get("rental_income_expected")=="Yes" and inputs.get("help")=="Yes" and not is_profitable_renting_help and profit_if_sold_rentalincome_help > 0:
            is_profitable_renting_help = True
            st.write(f"With renting your new property at ${inputs.get("rental_income")}/month and getting {inputs.get("monthly_help")} of help/month, you are profitable after {month} months")

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
    print(f"schedule length: {len(schedule)}")
    return schedule

def generate_monthly_property_profit_spreadsheet(inputs):
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
    st.set_page_config(page_title="Mortgage Calculator", layout="centered")
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

if __name__ == '__main__':
    main()