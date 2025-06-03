import pandas as pd
from taxes_by_prov_terr import calculate_total_taxes

def calculate_cpp_adjustment_factor(start_age):
    """
    Calculates the CPP adjustment factor based on the age when CPP benefits are first claimed.
    
    This function implements the official Canada Pension Plan adjustment rules that modify
    the base CPP amount depending on when benefits are started. The Canadian government
    provides incentives for delaying CPP and penalties for taking it early to account for
    the different number of years benefits will be received.
    
    Args:
        start_age (int): Age when CPP benefits will begin (must be between 60-70)
        
    Returns:
        float: Adjustment factor to multiply against base CPP amount
               - Values < 1.0 indicate reductions for early start
               - Value = 1.0 indicates no adjustment (standard age 65 start)
               - Values > 1.0 indicate increases for delayed start
               
    Adjustment Rules:
        - Early CPP (ages 60-64): 0.6% reduction per month before age 65
          Maximum reduction: 36% if started at age 60 (60 months × 0.6%)
        - Standard CPP (age 65): No adjustment (100% of calculated amount)
        - Delayed CPP (ages 66-70): 0.7% increase per month after age 65
          Maximum increase: 42% if started at age 70 (60 months × 0.7%)
          
    Example:
        calculate_cpp_adjustment_factor(62) returns 0.784 (21.6% reduction)
        calculate_cpp_adjustment_factor(65) returns 1.0 (no adjustment)
        calculate_cpp_adjustment_factor(68) returns 1.252 (25.2% increase)
    """
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

def calculate_oas_adjustment_factor(delay_months):
    """
    Calculates the OAS adjustment factor based on the number of months delayed after age 65.
    
    This function implements the OAS deferral increase rules. OAS can be deferred up to age 70,
    with a 0.6% increase per month deferred.
    
    Args:
        delay_months (int): Number of months OAS is delayed (0-60)
        
    Returns:
        float: Adjustment factor (1.0 + 0.006 per month delayed)
        
    Example:
        calculate_oas_adjustment_factor(0) returns 1.0
        calculate_oas_adjustment_factor(60) returns 1.36 (36% increase)
    """
    return 1 + (delay_months * 0.006)

def calculate_gis_reduction(adjusted_cpp_monthly, other_taxable_monthly, rrif_monthly=0):
    """
    Calculates the annual reduction in Guaranteed Income Supplement (GIS) based on other income sources.
    
    This function implements the Canadian government's GIS clawback rules, which reduce GIS benefits
    based on annual income from other sources. The GIS is designed as a supplement for low-income
    seniors, so it decreases as other income increases to target benefits to those most in need.
    
    Args:
        adjusted_cpp_monthly (float): Monthly CPP amount after age-based adjustments
        other_taxable_monthly (float): Monthly taxable income from employment, self-employment, etc.
        rrif_monthly (float, optional): Monthly RRIF income starting at age 71. Defaults to 0.
        
    Returns:
        float: Annual GIS reduction amount in CAD. Returns 0 if total income is below threshold.
        
    Implementation:
        - Income threshold: $5,000 annually before any GIS reduction
        - Reduction rate: 50% of income above threshold (50 cents per dollar)
        - Includes: CPP, other taxable income, net self employment income, RRIF income
        - Excludes: OAS (Old Age Security) - not included in this calculation
        
    Note:
        Not yet implemented:
        - Different thresholds for single vs. married individuals
        - Different reduction rates at different income levels?  #TODO: double check this
        - Provincial supplements with their own rules  #TODO: is this a thing?
    """
    threshold = 5000  # amount you are allowed to make before clawbacks occur
    total_annual_taxable_income = (adjusted_cpp_monthly + other_taxable_monthly + rrif_monthly) * 12
    if total_annual_taxable_income > threshold:
        reduction = (total_annual_taxable_income - threshold) * 0.5
        print(f"GIS values:\nreduction: {reduction}\nmonthly CPP: {adjusted_cpp_monthly}\nother monthly: {other_taxable_monthly}\nRRIF monthly: {rrif_monthly}\nthreshold: {threshold}")
        return max(0, reduction)
    return 0

def optimize_cpp_start_age(gis_base, cpp_base, life_expectancy, pre_retirement_taxable_monthly, post_retirement_taxable_monthly, retirement_age, retirement_months_delay, province, oas_monthly, oas_delay_months, birth_month, rrif_monthly=0):
    """
    Determines the optimal CPP start age to maximize total lifetime income across all benefit sources.
    
    This is the core optimization function that simulates lifetime income scenarios for each possible
    CPP start age (60-70) and calculates the total cumulative income from all sources. The function
    models the complex interactions between CPP timing, GIS clawbacks, RRIF income, and other taxable
    income to find the age that maximizes total lifetime benefits.
    
    The optimization considers:
    - CPP adjustment factors for early/delayed start
    - GIS reduction based on total income
    - Age-based benefit eligibility (GIS starts at 65, RRIF at 71)
    - Year-by-year income calculations from age 60 to life expectancy
    
    Args:
        gis_base (float): Base monthly GIS amount (before any reductions)
        cpp_base (float): Base monthly CPP amount at age 65 (before adjustments)
        life_expectancy (int): Expected life expectancy in years
        other_taxable_monthly (float): Monthly taxable income from other sources
        rrif_monthly (float, optional): Monthly RRIF income starting at age 71. Defaults to 0.
        
    Returns:
        pandas.DataFrame: Results dataframe with columns:
            - start_age: CPP start age (60-70)
            - total_cpp: Cumulative lifetime CPP income
            - total_gis: Cumulative lifetime GIS income (after reductions)
            - total_other_taxable_income: Cumulative lifetime other taxable income
            - total_rrif_income: Cumulative lifetime RRIF income
            - total_lifetime_income: Sum of all income sources over lifetime
            
    Calculation Process:
        1. For each possible CPP start age (60-70):
           a. Calculate adjusted CPP amount using age-based factors
           b. For each year from 60 to life expectancy:
              - Determine active income sources based on current age
              - Calculate GIS reduction based on total taxable income
              - Sum annual income from all sources
           c. Accumulate lifetime totals for each income category
        2. Return comprehensive results for comparison and optimization
        
    Note:
        The function includes debug print statements that output annual calculations
        for each age and start age combination, which can be useful for troubleshooting
        but may produce verbose console output during execution.
    """
    results = []

    # Calculate effective retirement age and proration
    retirement_calendar_month = ((birth_month - 1 + retirement_months_delay) % 12) + 1
    carry_over = 1 if (birth_month + retirement_months_delay > 12) else 0
    effective_retirement_age = retirement_age + carry_over
    pre_retirement_months_in_ret_year = retirement_calendar_month - 1
    post_retirement_months_in_ret_year = 12 - pre_retirement_months_in_ret_year
    
    # Calculate effective OAS start
    oas_delay_months_mod = oas_delay_months % 12
    oas_full_years = oas_delay_months // 12
    oas_calendar_month = ((birth_month - 1 + oas_delay_months_mod) % 12) + 1
    oas_carry_over = 1 if (birth_month + oas_delay_months_mod > 12) else 0
    oas_effective_age = 65 + oas_full_years + oas_carry_over
    oas_receiving_months_in_start_year = 12 - oas_calendar_month + 1

    # Calculate adjusted OAS amount
    oas_adjustment_factor = calculate_oas_adjustment_factor(oas_delay_months)
    adjusted_oas = oas_monthly * oas_adjustment_factor

    for start_age in range(60, 71):
        cumulative_gis_income = 0
        cumulative_cpp_income = 0
        cumulative_oas_income = 0
        cumulative_other_income = 0
        cumulative_rrif_income = 0
        cumulative_taxes = 0
        cumulative_income = 0
        
        # Calculate adjusted CPP amount
        adjustment_factor = calculate_cpp_adjustment_factor(start_age)
        adjusted_cpp = cpp_base * adjustment_factor
        
        for curAge in range(60, life_expectancy + 1):
            adjusted_gis = gis_base
            actual_cpp = adjusted_cpp
            actual_oas = 0
            actual_rrif = 0
            gis_reduction = 0
            
            if curAge < start_age: actual_cpp = 0
            if curAge >= oas_effective_age: actual_oas = adjusted_oas
            if curAge >= 71: actual_rrif = rrif_monthly
            
            # Calculate other taxable income accounting for effective retirement age
            if curAge < effective_retirement_age:
                other_taxable_monthly = pre_retirement_taxable_monthly
            elif curAge == effective_retirement_age:
                monthly_pre = (pre_retirement_taxable_monthly * pre_retirement_months_in_ret_year) / 12
                monthly_post = (post_retirement_taxable_monthly * post_retirement_months_in_ret_year) / 12
                other_taxable_monthly = monthly_pre + monthly_post
            else:
                other_taxable_monthly = post_retirement_taxable_monthly
                
            # Calculate GIS reduction
            if curAge < 65:
                adjusted_gis = 0
            else:
                gis_reduction = calculate_gis_reduction(actual_cpp, other_taxable_monthly, actual_rrif)

            # Calculate annual OAS based on effective start age
            if curAge > oas_effective_age:
                annual_oas = round(actual_oas * 12, 2)
            elif curAge == oas_effective_age:
                annual_oas = round(actual_oas * oas_receiving_months_in_start_year, 2)
            else:
                annual_oas = 0

            annual_cpp = round(actual_cpp * 12, 2)
            annual_gis = max(0, round((adjusted_gis * 12) - gis_reduction, 2))
            annual_other = round(other_taxable_monthly * 12, 2)
            annual_rrif = round(actual_rrif * 12, 2)
            annual_income = round(annual_cpp + annual_oas + annual_gis + annual_other + annual_rrif, 2)
            total_annual_taxable_income = (actual_cpp + actual_oas + other_taxable_monthly + actual_rrif) * 12
            taxes = calculate_total_taxes(province, total_annual_taxable_income)

            print(f"annual GIS: {annual_gis}, annual CPP: {annual_cpp}, annual OAS: {annual_oas}, annual RRIF: {annual_rrif} for curAge: {curAge} and start age: {start_age}\n---------------------------------------\n")

            cumulative_gis_income += annual_gis
            cumulative_cpp_income += annual_cpp
            cumulative_oas_income += annual_oas
            cumulative_other_income += annual_other
            cumulative_rrif_income += annual_rrif
            cumulative_taxes += taxes
            cumulative_income += annual_income
            
        results.append({
            'start_age': start_age,
            'total_cpp': cumulative_cpp_income,
            'total_oas': cumulative_oas_income,
            'total_gis': cumulative_gis_income,
            'total_other_taxable_income': cumulative_other_income,
            'total_rrif_income': cumulative_rrif_income,
            'total_lifetime_gross_income': cumulative_income,
            'total_taxes': cumulative_taxes,
            'total_lifetime_net_income': cumulative_income - cumulative_taxes
        })
    
    return pd.DataFrame(results)
