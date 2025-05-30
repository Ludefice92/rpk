import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#TODO: give this entire file a once over to make sure that the descriptions/comments make sense...made a ton of changes and didn't check

# Set page configuration
st.set_page_config(
    page_title="GIS and CPP Optimizer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def validate_inputs(gis_monthly, cpp_monthly, life_expectancy, other_taxable_monthly):
    """Validate user inputs with reasonable limits"""
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

    # Other taxable income monthly amount validation (reasonable range for Canadian GIS)
    if other_taxable_monthly < 0:
        errors.append("Other taxable income can not be negative")
    elif other_taxable_monthly > 20000:  # Maximum GIS is around $950 CAD as of 2024 #TODO: clean up comments in this function, also this variable needs a better max...should pick the number where you for sure aren't getting ANY GIS
        errors.append("We will save you some time, if you make more than $20000 per month you won't need GIS or CPP, why are you here?")
    
    return errors

def calculate_cpp_adjustment_factor(start_age):
    """Calculate CPP adjustment factor based on start age"""
    if start_age < 65:
        # Early pension reduction: 0.6% per month before 65
        months_early = (65 - start_age) * 12
        reduction = months_early * 0.006
        return 1 - reduction
    elif start_age > 65:
        # Delayed pension increase: 0.7% per month after 65
        months_late = (start_age - 65) * 12
        increase = months_late * 0.007
        return 1 + increase
    else:
        return 1.0

def calculate_gis_reduction(adjusted_cpp_monthly, other_taxable_monthly):
    """Calculate GIS reduction based on CPP and other taxable income amount"""
    threshold = 5000  # amount you are allowed to make before clawbacks occur
    total_annual_taxable_income = (adjusted_cpp_monthly + other_taxable_monthly) * 12
    if total_annual_taxable_income > threshold:
        reduction = (total_annual_taxable_income - threshold) * 0.5
        print(f"GIS values:\nreduction: {reduction}\nmonthly CPP: {adjusted_cpp_monthly}\nother monthly: {other_taxable_monthly}\nthreshold: {threshold}")
        return max(0, reduction)
    return 0

def optimize_cpp_start_age(gis_base, cpp_base, life_expectancy, other_taxable_monthly):
    """Find optimal CPP start age to maximize total lifetime benefits"""
    results = []

    for start_age in range(60, 71):
        cumulative_gis_income = 0
        cumulative_cpp_income = 0
        cumulative_other_income = 0
        cumulative_income = 0
        # Calculate adjusted CPP amount
        adjustment_factor = calculate_cpp_adjustment_factor(start_age)
        adjusted_cpp = cpp_base * adjustment_factor
        gis_reduction = 0
        for curAge in range(60, life_expectancy + 1):
            adjusted_gis = gis_base
            actual_cpp = adjusted_cpp
            if curAge < start_age: actual_cpp = 0
            # Calculate GIS reduction
            if curAge < 65 or curAge >= 71: #TODO: the upper part of this range is simplified due to RRIF assumptions, this should not be assumed
                adjusted_gis = 0
            else:
                gis_reduction = calculate_gis_reduction(actual_cpp, other_taxable_monthly)

            annual_cpp = round(actual_cpp * 12, 2)
            annual_gis = max(0,round((adjusted_gis * 12) - gis_reduction, 2))
            print(f"annual GIS: {annual_gis} and annual CPP: {annual_cpp} for curAge: {curAge} and start age: {start_age}\n---------------------------------------\n")
            annual_other = round(other_taxable_monthly * 12, 2)
            annual_income = round(annual_cpp + annual_gis + annual_other, 2)

            cumulative_gis_income += annual_gis
            cumulative_cpp_income += annual_cpp
            cumulative_other_income += annual_other
            cumulative_income += annual_income
            #TODO: I'm not properly accounting for the forced RRSP->RRIF income at 71 that should be a whole other category which affects GIS and total income
            #TODO: there is self employment income to model as well, there is a different clawback rate
        results.append({
            'start_age': start_age,
            'total_cpp': cumulative_cpp_income,
            'total_gis': cumulative_gis_income,
            'total_other_taxable_income': cumulative_other_income,
            'total_lifetime_income': cumulative_income
        })
    
    return pd.DataFrame(results)

def create_visualization(df):
    """Create visualizations for the optimization results"""
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Lifetime Benefits by Start Age
    ax1.plot(df['start_age'], df['total_lifetime_income'], marker='o', linewidth=2, markersize=8)
    ax1.set_title('Total Income by CPP Start Age', fontsize=14, fontweight='bold')
    ax1.set_xlabel('CPP Start Age')
    ax1.set_ylabel('Lifetime Income ($)')
    ax1.grid(True, alpha=0.3)
    ax1.ticklabel_format(style='plain', axis='y')
    
    # Highlight optimal age
    optimal_idx = df['total_lifetime_income'].idxmax()
    optimal_age = df.loc[optimal_idx, 'start_age']
    optimal_benefit = df.loc[optimal_idx, 'total_lifetime_income']
    ax1.scatter(optimal_age, optimal_benefit, color='red', s=100, zorder=5)
    ax1.annotate(f'Optimal: Age {optimal_age}', 
                xy=(optimal_age, optimal_benefit), 
                xytext=(optimal_age+1, optimal_benefit),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    # Plot 2: Monthly Benefits Breakdown
    ax2.plot(df['start_age'], df['total_cpp'], marker='s', label='CPP', linewidth=2)
    ax2.plot(df['start_age'], df['total_gis'], marker='^', label='GIS', linewidth=2)
    ax2.plot(df['start_age'], df['total_other_taxable_income'], marker='x', label='Other', linewidth=2)
    ax2.plot(df['start_age'], df['total_lifetime_income'], marker='o', label='Total', linewidth=2)
    ax2.set_title('Monthly Benefits by CPP Start Age', fontsize=14, fontweight='bold')
    ax2.set_xlabel('CPP Start Age')
    ax2.set_ylabel('Monthly Benefits ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def formatAndDisplayTable(display_df):
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
    col1, col2, col3 = st.columns([1, 6, 1])
    
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

        other_taxable_monthly = col2.number_input(
            "Other monthly taxable income ($CAD)",
            min_value=0,
            max_value=20000,
            value=0,
            step=10,
            help="How much you make from all taxable income sources per month, except for CPP/OAS/GIS"
        )
        
        life_expectancy = col2.number_input(
            "Life Expectancy (years)",
            min_value=60,
            max_value=130,
            value=80,
            step=1,
            help="Your estimated life expectancy"
        )
        
        # Validate inputs
        validation_errors = validate_inputs(gis_monthly, cpp_monthly, life_expectancy, other_taxable_monthly)
        
        if validation_errors:
            col2.error("Please fix the following input errors:")
            for error in validation_errors:
                col2.error(f"• {error}")
            return
        
        # Calculate optimization results
        if col2.button("🔍 Optimize CPP Start Age", type="primary"):
            with st.spinner("Calculating optimal CPP start age..."):
                results_df = optimize_cpp_start_age(gis_monthly, cpp_monthly, life_expectancy, other_taxable_monthly)
                
                # Find optimal age
                optimal_idx = results_df['total_lifetime_income'].idxmax()
                optimal_result = results_df.loc[optimal_idx]
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                st.metric(
                    "🎯 Optimal CPP Start Age",
                    f"{int(optimal_result['start_age'])} years",
                    help="Age that maximizes total lifetime income"
                )
                
                st.metric(
                    "💰 Maximum Total Lifetime Income",
                    f"${optimal_result['total_lifetime_income']:,.0f}",
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
                    'Start Age', 'Lifetime CPP ($)', 'Lifetime GIS ($)',
                    'Lifetime Other Taxable Income ($)', 'Total Lifetime Income ($)'
                ]

                # Format values
                display_df['Start Age'] = display_df['Start Age'].astype(int)

                for col in display_df.columns:
                    if col != 'Start Age':
                        display_df[col] = display_df[col].map(lambda x: f"{x:,.2f}")

                formatAndDisplayTable(display_df)
                
                col1, col2 = st.columns(2)
                
                # Download option
                csv = results_df.to_csv(index=False)
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
