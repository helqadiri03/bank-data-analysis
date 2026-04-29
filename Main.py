import streamlit as st

st.set_page_config(
    page_title="Bank Analysis Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar to navigate between different sections of the report.")

# Main content
st.title("🏦 Bank Marketing Campaign Analysis")
st.subheader("Optimizing Term Deposit Subscriptions")

col1, col2 = st.columns([1, 1])

with col1:
    st.image('bank.jpeg', use_column_width=True)

with col2:
    st.markdown("""
    ### 🎯 Project Objective
    This report presents a comprehensive analysis of a bank's customer data, aiming to uncover key insights into customer behavior and identify factors influencing the success of marketing campaigns for term deposits.
    
    ### 🔍 Analysis Scope
    - **Customer Demographics**: Age, Job, Education, etc.
    - **Financial Status**: Loans, Defaults, Balances.
    - **Campaign Metrics**: Contact duration, frequency, and outcome.
    
    ### 📈 Why this matters?
    By understanding the profiles of successful subscribers, we can:
    - **Optimize** marketing spend.
    - **Increase** subscription rates.
    - **Personalize** customer outreach.
    """)

st.divider()

st.markdown("""
<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;'>
    <h4 style='color: #007bff; margin-top: 0;'>📊 Note on Visualizations</h4>
    <p>This report primarily utilizes interactive <b>Plotly charts</b>. This choice was made to provide a clear and concise understanding of complex data trends, allowing for easy identification of actionable recommendations.</p>
</div>
""", unsafe_allow_html=True)
