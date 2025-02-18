import pandas as pd


def calculate_gis_cpp_earnings(start_age=65, cpp_amount=1311.51, gis_amount=1086.88, cpp_deferral_rate=0.0084):
    """
    Compares total earnings when taking CPP at different ages vs. GIS clawbacks.
    Saves results in separate sheets for life expectancies 75, 80, 85, 90, and 95.
    """
    life_expectancy_max = 100
    cpp_start_ages = [65, 66, 67, 68, 69, 70]

    with pd.ExcelWriter("cpp_gis_comparison.xlsx", engine="xlsxwriter") as writer:
            for cpp_start in cpp_start_ages:
                results = []
                # Reset cumulative incomes for each CPP start age
                cumulative_gis_income = 0
                cumulative_cpp_income = 0
                cumulative_income = 0
                deferral_years = max(0, cpp_start - 65)
                cpp_def_factor = 1 + cpp_deferral_rate * (deferral_years * 12)

                for age in range(start_age, life_expectancy_max + 1):
                    if age < cpp_start:
                        gis_adjusted = gis_amount  # Full GIS until CPP starts
                        cpp_income = 0
                    elif age >= 71:
                        gis_adjusted = 0 #because rrif withdrawals start
                        cpp_income = round(cpp_amount * cpp_def_factor, 2)
                    else:
                        cpp_income = round(cpp_amount * cpp_def_factor, 2)
                        gis_reduction = cpp_income * 0.5
                        gis_adjusted = round(max(0, gis_amount - gis_reduction), 2)

                    annual_cpp = round(cpp_income * 12)
                    annual_gis = round(gis_adjusted * 12)
                    annual_income = round(annual_cpp + annual_gis, 2)

                    cumulative_gis_income += annual_gis
                    cumulative_cpp_income += annual_cpp
                    cumulative_income += annual_income
                    results.append(
                        [age, cpp_income, annual_cpp, gis_adjusted, annual_gis, annual_income,
                         cumulative_gis_income, cumulative_cpp_income, cumulative_income])

                df = pd.DataFrame(results,
                              columns=["Age", "CPP_Income", "Annual_CPP", "GIS_Adjusted", "Annual_GIS",
                                       "Annual_Income", "Cumulative_GIS_Income", "Cumulative_CPP_Income", "Cumulative_Income"])
                df.to_excel(writer, sheet_name=f"CPP_Start_Age_{cpp_start}", index=False)

                # Adjust column width
                worksheet = writer.sheets[f"CPP_Start_Age_{cpp_start}"]
                for i, col in enumerate(df.columns):
                    max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_length)

    return "cpp_gis_comparison.xlsx"


# Run the calculation
calculate_gis_cpp_earnings()
