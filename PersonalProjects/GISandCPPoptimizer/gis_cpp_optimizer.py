import pandas as pd
from taxes_by_prov_terr import calculate_total_taxes

def calculate_cpp_adjustment_factor(cpp_start_delay_months):
    """
    Calculates the CPP adjustment factor based on the age when CPP benefits are first claimed.
    
    This function implements the official Canada Pension Plan adjustment rules that modify
    the base CPP amount depending on when benefits are started. The Canadian government
    provides incentives for delaying CPP and penalties for taking it early to account for
    the different number of years benefits will be received.
    #TODO: update this functions comments and check others
    Args:
        cpp_start_delay_months (int): Month when CPP benefits will begin (must be between 0-120)
        
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
    # Calculate adjustment factor
    if cpp_start_delay_months < 61:
        months_early = 61 - cpp_start_delay_months
        reduction = months_early * 0.006
        return 1 - reduction
    elif cpp_start_delay_months > 61:
        months_late = cpp_start_delay_months - 61
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

def calculate_gis_reduction(annual_cpp, annual_other_taxable, annual_rrif=0):
    """
    Calculates the annual reduction in Guaranteed Income Supplement (GIS) based on other income sources.
    
    This function implements the Canadian government's GIS clawback rules, which reduce GIS benefits
    based on annual income from other sources. The GIS is designed as a supplement for low-income
    seniors, so it decreases as other income increases to target benefits to those most in need.
    
    Args:
        annual_cpp (float): Annual CPP amount after age-based adjustments
        annual_other_taxable (float): Annual taxable income from employment, self-employment, etc.
        annual_rrif (float, optional): Annual RRIF income starting at age 71. Defaults to 0.
        
    Returns:
        float: Annual GIS reduction amount in CAD. Returns 0 if total income is below threshold.
        
    Implementation:
        - Income threshold: $5,000 annually before any GIS reduction
        - Reduction rate: 50% of income between $5,000 and $15,000
        - Reduction rate: 100% of income above $15,000
        - Includes: CPP, other taxable income, net self employment income, RRIF income
        - Excludes: OAS (Old Age Security) - not included in this calculation
        
    Note:
        Not yet implemented:
        - Different thresholds for single vs. married individuals
        - Provincial supplements with their own rules
    """
    threshold1 = 5000
    threshold2 = 15000
    total_annual_taxable_income_no_oas = annual_cpp + annual_other_taxable + annual_rrif
    if total_annual_taxable_income_no_oas <= threshold1:
        reduction = 0
    elif total_annual_taxable_income_no_oas <= threshold2:
        reduction = (total_annual_taxable_income_no_oas - threshold1) * 0.5
    else:
        reduction = (threshold2 - threshold1) * 0.5 + total_annual_taxable_income_no_oas - threshold2
    print(f"GIS values: reduction: {reduction}, annual CPP: {annual_cpp}, annual other: {annual_other_taxable}, annual RRIF: {annual_rrif}, threshold1: {threshold1}, threshold2: {threshold2}")
    return max(0, reduction)

def optimize_cpp_start_age(gis_base, cpp_base, life_expectancy, pre_retirement_taxable_monthly, post_retirement_taxable_monthly, retirement_age, retirement_months_delay, province, oas_monthly, oas_delay_months, birth_month, rrif_monthly=0):
    """
    Determines the optimal CPP start age and month to maximize total lifetime income across all benefit sources.
    
    This is the core optimization function that simulates lifetime income scenarios for each possible
    CPP start month (from age 60 to 70) and calculates the total cumulative income from all sources. The function
    models the complex interactions between CPP timing, GIS clawbacks, RRIF income, and other taxable
    income to find the age and month that maximizes total lifetime benefits.
    
    The optimization considers:
    - CPP adjustment factors for early/delayed start (calculated monthly)
    - GIS reduction based on total income
    - Age-based benefit eligibility (GIS starts at 65, RRIF at 71)
    - Month-by-month income calculations from age 60 to life expectancy
    - CPP can start the month after birth month when turning 60 or later
    
    Args:
        gis_base (float): Base monthly GIS amount (before any reductions)
        cpp_base (float): Base monthly CPP amount at age 65 (before adjustments)
        life_expectancy (int): Expected life expectancy in years
        pre_retirement_taxable_monthly (float): Monthly taxable income before retirement
        post_retirement_taxable_monthly (float): Monthly taxable income after retirement
        retirement_age (int): Age at which retirement occurs
        retirement_months_delay (int): Months after birth month to retire (0-11)
        province (str): Province/territory code for tax calculations
        oas_monthly (float): Base monthly OAS amount at age 65
        oas_delay_months (int): Number of months to delay OAS after age 65
        birth_month (int): Birth month (1-12)
        rrif_monthly (float, optional): Monthly RRIF income starting at age 71. Defaults to 0.
        
    Returns:
        pandas.DataFrame: Results dataframe with columns:
            - start_age: CPP start age (60-70)
            - start_month: CPP start month (1-12, month after birth month)
            - total_cpp: Cumulative lifetime CPP income
            - total_gis: Cumulative lifetime GIS income (after reductions)
            - total_other_taxable_income: Cumulative lifetime other taxable income
            - total_rrif_income: Cumulative lifetime RRIF income
            - total_lifetime_income: Sum of all income sources over lifetime
            
    Calculation Process:
        1. For each possible CPP start month from age 60 to 70:
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

    for cpp_start_delay_months in range(1, 122):
        # Calculate effective CPP start
        delay_mod = cpp_start_delay_months % 12
        full_years = cpp_start_delay_months // 12
        start_calendar_month = ((birth_month - 1 + delay_mod) % 12) + 1
        carry_over = 1 if (birth_month + delay_mod > 12) else 0
        cpp_effective_age = 60 + full_years + carry_over
        receiving_months_in_start_year = 12 - start_calendar_month + 1

        # Calculate adjusted CPP amount
        adjustment_factor = calculate_cpp_adjustment_factor(cpp_start_delay_months)
        adjusted_cpp = cpp_base * adjustment_factor

        cumulative_gis_income = 0
        cumulative_cpp_income = 0
        cumulative_oas_income = 0
        cumulative_other_income = 0
        cumulative_rrif_income = 0
        cumulative_taxes = 0
        cumulative_income = 0
        
        for curAge in range(60, life_expectancy + 1):
            adjusted_gis = gis_base
            actual_oas = 0
            actual_rrif = 0
            gis_reduction = 0
            
            if curAge >= oas_effective_age: actual_oas = adjusted_oas
            if curAge > 71: actual_rrif = rrif_monthly
            
            # Calculate other taxable income accounting for effective retirement age
            if curAge < effective_retirement_age:
                other_taxable_monthly = pre_retirement_taxable_monthly
            elif curAge == effective_retirement_age:
                monthly_pre = (pre_retirement_taxable_monthly * pre_retirement_months_in_ret_year) / 12
                monthly_post = (post_retirement_taxable_monthly * post_retirement_months_in_ret_year) / 12
                other_taxable_monthly = monthly_pre + monthly_post
            else:
                other_taxable_monthly = post_retirement_taxable_monthly
                
            # Calculate annual OAS based on effective start age
            if curAge > oas_effective_age:
                annual_oas = round(actual_oas * 12, 2)
            elif curAge == oas_effective_age:
                annual_oas = round(actual_oas * oas_receiving_months_in_start_year, 2)
            else:
                annual_oas = 0

            # For CPP
            if curAge > cpp_effective_age:
                annual_cpp = round(adjusted_cpp * 12, 2)
            elif curAge == cpp_effective_age:
                annual_cpp = round(adjusted_cpp * receiving_months_in_start_year, 2)
            else:
                annual_cpp = 0

            annual_other = round(other_taxable_monthly * 12, 2)
            annual_rrif = round(actual_rrif * 12, 2)

            total_annual_taxable_income = round(annual_cpp + annual_oas + annual_other + annual_rrif, 2)
            taxes = round(calculate_total_taxes(province, total_annual_taxable_income), 2)

            # Calculate GIS reduction after taxes
            if curAge > oas_effective_age:
                gis_reduction = calculate_gis_reduction(annual_cpp, annual_other, annual_rrif)
                annual_gis = max(0, round((adjusted_gis * 12) - gis_reduction, 2))
            elif curAge == oas_effective_age:
                gis_reduction = calculate_gis_reduction(annual_cpp, annual_other, annual_rrif)
                annual_gis = max(0, round((adjusted_gis * oas_receiving_months_in_start_year) - gis_reduction, 2))
            else:
                annual_gis = 0

            gross_annual_income = round(total_annual_taxable_income + annual_gis, 2)

            print(f"annual GIS: {annual_gis}, annual CPP: {annual_cpp}, annual OAS: {annual_oas}, annual RRIF: {annual_rrif}, taxes: {taxes}, cpp_fact: {adjustment_factor} for curAge: {curAge} and start age: {cpp_effective_age} and start month: {delay_mod}\n---------------------------------------")

            cumulative_gis_income += annual_gis
            cumulative_cpp_income += annual_cpp
            cumulative_oas_income += annual_oas
            cumulative_other_income += annual_other
            cumulative_rrif_income += annual_rrif
            cumulative_taxes += taxes
            cumulative_income += gross_annual_income
            
        results.append({
            'start_age': cpp_effective_age - carry_over,
            'start_month': delay_mod,
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
