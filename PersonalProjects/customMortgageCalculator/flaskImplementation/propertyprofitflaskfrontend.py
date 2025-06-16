#!/bin/env python3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from propertyprofitflaskbackend import calculate_amortization_schedule, generate_monthly_property_profit_spreadsheet

#TODO: add ad functionality
#TODO: make a website for this instead of using localhost
#TODO: update such that the output spreadsheet has the correct number of columns for every single type of situation (right now just printing 0s for columns that aren't relevant)
#TODO: Convert this implementation from streamlit to flask

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
            rental_income = st.text_input("How much rental income is expected per month?", value="2000")
            inputs["rental_income"] = float(rental_income) if rental_income else 0.0
            rental_income_annual_increase = st.text_input("How much will you increase the rent for your new property each year (in %)?", value="2.5")
            inputs["rental_income_annual_increase"] = float(rental_income_annual_increase) if rental_income_annual_increase else 0.0
            occupancy_rate = st.text_input("What is the occupancy rate of your new rental (in %, 95 is the max allowed)?", value="90")
            inputs["occupancy_rate"] = float(occupancy_rate) if occupancy_rate else 0.0
            is_property_managed = st.radio("Are you going to pay someone to manage your property for you?", ("Yes", "No"))
            inputs["is_property_managed"] = is_property_managed
            if is_property_managed == "Yes":
                property_management_fees = st.text_input("How much are you going to pay your property manager (as a % of your rental income, standard is 10)?", value="10")
                inputs["property_management_fees"] = float(property_management_fees) if property_management_fees else 0.0
            are_utilities_paid_by_renter = st.radio("Are there utilities that your renter is not paying for?",("Yes", "No"))
            inputs["are_utilities_paid_by_renter"] = are_utilities_paid_by_renter
            if are_utilities_paid_by_renter == "Yes":
                total_utilities_not_paid_by_occupant = st.text_input("How much are you paying in utilities per month that your renter is not responsible for?",value="100")
                inputs["total_utilities_not_paid_by_occupant"] = float(total_utilities_not_paid_by_occupant) if total_utilities_not_paid_by_occupant else 0.0
    else:
        # Check if the user is moving from a rental property
        moving_from_rent = st.radio("Are you moving from a property which you currently rent?", ("Yes", "No"), index=1)
        inputs["moving_from_rent"] = moving_from_rent
        if moving_from_rent == "Yes":
            current_rent = st.text_input("What is the monthly rent paid?", value="2000")
            inputs["current_rent"] = float(current_rent) if current_rent else 0.0
            annual_rent_increase = st.text_input("How much do you estimate your current rent will go up each year (in %)?", value="2.5")
            inputs["annual_rent_increase"] = float(annual_rent_increase) if annual_rent_increase else 0.0
        utilities_difference = st.text_input(
            "How much more do you expect to pay in utilities/month compared to your current residence? (Negative value if less, 0 if same)",
            value="0")
        inputs["utilities_difference"] = float(utilities_difference) if utilities_difference else 0.0

    # Check if the property is a condo
    is_condo = st.radio("Is the property a condo?", ("Yes", "No"), index=1)
    inputs["is_condo"] = is_condo
    if is_condo == "Yes":
        condo_fees = st.text_input("What are the monthly condo fees?", value="400")
        inputs["condo_fees"] = float(condo_fees) if condo_fees else 0.0
        condo_fee_annual_increase = st.text_input("How much do the condo fees increase each year (in %)?", value="2")
        inputs["condo_fee_annual_increase"] = float(condo_fee_annual_increase) if condo_fee_annual_increase else 0.0

    # Check if user is getting help from someone monthly to pay for their mortgage
    if_help = st.radio("Are you getting assistance from someone each month (renting a room, from parents, a partner, etc)?", ("Yes", "No"), index=1)
    inputs["help"] = if_help
    if if_help == "Yes":
        monthly_help = st.text_input("How much are you getting each month?", value="500")
        inputs["monthly_help"] = float(monthly_help) if monthly_help else 0.0

    interest_rate = st.text_input("Interest rate of your loan (in %)", value="5")
    inputs["interest_rate"] = float(interest_rate) if interest_rate else 0.0

    house_price = st.text_input("House price", value="500000")
    inputs["house_price"] = float(house_price) if house_price else 0.0

    down_payment_percentage = st.text_input("Down payment (as a % of house price)", value="20")
    inputs["down_payment_percentage"] = float(down_payment_percentage) if down_payment_percentage else 0.0

    appreciation_rate = st.text_input("Expected annual appreciation rate of your new property (in %)", value="2")
    inputs["appreciation_rate"] = float(appreciation_rate) if appreciation_rate else 0.0

    amortization_period = st.text_input("What is the amortization period (in years)?", value="25")
    inputs["amortization_period"] = int(amortization_period) if amortization_period else 0

    property_taxes = st.text_input("What are the annual property taxes?", value="5000")
    inputs["property_taxes"] = float(property_taxes) if property_taxes else 0.0

    annual_property_tax_increase = st.text_input("How much do you estimate your property tax will go up each year (in %)?", value="2")
    inputs["annual_property_tax_increase"] = float(annual_property_tax_increase) if annual_property_tax_increase else 0.0

    real_estate_agent_fee = st.text_input("What is your real estate agent fee when you sell (in %)?", value="5.5")
    inputs["real_estate_agent_fee"] = float(real_estate_agent_fee) if real_estate_agent_fee else 0.0

    land_transfer_tax = st.text_input("What is the land transfer tax when you buy your new property?", value="8000")
    inputs["land_transfer_tax"] = float(land_transfer_tax) if land_transfer_tax else 0.0

    maintenance_budget = st.text_input("What is your expected monthly maintenance fee budget?", value="300")
    inputs["monthly_maintenance"] = float(maintenance_budget) if maintenance_budget else 0.0

    is_taxed = st.radio("Will there be a tax on the sale of the property?", ("Yes", "No"), index=1)
    inputs["is_taxed"] = is_taxed
    if is_taxed == "Yes":
        tax_percentage = st.text_input("What is the tax percentage on the capital gain?", value="35")
        inputs["tax_percentage"] = float(tax_percentage) if tax_percentage else 0.0
        factor = st.text_input("What is the factor at which the capital gain is taxed (e.g., 0.5 for 50% taxable)?", value="1")
        inputs["factor"] = float(factor) if factor else 0.0

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
            if inputs.get("utilities_difference") != 0:
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
    
def create_visualization(amortization_schedule):
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
    ax1.plot(amortization_schedule['month'], amortization_schedule['profit_if_sold'], linewidth=2)
    ax1.set_title('Profit if there is no rental income, help, or savings from renting before', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month property is sold')
    ax1.set_ylabel('Profit ($)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Lifetime Benefits Breakdown
    ax2.plot(amortization_schedule['month'], amortization_schedule['profit_if_sold_rentalincome_help'], marker='o', label='Total', linewidth=2)
    ax2.set_title('Profit if there is...#TODO this plot should be based on different inputs, title and y axis should change based on this', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month property is sold')
    ax2.set_ylabel('Profit ($)')
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

    plt.tight_layout()
    return fig

def formatAndDisplayTable(amortization_schedule):
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
    base_columns = ['month', 'outstanding_balance', 'current_house_value', 'profit_if_sold']

    # Find all profit_* columns (excluding 'profit_if_sold' itself)
    profit_columns = [col for col in amortization_schedule.columns if col.startswith('profit_') and col != 'profit_if_sold']

    # Filter profit columns where at least one value differs from 'profit_if_sold'
    variable_profit_columns = [
        col for col in profit_columns
        if not (amortization_schedule[col] == amortization_schedule['profit_if_sold']).all()
    ]

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

        inputs = initialize_webpage()
                                                                             
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
            #displaying graphs and table
            st.subheader("📈 Profit over Time")
            fig = create_visualization(amortization_schedule)
            st.pyplot(fig)
            
            formatAndDisplayTable(amortization_schedule)

            for message in profitability_messages:
                col2.write(message)
            
            # Generate and provide download for spreadsheet
            spreadsheet_data = generate_monthly_property_profit_spreadsheet(inputs)
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
