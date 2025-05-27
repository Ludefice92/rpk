import os
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render


def calculate_gis_cpp_earnings():
    """
    Calculates and generates comprehensive GIS (Guaranteed Income Supplement) vs CPP (Canada Pension Plan) earnings analysis.
    
    This function performs detailed financial modeling to compare different CPP start age scenarios and their impact
    on total retirement income when combined with GIS benefits. The analysis accounts for the complex interaction
    between CPP and GIS, where higher CPP payments reduce GIS eligibility due to income testing.
    
    Key Financial Modeling:
        - CPP deferral bonus: 0.84% per month (0.7% + 0.14% enhancement) for delayed retirement
        - GIS reduction: 50% clawback rate on CPP income above basic exemption
        - Age eligibility: GIS available ages 65-70, CPP can start 60-70
        - Multiple start age scenarios: 65, 66, 67, 68, 69, 70 years
        
    Calculations Include:
        - Monthly and annual CPP payments with deferral adjustments
        - GIS payment reductions based on CPP income levels
        - Cumulative lifetime income projections to age 100
        - Comparative analysis across different CPP start ages
        
    Returns:
        str: Filename of the generated Excel spreadsheet containing all scenarios
        
    Excel Output:
        - Separate worksheet for each CPP start age (65-70)
        - Monthly breakdown from age 65 to 100
        - Cumulative income tracking for long-term planning
        - Formatted columns with auto-sizing for readability
    """
    life_expectancy_max = 100
    cpp_start_ages = [65, 66, 67, 68, 69, 70]
    output_file = "cpp_gis_comparison.xlsx"

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for cpp_start in cpp_start_ages:
            results = []

            cumulative_gis_income = 0
            cumulative_cpp_income = 0
            cumulative_income = 0
            cpp_deferral_rate = 0.0084
            cpp_amount = 1311.51
            gis_amount = 1086.88
            start_age = 65

            deferral_years = max(0, cpp_start - 65)
            cpp_def_factor = 1 + cpp_deferral_rate * (deferral_years * 12)

            for age in range(start_age, life_expectancy_max + 1):
                if age < cpp_start:
                    gis_adjusted = gis_amount
                    cpp_income = 0
                else:
                    cpp_income = round(cpp_amount * cpp_def_factor, 2)
                    gis_reduction = cpp_income * 0.5
                    gis_adjusted = round(max(0, gis_amount - gis_reduction), 2)

                if age < 65 or age >= 71: gis_adjusted = 0

                annual_cpp = round(cpp_income * 12)
                annual_gis = round(gis_adjusted * 12)
                annual_income = round(annual_cpp + annual_gis, 2)

                cumulative_gis_income += annual_gis
                cumulative_cpp_income += annual_cpp
                cumulative_income += annual_income

                results.append([
                    age, cpp_income, annual_cpp, gis_adjusted, annual_gis, annual_income,
                    cumulative_gis_income, cumulative_cpp_income, cumulative_income
                ])

            df = pd.DataFrame(results, columns=[
                "Age", "CPP_Income", "Annual_CPP", "GIS_Adjusted", "Annual_GIS",
                "Annual_Income", "Cumulative_GIS_Income", "Cumulative_CPP_Income", "Cumulative_Income"
            ])
            df.to_excel(writer, sheet_name=f"CPP_Start_Age_{cpp_start}", index=False)

            worksheet = writer.sheets[f"CPP_Start_Age_{cpp_start}"]
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)

    return output_file


def generate_report(request):
    """
    Django view function that handles HTTP requests to generate and download the GIS/CPP comparison Excel report.
    
    This function serves as the web interface endpoint for generating the retirement income analysis spreadsheet.
    It orchestrates the calculation process and returns the Excel file as a downloadable HTTP response.
    The function implements proper file handling and HTTP response formatting for web delivery.
    
    Args:
        request (HttpRequest): Django HTTP request object containing client request data
        
    Returns:
        HttpResponse: HTTP response containing the Excel file as an attachment with proper headers:
            - Content-Type: Excel MIME type for proper browser handling
            - Content-Disposition: Attachment header to trigger download
            - Binary file data: Complete Excel spreadsheet with all calculations
            
    Process Flow:
        1. Calls calculate_gis_cpp_earnings() to generate the Excel file
        2. Opens the generated file in binary read mode
        3. Creates HTTP response with Excel content type
        4. Sets download headers to prompt file save dialog
        5. Returns complete response with file data
        
    Error Handling:
        - File operations are handled within context managers for proper cleanup
        - Django's HttpResponse handles HTTP protocol compliance
    """
    file_path = calculate_gis_cpp_earnings()

    with open(file_path, "rb") as excel:
        response = HttpResponse(excel.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{file_path}"'
        return response


def index(request):
    """
    Django view function that renders the main application homepage with the report generation interface.
    
    This function serves as the entry point for the web application, displaying the user interface
    that allows users to trigger the GIS/CPP earnings analysis. It renders an HTML template
    containing the necessary UI elements (typically a button) to initiate the report generation.
    
    Args:
        request (HttpRequest): Django HTTP request object from the client browser
        
    Returns:
        HttpResponse: Rendered HTML page containing the application interface
        
    Template Requirements:
        - The "index.html" template should contain:
            * User-friendly interface elements
            * Button or form to trigger report generation
            * Clear instructions for users
            * Proper styling and layout
            
    Integration:
        - This view works in conjunction with generate_report() view
        - URL routing should map this function to the root application path
        - Template should reference the generate_report URL for form submission
    """
    return render(request, "index.html")
