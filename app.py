import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_savings
from visualizations import create_savings_chart, create_comparison_chart, create_time_savings_charts
from report_generator import generate_report
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Proactive Mental Health Cost Savings Calculator for K-12 Schools",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("Proactive Mental Health Cost Savings Calculator for K-12 Schools")
st.markdown("""
This calculator helps schools and districts estimate potential cost savings from implementing proactive mental health 
screening, education, and resources to reduce disciplinary issues, chronic absenteeism, and crisis management needs. 
Please note, the estimates provided are based on national assumptions and are intended to offer a general overview 
rather than specific outcomes for your school, as precise predictions are not feasible.

**Additional Resource:** Tools like Maro ([meetmaro.com](https://meetmaro.com)) can support your efforts by making 
mental health screening, care navigation, access to community resources, and lesson planning easier and more 
accessible in one platform.
""")

# Display hero image
st.markdown("""
<div style="text-align: center">
    <svg width="100%" height="120px" viewBox="0 0 800 120">
        <rect width="100%" height="100%" fill="#1565C0" />
        <text x="50%" y="50%" font-family="Arial" font-size="24px" fill="white" text-anchor="middle" dominant-baseline="middle">
            Proactive Mental Health Cost Savings Estimator
        </text>
        <text x="50%" y="75%" font-family="Arial" font-size="16px" fill="white" text-anchor="middle" dominant-baseline="middle">
            Helping schools optimize resources through preventative mental health programs
        </text>
    </svg>
</div>
""", unsafe_allow_html=True)

# Main content in a single column layout
st.header("Cost Savings Calculator")

# Institution Information
st.subheader("Institution Information")
col_inst1, col_inst2 = st.columns([1, 1])
with col_inst1:
    institution_name = st.text_input("Institution Name", "My School District")
with col_inst2:
    num_students = st.number_input("Number of Students", min_value=1, value=1000, step=100)

# Create a visual separator
st.markdown("---")

# Current Statistics
st.subheader("Current Statistics")
st.markdown("*Enter your institution's current rates or use the default national averages*")

col_a, col_b, col_c = st.columns(3)
with col_a:
    discipline_rate = st.number_input("Current Disciplinary Rate (%)", 
                                  min_value=0.0, max_value=100.0, value=10.0, step=0.5, key="main_discipline_rate") / 100
with col_b:
    absenteeism_rate = st.number_input("Current Chronic Absenteeism Rate (%)", 
                                   min_value=0.0, max_value=100.0, value=15.0, step=0.5, key="main_absenteeism_rate") / 100
with col_c:
    crisis_rate = st.number_input("Current Crisis Management Rate (%)", 
                              min_value=0.0, max_value=100.0, value=5.0, step=0.5, key="main_crisis_rate") / 100

# Cost Per Instance
st.subheader("Cost Per Instance")
st.markdown("*Enter your institution's cost per case or use the default estimates*")

col_d, col_e, col_f = st.columns(3)
with col_d:
    discipline_cost = st.number_input("Cost Per Disciplinary Issue ($)", 
                                  min_value=0, value=250, step=10, key="main_discipline_cost")
with col_e:
    absenteeism_cost = st.number_input("Cost Per Chronic Absenteeism Case ($)", 
                                   min_value=0, value=1200, step=100, key="main_absenteeism_cost")
with col_f:
    crisis_cost = st.number_input("Cost Per Crisis Management Case ($)", 
                              min_value=0, value=10000, step=1000, key="main_crisis_cost")

# Estimated Improvements
st.subheader("Estimated Improvements")
st.markdown("*These values are preset to national averages when implementing proactive mental health resources. You can adjust them based on your expectations.*")

col_g, col_h, col_i = st.columns(3)
with col_g:
    discipline_drop = st.slider("Drop in Disciplinary Issues (%)", 
                             min_value=0, max_value=100, value=38, step=1, key="main_discipline_drop") / 100
with col_h:
    absenteeism_drop = st.slider("Drop in Chronic Absenteeism (%)", 
                              min_value=0, max_value=100, value=20, step=1, key="main_absenteeism_drop") / 100
with col_i:
    crisis_drop = st.slider("Drop in Crisis Management (%)", 
                         min_value=0, max_value=100, value=30, step=1, key="main_crisis_drop") / 100

# Create a visual separator
st.markdown("---")

# Calculator section
st.subheader("Calculate Your Potential Savings")

# Calculate button
calculate_button = st.button("Calculate Potential Savings", key="calculate_button") 
if calculate_button:
    # Perform calculations
    discipline_savings, absenteeism_savings, crisis_savings, total_savings = calculate_savings(
        num_students, discipline_rate, absenteeism_rate, crisis_rate,
        discipline_drop, absenteeism_drop, crisis_drop,
        discipline_cost, absenteeism_cost, crisis_cost
    )
    
    # Store results in session state
    st.session_state.results = {
        "discipline_savings": discipline_savings,
        "absenteeism_savings": absenteeism_savings,
        "crisis_savings": crisis_savings,
        "total_savings": total_savings,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "institution_name": institution_name,
        "num_students": num_students,
        "discipline_rate": discipline_rate,
        "absenteeism_rate": absenteeism_rate,
        "crisis_rate": crisis_rate,
        "discipline_drop": discipline_drop,
        "absenteeism_drop": absenteeism_drop,
        "crisis_drop": crisis_drop,
        "discipline_cost": discipline_cost,
        "absenteeism_cost": absenteeism_cost,
        "crisis_cost": crisis_cost
    }

    st.session_state["report_ready"] = True
    
    # Display results
    st.subheader("Savings Summary")
    
    # Create metrics in rows
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Disciplinary Savings", f"${discipline_savings:,.0f}")
    metric_col2.metric("Absenteeism Savings", f"${absenteeism_savings:,.0f}")
    metric_col3.metric("Crisis Management Savings", f"${crisis_savings:,.0f}")
    
    st.metric("Total Estimated Annual Savings", f"${total_savings:,.0f}")
    
    # Create and display charts
    fig = create_savings_chart(discipline_savings, absenteeism_savings, crisis_savings)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show comparison chart
    compare_fig = create_comparison_chart(
        num_students, discipline_rate, absenteeism_rate, crisis_rate,
        discipline_drop, absenteeism_drop, crisis_drop,
        discipline_cost, absenteeism_cost, crisis_cost
    )
    st.plotly_chart(compare_fig, use_container_width=True)
    
    from utils import calculate_time_saved  # Make sure this is at the top of the file

    # Calculate team time savings (per educator/counselor)
    time_saved = calculate_time_saved(num_students, discipline_drop, crisis_drop)
    teacher_time_saved = time_saved["teacher"]
    counselor_time_saved = time_saved["counselor"]

# Display team time savings section
    st.markdown("### 👥 Team Time Savings")
    st.markdown("""
    Beyond financial savings, implementing proactive mental health strategies can lead to meaningful **time savings** for your staff.
    """)
    st.markdown(f"""
    - **Teachers** may save an estimated **{teacher_time_saved:.1f} hours per week** by reducing time spent on classroom disruptions, crisis management, and referrals.
    - **Counselors** may save an estimated **{counselor_time_saved:.1f} hours per week** by decreasing time spent on disciplinary actions, crisis interventions, and processing referrals.
    
    These reclaimed hours can be redirected to proactive student support, instructional planning, and fostering a healthy school climate.
    """)

    from visualizations import create_time_savings_charts

    weekly_fig, annual_fig = create_time_savings_charts(teacher_time_saved, counselor_time_saved)
    st.plotly_chart(weekly_fig, use_container_width=True)
    st.plotly_chart(annual_fig, use_container_width=True)

    # Generate report button
if st.session_state.get("report_ready"):
    st.subheader("Generate Your Report")

    try:
        report_html = generate_report(st.session_state.results)

        st.download_button(
            label="📄 Download Report",
            data=report_html,
            file_name=f"savings_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            key="download_report_button"
        )
    except Exception as e:
        st.error(f"❌ An error occurred while generating the report: {e}")


    

# Contact Form Section
# Contact Form Section
st.markdown("---")
st.subheader("Contact Us")
st.markdown("""
If your district is looking to take a more proactive approach to mental health, please fill out the contact form below. 
Kris from the Maro team will reach out to schedule a time to discuss affordable resources tailored to your district's needs.
""")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    district = st.text_input("School District")
    email = st.text_input("Email Address")
    submitted = st.form_submit_button("Request Information")

    if submitted:
        import requests

        data = {
            "name": name,
            "district": district,
            "email": email,
        }

        try:
            response = requests.post("https://getform.io/f/bpjndonb", data=data)
            if response.status_code == 200:
                st.success("✅ Thank you! Kris from Maro will reach out to you soon.")
            else:
                st.error("❌ Something went wrong. Please try again later.")
        except Exception as e:
            st.error(f"❌ Error: {e}")



# Information section
st.header("About the Calculator")
st.markdown("""
### How It Works

This calculator estimates potential cost savings based on implementing proactive mental health resources:

1. **Disciplinary Issues**: Each disciplinary incident costs schools in staff time, 
   administrative resources, and potential loss of instructional time. Proactive mental health
   resources have been shown to reduce these incidents through early intervention.

2. **Chronic Absenteeism**: Student absences impact funding, require intervention 
   resources, and affect overall educational outcomes. Mental health support helps address
   underlying factors contributing to attendance problems.

3. **Crisis Management**: Behavioral crises require significant resources, 
   specialized staff, and can disrupt the educational environment. Preventative approaches
   can significantly reduce the frequency and severity of crises.

### Calculation Methodology

For each category, we calculate:
```
Savings = Number of Students × Current Rate × Expected Drop × Cost Per Incident
```

The calculator uses national averages for expected improvements based on research on
proactive mental health programs in schools, but allows for customization based on 
your specific context and expectations.

### Using The Results

The estimated savings can help:
- Justify investments in proactive mental health programs
- Allocate resources more effectively
- Demonstrate potential return on investment (ROI)
- Facilitate data-driven decision making about student wellbeing initiatives
""")

st.info("""
**Note**: Actual savings may vary based on implementation quality, 
consistency, and other contextual factors. This calculator provides 
estimates to support decision-making but should be used alongside 
other evaluation methods.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    Proactive Mental Health Cost Savings Calculator | Developed for School Administrators and District Leaders | Product of <a href="https://meetmaro.com" target="_blank">meetmaro.com</a>
</div>
""", unsafe_allow_html=True)
