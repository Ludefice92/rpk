def calculate_progressive_tax(income, brackets):
    """
    Calculate progressive tax based on income brackets.
    
    Args:
        income: Annual income
        brackets: List of tuples (threshold, rate) where threshold is the income level
                 and rate is the tax rate for that bracket
    
    Returns:
        Total tax amount
    """
    total_tax = 0
    previous_threshold = 0
    
    for threshold, rate in brackets:
        if income > threshold:
            taxable_in_bracket = threshold - previous_threshold
            total_tax += taxable_in_bracket * rate
            previous_threshold = threshold
        else:
            taxable_in_bracket = income - previous_threshold
            total_tax += taxable_in_bracket * rate
            break
    else:
        # Income exceeds highest bracket
        if income > previous_threshold:
            taxable_in_bracket = income - previous_threshold
            total_tax += taxable_in_bracket * brackets[-1][1]
    
    return total_tax

def calculate_federal_taxes(income):
    """
    Calculate federal income tax for Canada.
    Tax brackets for 2025 tax year.
    """
    # Federal tax brackets for 2025
    federal_brackets = [
        (16129, 0),           # not taxed on first $16129
        (57375, 0.15),        # 15% on first $57375
        (114750, 0.205),      # 20.5% from $57375 to $114750
        (177882, 0.26),       # 26% from $114750 to $177882
        (253414, 0.29),       # 29% from $177882 to $253414
        (float('inf'), 0.33)  # 33% on income over $253,414
    ]
    
    return calculate_progressive_tax(income, federal_brackets)

def calculate_alberta_taxes(income):
    """
    Calculate Alberta provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # AB tax brackets for 2025
    ab_brackets = [
        (22323, 0),           # not taxed on first $22323
        (151234, 0.1),        # 10% on first $151234
        (181481, 0.12),       # 12% from $151234 to $181481
        (241974, 0.13),       # 13% from $181481 to $241974
        (362961, 0.14),       # 14% from $241974 to $362961
        (float('inf'), 0.15)  # 15 from income over $362961
    ]
    
    return taxable_income * 0.10

def calculate_britishcolumbia_taxes(income):
    """
    Calculate British Columbia provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # BC tax brackets for 2025
    bc_brackets = [
        (19151, 0),            # not taxed on first $19151
        (49279, 0.0506),       # 5.06% on first $49279
        (98560, 0.077),        # 7.7% from $49279 to $98560
        (113158, 0.105),       # 10.5% from $98560 to $113158
        (137407, 0.1229),      # 12.29% from $113158 to $137407
        (186306, 0.147),       # 14.7% from $137407 to $186306
        (259829, 0.168),       # 16.8% from $186306 to $259829
        (float('inf'), 0.205)  # 20.5% on income over $259829
    ]
    
    return calculate_progressive_tax(income, bc_brackets)

def calculate_manitoba_taxes(income):
    """
    Calculate Manitoba provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Manitoba tax brackets for 2025
    mb_brackets = [
        (15780, 0),            # not taxed on first $15780
        (47564, 0.108),        # 10.8% on first $47564
        (101200, 0.1275),      # 12.75% from $47564 to $101200
        (float('inf'), 0.174)  # 17.4% on income over $101200
    ]
    
    return calculate_progressive_tax(income, mb_brackets)

def calculate_newbrunswick_taxes(income):
    """
    Calculate New Brunswick provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # New Brunswick tax brackets for 2025
    nb_brackets = [
        (13396, 0),            # not taxed on first $13396
        (51306, 0.094),        # 9.4% on first $51306
        (102614, 0.14),        # 14% from $51306 to $102614
        (190060, 0.16),        # 16% from $102614 to $190060
        (float('inf'), 0.195)  # 19.5% on income over $190060
    ]
    
    return calculate_progressive_tax(income, nb_brackets)

def calculate_newfoundland_labrador_taxes(income):
    """
    Calculate Newfoundland and Labrador provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Newfoundland and Labrador tax brackets for 2025
    nl_brackets = [
        (11067, 0),            # not taxed on first $11067
        (44192, 0.087),        # 8.7% on first $44192
        (88382, 0.145),        # 14.5% from $44192 to $88382
        (157792, 0.158),       # 15.8% from $88382 to $157792
        (220910, 0.178),       # 17.8% from $157792 to $220910
        (282214, 0.198),       # 14.5% from $220910 to $282214
        (564429, 0.208),       # 15.8% from $282214 to $564429
        (1128858, 0.213),      # 17.8% from $564429 to $1128858
        (float('inf'), 0.218)  # 20.8% on income over $1128858
    ]
    
    return calculate_progressive_tax(income, nl_brackets)

def calculate_novascotia_taxes(income):
    """
    Calculate Nova Scotia provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Nova Scotia tax brackets for 2025
    ns_brackets = [
        (11744, 0),            # not taxed on first $11744
        (30507, 0.0879),       # 8.79% on first $30507
        (61015, 0.1495),       # 14.95% from $30507 to $61015
        (95883, 0.1667),       # 16.67% from $61015 to $95883
        (154650, 0.175),       # 17.5% from $95883 to $154650
        (float('inf'), 0.21)   # 21% on income over $154650
    ]
    
    return calculate_progressive_tax(income, ns_brackets)

def calculate_ontario_taxes(income):
    """
    Calculate Ontario provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Ontario tax brackets for 2025
    on_brackets = [
        (18569, 0),             # not taxed on first $18569
        (52886, 0.0505),        # 5.05% on first $52886
        (105775, 0.0915),       # 9.15% from $52886 to $105775
        (150000, 0.1116),       # 11.16% from $105775 to $150000
        (220000, 0.1216),       # 12.16% from $150000 to $220000
        (float('inf'), 0.1316)  # 13.16% on income over $220000
    ]
    
    return calculate_progressive_tax(income, on_brackets)

def calculate_princeedwardisland_taxes(income):
    """
    Calculate Prince Edward Island provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Prince Edward Island tax brackets for 2025
    pe_brackets = [
        (14650, 0),           # not taxed on first $14650
        (33328, 0.095),       # 9.5% on first $33328
        (64656, 0.1347),      # 13.47% from $33328 to $64656
        (105000, 0.166),      # 16.6% from $64656 to $105000
        (140000, 0.1762),     # 17.62% from $105000 to $140000
        (float('inf'), 0.19)  # 19% on income over $140000
    ]
    
    return calculate_progressive_tax(income, pe_brackets)

def calculate_quebec_taxes(income):
    """
    Calculate Quebec provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Quebec tax brackets for 2025
    qc_brackets = [
        (18571, 0),             # not taxed on first $18571
        (53255, 0.14),          # 14% on first $53255
        (106495, 0.19),         # 19% from $53255 to $106495
        (129590, 0.24),         # 24% from $106495 to $129590
        (float('inf'), 0.2575)  # 25.75% on income over $129590
    ]
    
    return calculate_progressive_tax(income, qc_brackets)

def calculate_saskatchewan_taxes(income):
    """
    Calculate Saskatchewan provincial income tax.
    Tax brackets for 2025 tax year.
    """
    # Saskatchewan tax brackets for 2025
    sk_brackets = [
        (19491, 0),            # not taxed on first $19491
        (53463, 0.105),        # 10.5% on first $53463
        (152750, 0.125),       # 12.5% from $53463 to $152750
        (float('inf'), 0.145)  # 14.5% on income over $152750
    ]
    
    return calculate_progressive_tax(income, sk_brackets)

def calculate_northwestterritories_taxes(income):
    """
    Calculate Northwest Territories territorial income tax.
    Tax brackets for 2025 tax year.
    """
    # Northwest Territories tax brackets for 2025
    nt_brackets = [
        (17842, 0),             # not taxed on first $17842
        (51964, 0.059),         # 5.9% on first $51964
        (103930, 0.086),        # 8.6% from $51964 to $103930
        (168967, 0.122),        # 12.2% from $103930 to $168967
        (float('inf'), 0.1405)  # 14.05% on income over $168967
    ]
    
    return calculate_progressive_tax(income, nt_brackets)

def calculate_nunavut_taxes(income):
    """
    Calculate Nunavut territorial income tax.
    Tax brackets for 2025 tax year.
    """
    # Nunavut tax brackets for 2025
    nu_brackets = [
        (19274, 0),            # not taxed on first $19274
        (54707, 0.04),         # 4% on first $54707
        (109413, 0.07),        # 7% from $54707 to $109413
        (177881, 0.09),        # 9% from $109413 to $177881
        (float('inf'), 0.115)  # 11.5% on income over $177881
    ]
    
    return calculate_progressive_tax(income, nu_brackets)

def calculate_yukon_taxes(income):
    """
    Calculate Yukon territorial income tax.
    Tax brackets for 2025 tax year.
    """
    # Yukon tax brackets for 2025
    yt_brackets = [
        (16129, 0),            # not taxed on first $16129
        (57375, 0.064),        # 6.4% on first $57375
        (114750, 0.09),        # 9% from $57375 to $114750
        (177882, 0.109),       # 10.9% from $114750 to $177882
        (500000, 0.128),       # 12.8% from $173,205 to $500000
        (float('inf'), 0.15)   # 15% on income over $500000
    ]
    
    return calculate_progressive_tax(income, yt_brackets)

def calculate_total_taxes(province, income):
    """
    Calculate total income tax (provincial/territorial + federal) for a given province/territory and income.
    
    Args:
        province: Two-letter province/territory code (e.g., 'ON', 'BC', 'AB')
        income: Annual income
    
    Returns:
        Total tax amount (provincial/territorial + federal)
    """
    if income <= 0: return 0
    if province == 'AB':
        prov_tax = calculate_alberta_taxes(income)
    elif province == 'BC':
        prov_tax = calculate_britishcolumbia_taxes(income)
    elif province == 'MB':
        prov_tax = calculate_manitoba_taxes(income)
    elif province == 'NB':
        prov_tax = calculate_newbrunswick_taxes(income)
    elif province == 'NL':
        prov_tax = calculate_newfoundland_labrador_taxes(income)
    elif province == 'NS':
        prov_tax = calculate_novascotia_taxes(income)
    elif province == 'ON':
        prov_tax = calculate_ontario_taxes(income)
    elif province == 'PE':
        prov_tax = calculate_princeedwardisland_taxes(income)
    elif province == 'QC':
        prov_tax = calculate_quebec_taxes(income)
    elif province == 'SK':
        prov_tax = calculate_saskatchewan_taxes(income)
    elif province == 'NT':
        prov_tax = calculate_northwestterritories_taxes(income)
    elif province == 'NU':
        prov_tax = calculate_nunavut_taxes(income)
    elif province == 'YT':
        prov_tax = calculate_yukon_taxes(income)
    else:
        raise ValueError(f"Unknown province/territory: {province}")
    
    fed_tax = calculate_federal_taxes(income)
    return prov_tax + fed_tax