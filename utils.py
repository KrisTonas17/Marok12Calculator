import pandas as pd

def calculate_time_saved(num_students, discipline_drop, crisis_drop, referral_drop=0.25):
    """
    Estimate weekly time saved for educators and counselors.
    """
    teacher_discipline_hours = 3.5
    counselor_discipline_hours = 2.5
    teacher_crisis_hours = 1.5
    counselor_crisis_hours = 6
    teacher_referral_hours = 0.5  # 30 minutes per referral
    counselor_referral_hours = 1.5  # Average of 1–2 hours per referral

    time_saved = {
        "teacher": round(
            (teacher_discipline_hours * discipline_drop) +
            (teacher_crisis_hours * crisis_drop) +
            (teacher_referral_hours * referral_drop),
            1
        ),
        "counselor": round(
            (counselor_discipline_hours * discipline_drop) +
            (counselor_crisis_hours * crisis_drop) +
            (counselor_referral_hours * referral_drop),
            1
        )
    }
    return time_saved


def calculate_savings(
    num_students, 
    discipline_rate, 
    absenteeism_rate, 
    crisis_rate,
    discipline_drop, 
    absenteeism_drop, 
    crisis_drop,
    discipline_cost, 
    absenteeism_cost, 
    crisis_cost
):
    """
    Calculate the potential savings from reducing disciplinary issues,
    chronic absenteeism, and crisis management needs.
    
    Parameters:
    -----------
    num_students : int
        Number of students in the school/district
    discipline_rate : float
        Current rate of disciplinary issues (as a decimal)
    absenteeism_rate : float
        Current rate of chronic absenteeism (as a decimal)
    crisis_rate : float
        Current rate of crisis management needs (as a decimal)
    discipline_drop : float
        Estimated drop in disciplinary issues (as a decimal)
    absenteeism_drop : float
        Estimated drop in chronic absenteeism (as a decimal)
    crisis_drop : float
        Estimated drop in crisis management needs (as a decimal)
    discipline_cost : float
        Cost per disciplinary issue ($)
    absenteeism_cost : float
        Cost per chronic absenteeism case ($)
    crisis_cost : float
        Cost per crisis management case ($)
    
    Returns:
    --------
    tuple
        (discipline_savings, absenteeism_savings, crisis_savings, total_savings)
    """
    # Disciplinary Savings Calculation
    discipline_savings = num_students * discipline_rate * discipline_drop * discipline_cost

    # Absenteeism Savings Calculation
    absenteeism_savings = num_students * absenteeism_rate * absenteeism_drop * absenteeism_cost

    # Crisis Management Savings Calculation
    crisis_savings = num_students * crisis_rate * crisis_drop * crisis_cost

    # Total Savings Calculation
    total_savings = discipline_savings + absenteeism_savings + crisis_savings
    
    return discipline_savings, absenteeism_savings, crisis_savings, total_savings

def format_currency(value):
    """Format a value as currency with commas and no decimal places."""
    return f"${value:,.0f}"

def create_summary_dataframe(results):
    """
    Create a summary dataframe from the results dictionary.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing calculation results
    
    Returns:
    --------
    pd.DataFrame
        Summary dataframe
    """
    summary_data = {
        "Category": ["Disciplinary Issues", "Chronic Absenteeism", "Crisis Management", "Total"],
        "Savings": [
            results["discipline_savings"],
            results["absenteeism_savings"], 
            results["crisis_savings"],
            results["total_savings"]
        ],
        "Savings_Formatted": [
            format_currency(results["discipline_savings"]),
            format_currency(results["absenteeism_savings"]),
            format_currency(results["crisis_savings"]),
            format_currency(results["total_savings"])
        ],
        "Percentage": [
            results["discipline_savings"] / results["total_savings"] * 100 if results["total_savings"] > 0 else 0,
            results["absenteeism_savings"] / results["total_savings"] * 100 if results["total_savings"] > 0 else 0,
            results["crisis_savings"] / results["total_savings"] * 100 if results["total_savings"] > 0 else 0,
            100.0
        ]
    }
    
    return pd.DataFrame(summary_data)

def calculate_current_costs(
    num_students, 
    discipline_rate, 
    absenteeism_rate, 
    crisis_rate,
    discipline_cost, 
    absenteeism_cost, 
    crisis_cost
):
    """
    Calculate the current costs associated with disciplinary issues,
    chronic absenteeism, and crisis management needs.
    
    Parameters:
    -----------
    Same as calculate_savings function
    
    Returns:
    --------
    tuple
        (discipline_current, absenteeism_current, crisis_current, total_current)
    """
    # Current cost calculations
    discipline_current = num_students * discipline_rate * discipline_cost
    absenteeism_current = num_students * absenteeism_rate * absenteeism_cost
    crisis_current = num_students * crisis_rate * crisis_cost
    total_current = discipline_current + absenteeism_current + crisis_current
    
    return discipline_current, absenteeism_current, crisis_current, total_current

def calculate_projected_costs(
    num_students, 
    discipline_rate, 
    absenteeism_rate, 
    crisis_rate,
    discipline_drop, 
    absenteeism_drop, 
    crisis_drop,
    discipline_cost, 
    absenteeism_cost, 
    crisis_cost
):
    """
    Calculate the projected costs after implementing improvements.
    
    Parameters:
    -----------
    Same as calculate_savings function
    
    Returns:
    --------
    tuple
        (discipline_projected, absenteeism_projected, crisis_projected, total_projected)
    """
    # Current costs
    discipline_current, absenteeism_current, crisis_current, total_current = calculate_current_costs(
        num_students, discipline_rate, absenteeism_rate, crisis_rate,
        discipline_cost, absenteeism_cost, crisis_cost
    )
    
    # Projected costs after improvement
    discipline_projected = discipline_current * (1 - discipline_drop)
    absenteeism_projected = absenteeism_current * (1 - absenteeism_drop)
    crisis_projected = crisis_current * (1 - crisis_drop)
    total_projected = discipline_projected + absenteeism_projected + crisis_projected
    
    return discipline_projected, absenteeism_projected, crisis_projected, total_projected
