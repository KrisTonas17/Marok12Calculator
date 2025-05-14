# Proactive Mental Health Cost Savings Calculator

This application helps schools and districts estimate potential cost savings from implementing proactive mental health screening, education, and resources to reduce disciplinary issues, chronic absenteeism, and crisis management needs.

## Features

- Calculate potential savings based on your institution's data
- Visualize savings with interactive charts
- Generate downloadable reports
- Contact form integration with Maro team

## Deployment to Streamlit Cloud

To deploy this application to Streamlit Community Cloud:

1. Create a GitHub repository and push this code
2. Visit [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file path (app.py)
6. Click "Deploy"

### Required Files

- `app.py` - Main application code
- `requirements.txt` - Rename `streamlit_requirements.txt` to `requirements.txt` before GitHub upload
- `.streamlit/config.toml` - Configuration settings

### Email Configuration (Optional)

For the contact form email functionality to work in production:

1. Create a `.streamlit/secrets.toml` file on Streamlit Cloud with your email credentials:
   ```toml
   [email]
   username = "your-email@example.com"
   password = "your-app-password"
   smtp_server = "smtp.gmail.com"
   smtp_port = 465
   ```

2. Uncomment the email sending code in `email_sender.py`

## Local Development

To run this application locally:

```bash
pip install -r streamlit_requirements.txt
streamlit run app.py
```

## Contact

For questions or support regarding this calculator, contact Kris at [kris@meetmaro.com](mailto:kris@meetmaro.com).