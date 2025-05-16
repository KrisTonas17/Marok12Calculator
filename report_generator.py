import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils import format_currency, create_summary_dataframe
from visualizations import create_savings_chart, create_roi_chart, create_time_savings_charts

def generate_report(results):
    """
    Generate an HTML report based on the calculation results.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing calculation results
    
    Returns:
    --------
    str
        HTML content for the report
    """
    # Create summary dataframe
    summary_df = create_summary_dataframe(results)

    # Create charts
    savings_chart = create_savings_chart(
        results["discipline_savings"],
        results["absenteeism_savings"],
        results["crisis_savings"]
    )
    roi_chart = create_roi_chart(results)

    # Calculate time savings
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

    # Generate charts
    weekly_chart_fig, annual_chart_fig = create_time_savings_charts(
        teacher_time_saved_weekly, counselor_time_saved_weekly
    )

    weekly_chart = weekly_chart_fig.to_html(full_html=False, include_plotlyjs=False)
    annual_chart = annual_chart_fig.to_html(full_html=False, include_plotlyjs=False)

    # Format the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Proactive Mental Health Cost Savings Report - {results["institution_name"]}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 10px;
                border-bottom: 2px solid #1565C0;
            }}
            .logo {{
                background-color: #1565C0;
                color: white;
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
            }}
            h1, h2, h3 {{
                color: #1565C0;
            }}
            .summary-box {{
                background-color: #f5f5f5;
                border-left: 5px solid #1565C0;
                padding: 15px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #1565C0;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .chart-container {{
                width: 100%;
                height: 350px;
                margin-bottom: 30px;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 10px;
            }}
            .total-row {{
                font-weight: bold;
                background-color: #e6f2ff !important;
            }}
            .methodology {{
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">
                <h1>Proactive Mental Health Cost Savings Report</h1>
                <p>Data-driven insights for implementing mental health resources in schools</p>
            </div>
            <h2>{results["institution_name"]}</h2>
            <p>Report generated on {results["timestamp"]}</p>
        </div>

        <div class="summary-box">
            <h3>Executive Summary</h3>
            <p>Based on a student population of <strong>{results["num_students"]:,}</strong>, 
            our analysis indicates a potential total annual savings of 
            <strong>{format_currency(results["total_savings"])}</strong> through strategic improvements 
            in three key areas.</p>
        </div>

        <h3>Savings Breakdown</h3>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Current Rate</th>
                    <th>Improvement</th>
                    <th>Cost Per Instance</th>
                    <th>Estimated Savings</th>
                    <th>% of Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Disciplinary Issues</td>
                    <td>{results["discipline_rate"]*100:.1f}%</td>
                    <td>{results["discipline_drop"]*100:.1f}%</td>
                    <td>{format_currency(results["discipline_cost"])}</td>
                    <td>{format_currency(results["discipline_savings"])}</td>
                    <td>{results["discipline_savings"]/results["total_savings"]*100:.1f}%</td>
                </tr>
                <tr>
                    <td>Chronic Absenteeism</td>
                    <td>{results["absenteeism_rate"]*100:.1f}%</td>
                    <td>{results["absenteeism_drop"]*100:.1f}%</td>
                    <td>{format_currency(results["absenteeism_cost"])}</td>
                    <td>{format_currency(results["absenteeism_savings"])}</td>
                    <td>{results["absenteeism_savings"]/results["total_savings"]*100:.1f}%</td>
                </tr>
                <tr>
                    <td>Crisis Management</td>
                    <td>{results["crisis_rate"]*100:.1f}%</td>
                    <td>{results["crisis_drop"]*100:.1f}%</td>
                    <td>{format_currency(results["crisis_cost"])}</td>
                    <td>{format_currency(results["crisis_savings"])}</td>
                    <td>{results["crisis_savings"]/results["total_savings"]*100:.1f}%</td>
                </tr>
                <tr class="total-row">
                    <td>Total</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>{format_currency(results["total_savings"])}</td>
                    <td>100.0%</td>
                </tr>
            </tbody>
        </table>

        <div class="chart-container" id="savings-chart">
            {savings_chart.to_html(full_html=False, include_plotlyjs=False)}
        </div>

        <div class="chart-container" id="roi-chart">
            {roi_chart.to_html(full_html=False, include_plotlyjs=False)}
        </div>

        <div class="methodology">
            <h3>Calculation Methodology</h3>
            <p>The savings calculations are based on the following formulas:</p>
            <ul>
                <li><strong>Disciplinary Savings</strong> = Students × Rate × Drop × Cost</li>
                <li><strong>Absenteeism Savings</strong> = Students × Rate × Drop × Cost</li>
                <li><strong>Crisis Management Savings</strong> = Students × Rate × Drop × Cost</li>
            </ul>
            <p>Default values reflect national averages of schools implementing proactive mental health strategies.</p>
        </div>

        <div class="additional-resources">
            <h3>Additional Resources</h3>
            <p>Tools like Maro (<a href="https://meetmaro.com" target="_blank">meetmaro.com</a>) support screening, care navigation, and planning.</p>
        </div>

        <h3>Team Time Savings</h3>
        <div class="summary-box">
            <p>
                <strong>Teachers:</strong> Estimated weekly time savings of <strong>{teacher_time_saved_weekly:.1f} hours</strong><br>
                <strong>Counselors:</strong> Estimated weekly time savings of <strong>{counselor_time_saved_weekly:.1f} hours</strong>
            </p>
        </div>

        <div class="chart-container" id="weekly-time-chart">
            {weekly_chart}
        </div>

        <div class="chart-container" id="annual-time-chart">
            {annual_chart}
        </div>

        <div class="footer">
            <p>This report was generated by the Proactive Mental Health Cost Savings Calculator.</p>
        </div>
    </body>
    </html>
    """
    return html_content
