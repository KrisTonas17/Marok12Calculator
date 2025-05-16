
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils import format_currency, create_summary_dataframe
from visualizations import create_savings_chart, create_roi_chart, create_time_savings_charts

def generate_report(results):
    summary_df = create_summary_dataframe(results)

    # Charts
    savings_chart = create_savings_chart(
        results["discipline_savings"],
        results["absenteeism_savings"],
        results["crisis_savings"]
    )
    roi_chart = create_roi_chart(results)

    # Time savings calculations
    num_students = results["num_students"]
    discipline_drop = results["discipline_drop"]
    absenteeism_drop = results["absenteeism_drop"]
    crisis_drop = results["crisis_drop"]

    teacher_time_saved_weekly = (
        num_students * discipline_drop * 0.25 +
        num_students * crisis_drop * 0.33 +
        num_students * absenteeism_drop * 0.25
    )
    counselor_time_saved_weekly = (
        num_students * discipline_drop * 0.33 +
        num_students * crisis_drop * 0.5 +
        num_students * absenteeism_drop * 0.33
    )
    weekly_chart_fig, annual_chart_fig = create_time_savings_charts(
        teacher_time_saved_weekly, counselor_time_saved_weekly
    )
    weekly_chart = weekly_chart_fig.to_html(full_html=False, include_plotlyjs=False)
    annual_chart = annual_chart_fig.to_html(full_html=False, include_plotlyjs=False)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Proactive Mental Health Cost Savings Report - {results["institution_name"]}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial; padding: 20px; color: #333; max-width: 1000px; margin: auto; }}
            h1, h2, h3 {{ color: #1565C0; }}
            .summary-box {{ background: #f5f5f5; border-left: 5px solid #1565C0; padding: 15px; margin-bottom: 20px; }}
            .chart-container {{ width: 100%; height: 360px; margin-bottom: 30px; }}
            .footer {{ margin-top: 30px; font-size: 0.9em; color: #666; border-top: 1px solid #ddd; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>Proactive Mental Health Cost Savings Report</h1>
        <h2>{results["institution_name"]}</h2>
        <p>Report generated on {results["timestamp"]}</p>

        <div class="summary-box">
            <h3>Executive Summary</h3>
            <p>Potential annual savings: <strong>{format_currency(results["total_savings"])}</strong> based on {results["num_students"]:,} students.</p>
        </div>

        <div class="chart-container">{savings_chart.to_html(full_html=False, include_plotlyjs=False)}</div>
        <div class="chart-container">{roi_chart.to_html(full_html=False, include_plotlyjs=False)}</div>

        <h3>Team Time Savings</h3>
        <div class="summary-box">
            <p><strong>Teachers:</strong> {teacher_time_saved_weekly:.1f} hours/week &bull; {(teacher_time_saved_weekly * 36):.1f} hours/year</p>
            <p><strong>Counselors:</strong> {counselor_time_saved_weekly:.1f} hours/week &bull; {(counselor_time_saved_weekly * 36):.1f} hours/year</p>
            <p>These hours can be reinvested into proactive student support and fostering a healthy school climate.</p>
        </div>
        <div class="chart-container">{weekly_chart}</div>
        <div class="chart-container">{annual_chart}</div>

        <div class="footer">
            <p>This report was generated using the Maro K-12 Mental Health ROI Calculator.</p>
        </div>
    </body>
    </html>
    """
    return html_content
