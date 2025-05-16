import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_current_costs, calculate_projected_costs, format_currency

def create_savings_chart(discipline_savings, absenteeism_savings, crisis_savings):
    labels = ['Disciplinary Issues', 'Chronic Absenteeism', 'Crisis Management']
    values = [discipline_savings, absenteeism_savings, crisis_savings]

    fig = px.pie(
        names=labels,
        values=values,
        title='Savings Breakdown by Category',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )

    total_savings = sum(values)
    fig.update_layout(
        annotations=[dict(
            text=f'Total<br>${total_savings:,.0f}',
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )]
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent} of total savings<extra></extra>'
    )

    return fig

def create_comparison_chart(
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
    discipline_current, absenteeism_current, crisis_current, total_current = calculate_current_costs(
        num_students, discipline_rate, absenteeism_rate, crisis_rate,
        discipline_cost, absenteeism_cost, crisis_cost
    )

    discipline_projected, absenteeism_projected, crisis_projected, total_projected = calculate_projected_costs(
        num_students, discipline_rate, absenteeism_rate, crisis_rate,
        discipline_drop, absenteeism_drop, crisis_drop,
        discipline_cost, absenteeism_cost, crisis_cost
    )

    categories = ['Disciplinary Issues', 'Chronic Absenteeism', 'Crisis Management', 'Total']
    current_costs = [discipline_current, absenteeism_current, crisis_current, total_current]
    projected_costs = [discipline_projected, absenteeism_projected, crisis_projected, total_projected]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=current_costs,
        name='Current Costs',
        marker_color='#1565C0',
        text=[format_currency(cost) for cost in current_costs],
        textposition='auto',
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=projected_costs,
        name='Projected Costs After Improvement',
        marker_color='#90CAF9',
        text=[format_currency(cost) for cost in projected_costs],
        textposition='auto',
    ))

    fig.update_layout(
        title='Current vs. Projected Costs Comparison',
        xaxis_title='Category',
        yaxis_title='Cost ($)',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(tickprefix="$", tickformat=",.0f")
    )

    return fig

def create_roi_chart(results):
    discipline_current = results["num_students"] * results["discipline_rate"] * results["discipline_cost"]
    absenteeism_current = results["num_students"] * results["absenteeism_rate"] * results["absenteeism_cost"]
    crisis_current = results["num_students"] * results["crisis_rate"] * results["crisis_cost"]

    discipline_projected = discipline_current * (1 - results["discipline_drop"])
    absenteeism_projected = absenteeism_current * (1 - results["absenteeism_drop"])
    crisis_projected = crisis_current * (1 - results["crisis_drop"])

    categories = ['Disciplinary Issues', 'Chronic Absenteeism', 'Crisis Management']
    current = [discipline_current, absenteeism_current, crisis_current]
    projected = [discipline_projected, absenteeism_projected, crisis_projected]
    savings = [results["discipline_savings"], results["absenteeism_savings"], results["crisis_savings"]]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Current Costs',
        x=categories,
        y=current,
        marker_color='#1565C0',
        text=[format_currency(val) for val in current],
        textposition='auto',
    ))

    fig.add_trace(go.Bar(
        name='Projected Costs',
        x=categories,
        y=projected,
        marker_color='#90CAF9',
        text=[format_currency(val) for val in projected],
        textposition='auto',
    ))

    fig.add_trace(go.Scatter(
        name='Savings',
        x=categories,
        y=current,
        mode='markers',
        marker=dict(color='#4CAF50', size=16, symbol='star'),
        text=[format_currency(val) for val in savings],
        hovertemplate='%{text} savings<extra></extra>'
    ))

    fig.update_layout(
        title='Cost Reduction Analysis',
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(tickprefix="$", tickformat=",.0f")
    )

    return fig

def create_time_savings_charts(teacher_weekly, counselor_weekly):
    teacher_annual = teacher_weekly * 36
    counselor_annual = counselor_weekly * 36

    # Weekly chart
    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Bar(
        x=["Teachers", "Counselors"],
        y=[teacher_weekly, counselor_weekly],
        name="Weekly Time Saved",
        marker_color="#1f77b4"
    ))
    fig_weekly.update_layout(
        title="Weekly Team Time Savings",
        yaxis_title="Hours Saved per Week",
        height=300
    )

    # Annual chart
    fig_annual = go.Figure()
    fig_annual.add_trace(go.Bar(
        x=["Teachers", "Counselors"],
        y=[teacher_annual, counselor_annual],
        name="Annual Time Saved",
        marker_color="#2ca02c"
    ))
    fig_annual.update_layout(
        title="Annual Team Time Savings",
        yaxis_title="Hours Saved per Year",
        height=300
    )

    return fig_weekly, fig_annual
