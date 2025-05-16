import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils import format_currency, create_summary_dataframe, calculate_time_saved
from visualizations import create_savings_chart, create_roi_chart, create_time_savings_charts

def generate_report(results):
    summary_df = create_summary_dataframe(results)

    # Create savings and ROI charts
    savings_chart = create_savings_chart(
        results["discipline_savings"],
        results["absenteeism_savings"],
        results["crisis_savings"]
    )
    roi_chart = create_roi_chart(results)

    # Time savings
    num_students = results["num_students"]
    discipline_drop = results["discipline_drop"]
    crisis_drop = results["crisis_drop"]
    absenteeism_drop = results["absenteeism_drop"]

    time_savings = calculate_time_saved(num_students, discipline_drop, crisis_drop)
    teacher_time_saved_weekly = time_savings["teacher"]
    counselor_time_saved_weekly = time_savings["counselor"]

    # Create time savings charts
    weekly_chart_fig, annual_chart_fig = create_time_savings_charts(
        teacher_time_saved_weekly, counselor_time_saved_weekly
    )
    weekly_chart = weekly_chart_fig.to_html(full_html=False, include_plotlyjs=False)
    annual_chart = annual_chart_fig.to_html(full_html=False, include_plotlyjs=False)

    # Build HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Proactive Mental Health Cost Savings Report - {results["institution_name"]}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 900px; margin: auto; }}
            h1, h2, h3 {{ color: #1565C0; }}
            .summary-box {{ background-color: #f5f5f5; border-left: 5px solid #1565C0; padding: 15px; margin-bottom: 20px; }}
            .chart-container {{ height: 340px; margin-bottom: 25px; }}
            .footer {{ font-size: 0.8em; text-align: center; color: #666; margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Proactive Mental Health Cost Savings Report</h1>
            <h2>{results["institution_name"]}</h2>
            <p><em>Generated on {results["timestamp"]}</em></p>
        </div>

        <div class="summary-box">
            <h3>Executive Summary</h3>
            <p>
                Based on a student population of <strong>{results["num_students"]:,}</strong>, 
                your estimated annual cost savings is <strong>{format_currency(results["total_savings"])}</strong>.
            </p>
        </div>

        <h3>Cost Savings Breakdown</h3>
        <div class="chart-container">{savings_chart.to_html(full_html=False, include_plotlyjs=False)}</div>
        <div class="chart-container">{roi_chart.to_html(full_html=False, include_plotlyjs=False)}</div>

        <h3>Team Time Savings</h3>
        <div class="summary-box">
            <p>
                <strong>Teachers:</strong> Estimated <strong>{teacher_time_saved_weekly:.1f} hours per week</strong><br>
                <strong>Counselors:</strong> Estimated <strong>{counselor_time_saved_weekly:.1f} hours per week</strong>
            </p>
            <p>These time savings can be redirected toward proactive student support and improving school climate.</p>
        </div>

        <h4>Weekly Time Savings</h4>
        <div class="chart-container">{weekly_chart}</div>

        <h4>Annual Time Savings</h4>
        <div class="chart-container">{annual_chart}</div>

        <div class="footer">
            <p>Powered by the Proactive Mental Health Cost Savings Calculator • meetmaro.com</p>
        </div>
    </body>
    </html>
    """
    return html_content
