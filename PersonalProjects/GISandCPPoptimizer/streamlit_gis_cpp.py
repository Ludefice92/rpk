import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from gis_cpp_optimizer import calculate_cpp_adjustment_factor, calculate_oas_adjustment_factor, calculate_gis_reduction, optimize_cpp_start_age

#TODO: give this entire file a once over to make sure that the descriptions/comments make sense...made a ton of changes and didn't check

# Set page configuration
st.set_page_config(
    page_title="GIS and CPP Optimizer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def validate_inputs(gis_monthly, cpp_monthly, life_expectancy, pre_retirement_taxable_monthly, post_retirement_taxable_monthly, retirement_age, retirement_months_delay, oas_monthly, oas_delay_months, rrif_monthly=0):
    """
    Validates all user inputs to ensure they meet the required criteria for CPP and GIS optimization calculations.
    
    This function performs comprehensive validation on all input parameters, checking for:
    - Required field presence and non-negative values
    - Realistic ranges appropriate for Canadian government benefits
    - Logical consistency between related parameters
    - Age-based constraints for pension eligibility
    
    The function uses specific validation rules based on current Canadian government benefit
    maximums and reasonable life expectancy ranges to prevent unrealistic calculations.
    
    Args:
        gis_monthly (float): Expected monthly Guaranteed Income Supplement amount in CAD
        cpp_monthly (float): Expected monthly Canada Pension Plan amount at age 65 in CAD
        life_expectancy (int): Estimated life expectancy in years
        other_taxable_monthly (float): Monthly taxable income from other sources in CAD
        rrif_monthly (float, optional): Monthly RRIF income starting at age 71 in CAD. Defaults to 0.
        
    Returns:
        list: List of error messages as strings. Empty list if all inputs are valid.
        
    Validation Rules:
        - GIS monthly: $0-$3,000 (max GIS is ~$950 CAD as of 2024)
        - CPP monthly: $0-$5,000 (max CPP is ~$1,300 CAD as of 2024)
        - Life expectancy: 60-130 years (60 is earliest CPP start age)
        - Other taxable income: $0-$20,000 monthly
        - RRIF monthly: $0-$20,000 monthly
    """
    errors = []
    
    # GIS monthly amount validation (reasonable range for Canadian GIS)
    if gis_monthly < 0:
        errors.append("GIS monthly amount cannot be negative")
    elif gis_monthly > 3000:  # Maximum GIS is around $950 CAD as of 2024
        errors.append("GIS monthly amount seems too high (max ~$950 CAD)")
    
    # CPP monthly amount validation (maximum CPP is around $1300 CAD as of 2024)
    if cpp_monthly < 0:
        errors.append("CPP monthly amount cannot be negative")
    elif cpp_monthly > 5000:
        errors.append("CPP monthly amount seems too high (max ~$1300 CAD)")
    
    # Life expectancy validation (oldest verified human lived to 122, adding 5 years buffer)
    if life_expectancy < 60:
        errors.append("Life expectancy cannot be less than 60 (earliest CPP start age)")
    elif life_expectancy > 130:
        errors.append("Life expectancy cannot be more than 130 years")

    # Pre-retirement taxable income monthly amount validation
    if pre_retirement_taxable_monthly < 0:
        errors.append("Pre-retirement taxable income can not be negative")
    elif pre_retirement_taxable_monthly > 20000:
        errors.append("We will save you some time, if you make more than $20000 per month you won't need GIS or CPP, why are you here?")
    
    # Post-retirement taxable income monthly amount validation
    if post_retirement_taxable_monthly < 0:
        errors.append("Post-retirement taxable income can not be negative")
    elif post_retirement_taxable_monthly > 20000:
        errors.append("We will save you some time, if you make more than $20000 per month you won't need GIS or CPP, why are you here?")
    
    # Retirement age validation
    if retirement_age < 60:
        errors.append("Retirement age cannot be less than 60")
    elif retirement_age > 75:
        errors.append("Retirement age cannot be more than 75")
    if retirement_age >= life_expectancy:
        errors.append("Retirement age must be less than life expectancy")
        
    # Retirement months delay validation
    if retirement_months_delay < 0:
        errors.append("Retirement months delay cannot be negative")
    elif retirement_months_delay > 11:
        errors.append("Retirement months delay cannot be more than 11 months")
    
    # RRIF monthly amount validation
    if rrif_monthly < 0:
        errors.append("RRIF monthly amount cannot be negative")
    elif rrif_monthly > 20000:
        errors.append("RRIF monthly amount seems too high (consider reasonable withdrawal limits)")

    # OAS monthly amount validation (reasonable range for Canadian OAS)
    if oas_monthly < 0:
        errors.append("OAS monthly amount cannot be negative")
    elif oas_monthly > 3000:
        errors.append("OAS monthly amount is far too high (max $3000 CAD)")
    
    # OAS delay months validation
    if oas_delay_months < 0:
        errors.append("OAS delay months cannot be negative")
    elif oas_delay_months > 60:
        errors.append("OAS delay can be at most 60 months (5 years)")    
    return errors


def create_visualization(df):
    """
    Creates comprehensive matplotlib visualizations to display CPP optimization results.
    
    This function generates a two-panel visualization that helps users understand the optimization
    results both in terms of total lifetime income and the breakdown of different income sources.
    The visualizations are designed to clearly highlight the optimal CPP start age and show how
    different benefit sources contribute to total lifetime income.
    
    Args:
        df (pandas.DataFrame): Results dataframe from optimize_cpp_start_age() containing:
            - start_age: CPP start ages (60-70)
            - total_lifetime_income: Total cumulative income for each start age
            - total_cpp, total_gis, total_other_taxable_income, total_rrif_income: Income breakdowns
            
    Returns:
        matplotlib.figure.Figure: Complete figure object with two subplots ready for display
        
    Visualization Components:
        
        Left Panel - Total Lifetime Income Optimization:
        - Bar chart showing total lifetime income lost for each CPP start age compared to the optimal CPP start age
        - Grid and professional formatting for easy interpretation
        - Y-axis formatted to show dollar amounts clearly
        
        Right Panel - Income Source Breakdown:
        - Multiple line plots showing contribution of each income source
        - Separate lines for CPP, GIS, Other Income, RRIF (if applicable), and Total
        - Legend to distinguish between different income sources
        - Helps users understand how CPP timing affects each benefit type
    """
    fig, ((ax2, ax1)) = plt.subplots(2, 1, figsize=(18, 10))
    df['start_time'] = df['start_age'] + (df['start_month'] - 1) / 12.0
    # Calculate optimal
    optimal_idx = df['total_lifetime_net_income'].idxmax()
    optimal_start_time = df.loc[optimal_idx, 'start_time']
    optimal_benefit = df.loc[optimal_idx, 'total_lifetime_net_income']

    # Calculate losses
    df['loss'] = df['total_lifetime_net_income'] - optimal_benefit

    # Plot 1: Lifetime Loss by CPP Start Age
    ax1.bar(df['start_time'], df['loss'], width=0.2, color='red')
    ax1.set_title('Lifetime Loss Compared to Optimal CPP Start Age', fontsize=14, fontweight='bold')
    ax1.set_xlabel('CPP Start Age')
    ax1.set_ylabel('Lifetime Loss ($)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Lifetime Benefits Breakdown
    ax2.plot(df['start_time'], df['total_cpp'], marker='s', label='CPP', linewidth=2)
    ax2.plot(df['start_time'], df['total_oas'], marker='*', label='OAS', linewidth=2)
    ax2.plot(df['start_time'], df['total_gis'], marker='^', label='GIS', linewidth=2)
    ax2.plot(df['start_time'], df['total_other_taxable_income'], marker='x', label='Other', linewidth=2)
    if 'total_rrif_income' in df.columns and df['total_rrif_income'].sum() > 0:
        ax2.plot(df['start_time'], df['total_rrif_income'], marker='d', label='RRIF', linewidth=2)
    ax2.plot(df['start_time'], df['total_lifetime_net_income'], marker='o', label='Total', linewidth=2)
    ax2.set_title('Lifetime Income by CPP Start Age', fontsize=14, fontweight='bold')
    ax2.set_xlabel('CPP Start Age')
    ax2.set_ylabel('Lifetime Income ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

    plt.tight_layout()
    df.pop("start_time")
    df.pop("loss")
    return fig

def formatAndDisplayTable(display_df):
    """
    Formats and displays a pandas DataFrame as a styled HTML table in Streamlit.
    
    This function converts a pandas DataFrame into a professionally styled HTML table
    that integrates seamlessly with the Streamlit interface. The function manually
    generates HTML to ensure consistent styling and proper formatting of financial
    data, providing better control over appearance than Streamlit's default table display.
    
    Args:
        display_df (pandas.DataFrame): DataFrame containing the optimization results to display.
                                     Expected to have formatted string values for financial columns
                                     and integer values for age columns.
                                     
    Returns:
        None: The function directly renders the HTML table in the Streamlit interface
              using st.markdown() with unsafe_allow_html=True
    """
    headers = display_df.columns.tolist()
    rows = display_df.values.tolist()

    # Generate HTML table manually
    table_html = "<table><thead><tr>"
    for header in headers:
        table_html += f"<th>{header}</th>"
    table_html += "</tr></thead><tbody>"

    for row in rows:
        table_html += "<tr>"
        for item in row:
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
    Main application entry point that orchestrates the Streamlit web application for CPP and GIS optimization.
    
    This function serves as the primary controller for the CPP and GIS optimization application.
    It manages the overall user experience by coordinating input collection, validation,
    calculation processing, and result presentation. The function implements a comprehensive
    web application pattern with professional layout, advertising integration, and user guidance.
    
    Application Flow:
        1. Configure page layout with three-column structure (ads, main content, ads)
        2. Display application title, description, and input form
        3. Collect and validate all user inputs for optimization parameters
        4. Process optimization calculations when user triggers analysis
        5. Present results through multiple visualization formats
        6. Provide educational information and disclaimers
        7. Include donation functionality for application support
        
    Layout Structure:
        - Left column (1/8 width): Advertisement space for senior financial services
        - Center column (6/8 width): Main application interface and functionality
        - Right column (1/8 width): Advertisement space for senior financial services
        
    Key Features:
        - Professional three-column layout with integrated advertising
        - Comprehensive input validation with real-time error feedback
        - Interactive optimization with progress indicators
        - Multiple result presentation formats (metrics, charts, tables)
        - Educational expandable sections explaining CPP, GIS, and RRIF rules
        - CSV download functionality for detailed analysis
        - PayPal donation integration for application sustainability
        - Responsive design that adapts to different screen sizes
        
    Input Parameters Collected:
        - GIS monthly amount (expected Guaranteed Income Supplement)
        - CPP monthly amount at age 65 (base Canada Pension Plan amount)
        - Other monthly taxable income (employment, self-employment, RRSP withdrawals)
        - RRIF monthly income (optional, starting at age 71)
        - Life expectancy (for lifetime income calculations)
        
    Error Handling:
        - Comprehensive input validation with user-friendly error messages
        - Graceful handling of edge cases and invalid parameter combinations
        - Clear guidance for users to correct input errors
        
    Session State Management:
        - Maintains calculation state across Streamlit reruns
        - Ensures consistent user experience during form interaction
        - Preserves user inputs during validation and processing
        
    Note:
        The function includes placeholder advertisement content that should be
        replaced with actual advertising partnerships for monetization.
    """
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        if 'accepted_terms' not in st.session_state:
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
    
    with col1:
        st.header("Ads")
        st.html("""
        <div style="background-color: #f0f0f0; padding: 10px; text-align: center;">
            <p>Debt Consolidation for Seniors</p>
            <p>Consolidate your debts and save on interest!</p>
            <a href="https://example.com/debt-consolidation" target="_blank">Learn More</a>
        </div>
        """)

    with col3:
        st.header("Ads")
        st.html("""
        <div style="background-color: #f0f0f0; padding: 10px; text-align: center;">
            <p>Reverse Mortgages for 50+</p>
            <p>Access your home equity without monthly payments!</p>
            <a href="https://example.com/reverse-mortgage" target="_blank">Get Started</a>
        </div>
        """)

    with col2:
        col2.title("🏦 GIS and CPP Optimizer")
        col2.markdown("### Optimize your Canada Pension Plan (CPP) start age to maximize lifetime benefits")
        
        col2.markdown("""
        This tool helps you determine the optimal age to start receiving CPP benefits by considering:
        - CPP adjustment factors (early/late pension)
        - Guaranteed Income Supplement (GIS) interactions
        - RRIF income starting at age 71 (optional)
        - Your life expectancy
        - Total lifetime benefit optimization
        """)
        # Moved from sidebar
        col2.header("📊 Input Parameters")
    
        # Input fields
        gis_monthly = col2.number_input(
            "GIS Monthly Amount ($CAD)",
            min_value=0.0,
            max_value=3000.0,
            value=1100.0,
            step=10.0,
            help="Your expected monthly Guaranteed Income Supplement amount"
        )
        
        cpp_monthly = col2.number_input(
            "CPP Monthly Amount at Age 65 ($CAD)",
            min_value=0.0,
            max_value=5000.0,
            value=1400.0,
            step=10.0,
            help="Your expected monthly CPP amount if you start at age 65"
        )

        oas_monthly = col2.number_input(
            "OAS Monthly Amount at Age 65 ($CAD)",
            min_value=0.0,
            max_value=3000.0,
            value=750.0,
            step=10.0,
            help="Your expected monthly OAS amount if you start at age 65"
        )

        oas_delay_months = col2.number_input(
            "OAS Delay Months",
            min_value=0,
            max_value=60,
            value=0,
            step=1,
            help="Number of months to delay OAS after age 65 (up to 60 months for 36% increase, this also delays your GIS)"
        )
        pre_retirement_taxable_monthly = col2.number_input(
            "Pre-retirement gross monthly taxable income ($CAD)",
            min_value=0,
            max_value=20000,
            value=6000,
            step=10,
            help="How much you make from all taxable income sources per month before retirement, including net self-employment income and RRSP withdrawals, except for CPP/OAS/GIS and forced RRIF withdrawals"
        )
        post_retirement_taxable_monthly = col2.number_input(
            "Post-retirement monthly taxable income ($CAD)",
            min_value=0,
            max_value=20000,
            value=0,
            step=10,
            help="How much you make from all taxable income sources per month after retirement, including net self-employment income and RRSP withdrawals, except for CPP/OAS/GIS and forced RRIF withdrawals"
        )
        retirement_age = col2.number_input(
            "Retirement Age",
            min_value=60,
            max_value=75,
            value=65,
            step=1,
            help="The age at which you plan to retire (60-75)"
        )
        retirement_months_delay = col2.number_input(
            "Months after birth month to retire",
            min_value=0,
            max_value=11,
            value=0,
            step=1,
            help="How many months after your birth month will you retire? (0-11). For example, if you're born in January and want to retire in March of your retirement year, enter 2."
        )
        
        # RRIF section
        include_rrif = col2.checkbox(
            "Include RRIF Income",
            value=False,
            help="Check this if you have RRSP/RRIF assets that will be converted to mandatory income at age 71"
        )
        
        rrif_monthly = 0
        if include_rrif:
            rrif_monthly = col2.number_input(
                "RRIF Monthly Income at Age 71 ($CAD)",
                min_value=0.0,
                max_value=50000.0,
                value=1000.0,
                step=50.0,
                help="Your expected monthly RRIF income starting at age 71 (forced RRSP conversion)"
            )
        
        life_expectancy = col2.number_input(
            "Life Expectancy (years)",
            min_value=60,
            max_value=130,
            value=80,
            step=1,
            help="Your estimated life expectancy"
        )
        provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK', 'NT', 'NU', 'YT']
        province = col2.selectbox("Select Province/Territory", provinces, index=6)  # Default to ON

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        birth_month_str = col2.selectbox("Select Birth Month", months, index=0)
        birth_month = months.index(birth_month_str) + 1
        
        # Validate inputs
        validation_errors = validate_inputs(gis_monthly, cpp_monthly, life_expectancy, pre_retirement_taxable_monthly, post_retirement_taxable_monthly, retirement_age,
                                            retirement_months_delay, oas_monthly, oas_delay_months, rrif_monthly)
        
        if validation_errors:
            col2.error("Please fix the following input errors:")
            for error in validation_errors:
                col2.error(f"• {error}")
            return
        
        # Calculate optimization results
        if col2.button("🔍 Optimize CPP Start Age", type="primary"):
            with st.spinner("Calculating optimal CPP start age..."):
                results_df = optimize_cpp_start_age(gis_monthly, cpp_monthly, life_expectancy, pre_retirement_taxable_monthly, post_retirement_taxable_monthly, retirement_age,
                                                    retirement_months_delay, province, oas_monthly, oas_delay_months, birth_month, rrif_monthly)

                # Store results in session state so they aren't removed after generating CSV
                st.session_state['results_df'] = results_df

        # If results are available in session state
        if 'results_df' in st.session_state:
            results_df = st.session_state['results_df']

            # Find optimal age and month
            optimal_idx = results_df['total_lifetime_net_income'].idxmax()
            optimal_result = results_df.loc[optimal_idx]

            # Display results
            col1, col2, col3 = st.columns(3)
            
            st.metric(
                "🎯 Optimal CPP Start Age",
                f"{int(optimal_result['start_age'])} years, {int(optimal_result['start_month'])} months",
                help="Age and month that maximizes total lifetime income"
            )
            
            st.metric(
                "💰 Maximum Total Lifetime Net Income",
                f"${optimal_result['total_lifetime_net_income']:,.0f}",
                help="Total income over your lifetime"
            )
            #    st.metric(
            #        "📅 Monthly Benefits at Optimal Age",
            #        f"${optimal_result['total_monthly']:.0f}",
            #        help="Combined CPP + GIS monthly amount"
            #    )
            # Create and display visualizations
            st.subheader("📈 Optimization Analysis")
            fig = create_visualization(results_df)
            st.pyplot(fig)
            
            # Display detailed results table
            st.subheader("📋 Detailed Results")
            
            # Format the dataframe for display
            display_df = results_df.copy()
            
            # Rename columns for display
            display_df.columns = [
                'Start Age', 'Start Month', 'Lifetime CPP ($)', 'Lifetime OAS ($)', 'Lifetime GIS ($)', 'Lifetime Other Taxable Income ($)', 
                'Lifetime RRIF Income ($)', 'Total Lifetime Gross Income ($)', 'Lifetime Taxes ($)', 'Total Lifetime Net Income ($)'
            ]
            
            # Format values
            display_df['Start Age'] = display_df['Start Age'].astype(int)
            display_df['Start Month'] = display_df['Start Month'].astype(int)

            for col in display_df.columns:
                if col not in ['Start Age', 'Start Month']:
                    display_df[col] = display_df[col].map(lambda x: f"{x:,.2f}")

            formatAndDisplayTable(display_df)
            #col1, col2 = st.columns(2) #REMOVE?
            
            # Download option
            csv = results_df.round(2).to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"cpp_optimization_results_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Information section
        st.markdown("---")
        st.subheader("ℹ️ About This Tool")
        
        with st.expander("How CPP Adjustments Work"):
            st.markdown("""
            **Early Pension (Age 60-64):**
            - CPP is reduced by 0.6% for each month before age 65
            - Maximum reduction: 36% if you start at age 60
            
            **Standard Pension (Age 65):**
            - No adjustment - you receive 100% of your calculated CPP
            
            **Late Pension (Age 66-70):**
            - CPP is increased by 0.7% for each month after age 65
            - Maximum increase: 42% if you start at age 70
            """)
        
        with st.expander("GIS Interaction"):
            st.markdown("""
            **Guaranteed Income Supplement (GIS):**
            - GIS is reduced based on other pension income
            - Generally reduced by $1 for every $2 of CPP income above a threshold
            - This interaction affects the optimal CPP start age
            - Higher CPP payments may reduce GIS eligibility
            """) #TODO: this is a wrong description of GIS, fix it
            
        with st.expander("RRIF Information"):
            st.markdown("""
            **Registered Retirement Income Fund (RRIF):**
            - RRSPs must be converted to RRIFs by age 71
            - RRIF withdrawals are mandatory and taxable income
            - RRIF income affects GIS eligibility and amount
            - This tool assumes RRIF income starts at age 71 and continues until life expectancy
            - RRIF income is added to employment income for GIS calculation purposes
            """)
        
        with st.expander("Important Disclaimers"):
            st.markdown("""
            **⚠️ Important Notes:**
            - This tool provides estimates based on simplified calculations
            - Actual CPP and GIS amounts depend on many factors including contribution history
            - GIS eligibility and amounts are subject to annual income testing
            - Consult with a financial advisor for personalized advice
            - Government benefit rules may change over time
            """)

        # PayPal donation button at the bottom
        st.markdown("---")
        st.markdown("### 💝 Support This Tool")
        st.markdown("If you found this GIS and CPP optimizer helpful, consider supporting its development:")
        
        # PayPal donation button HTML
        paypal_html = """
        <form action="https://www.paypal.com/donate" method="post" target="_top">
        <input type="hidden" name="hosted_button_id" value="YOUR_PAYPAL_BUTTON_ID" />
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
        <img alt="" border="0" src="https://www.paypal.com/en_CA/i/scr/pixel.gif" width="1" height="1" />
        </form>
        """
        
        st.markdown(paypal_html, unsafe_allow_html=True)
        st.markdown("*Your support helps maintain and improve this free tool for everyone!*")

if __name__ == "__main__":
    main()
