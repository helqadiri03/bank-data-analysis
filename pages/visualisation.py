import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Visualisation - Bank Analysis", page_icon="📊", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stHeader {
        color: #1E3A8A;
    }
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .main {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data  
def load_data():
    df = pd.read_csv('bank.csv') 
    return df

def plot_bar(df, column, title, x_label, y_label, color_sequence=px.colors.qualitative.Pastel):
    counts = df[column].value_counts()
    fig = px.bar(
        x=counts.index, 
        y=counts.values,
        title=title,
        labels={'x': x_label, 'y': y_label},
        color=counts.index,
        color_discrete_sequence=color_sequence,
        template="plotly_white"
    )
    fig.update_layout(showlegend=False)
    return fig

try:
    df = load_data() 
    df_yes = df[df['deposit'] == 'yes']
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.title("🔍 Filters")
job_filter = st.sidebar.multiselect("Select Job", options=df['job'].unique(), default=df['job'].unique())
marital_filter = st.sidebar.multiselect("Select Marital Status", options=df['marital'].unique(), default=df['marital'].unique())

# Apply Filters
filtered_df = df[(df['job'].isin(job_filter)) & (df['marital'].isin(marital_filter))]
filtered_df_yes = filtered_df[filtered_df['deposit'] == 'yes']

# Metrics
st.title("📊 Customer Insights & Campaign Analysis")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Customers", len(filtered_df))
m2.metric("Subscribers (Yes)", len(filtered_df_yes))
m3.metric("Conversion Rate", f"{(len(filtered_df_yes)/len(filtered_df)*100):.2f}%" if len(filtered_df) > 0 else "0%")
m4.metric("Avg Age", f"{filtered_df['age'].mean():.1f}")

st.divider()

# Section 1: Customer Understanding
st.header("👤 Customer Understanding")
st.subheader("1. What is the typical profile of the customer who takes out a term deposit?")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_bar(filtered_df_yes, 'job', "Job Titles of Subscribers", "Job", "Count"), use_container_width=True)
    st.plotly_chart(plot_bar(filtered_df_yes, 'education', "Education Level of Subscribers", "Education", "Count"), use_container_width=True)

with col2:
    st.plotly_chart(plot_bar(filtered_df_yes, 'marital', "Marital Status of Subscribers", "Marital Status", "Count"), use_container_width=True)
    
    # Age Groups
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-18', '18-30', '30-40', '40-50', '50-60', '60+']
    filtered_df_yes['AgeGroup'] = pd.cut(filtered_df_yes['age'], bins=bins, labels=labels, right=False)
    st.plotly_chart(plot_bar(filtered_df_yes, 'AgeGroup', "Age Category of Subscribers", "Age Group", "Count"), use_container_width=True)

st.info("**Insight:** The typical term deposit subscriber is a married individual between the ages of 30 and 40, holding a management position, and possessing a secondary education level.")

st.divider()

# Section 2: Loans Impact
st.subheader("2. How do housing and personal loans impact the decision to subscribe?")
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(plot_bar(filtered_df_yes, 'housing', "Housing Loan Status", "Housing Loan", "Count"), use_container_width=True)
with col4:
    st.plotly_chart(plot_bar(filtered_df_yes, 'loan', "Personal Loan Status", "Personal Loan", "Count"), use_container_width=True)

st.info("**Insight:** Subscribers often lack housing and personal loans, suggesting individuals with fewer financial obligations are more inclined to save.")

st.divider()

# Section 3: Duration and Timing
st.header("🕒 Timing & Engagement")
st.subheader("3. Impact of Last Contact Duration")

bins_dur = [0, 500, 1000, 1500, 2000, 3000, 4000]
labels_dur = ['0-500s', '500-1000s', '1000-1500s', '1500-2000s', '2000-3000s', '3000s+']
filtered_df_yes['DurationGroup'] = pd.cut(filtered_df_yes['duration'], bins=bins_dur, labels=labels_dur, right=False)
st.plotly_chart(plot_bar(filtered_df_yes, 'DurationGroup', "Contact Duration vs Subscriptions", "Duration Group", "Count"), use_container_width=True)

st.subheader("4. Best time of year to contact clients?")
col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(plot_bar(filtered_df_yes, 'month', "Successful Subscriptions by Month", "Month", "Count"), use_container_width=True)
with col6:
    day_counts = filtered_df_yes['day'].value_counts().sort_index()
    fig_day = px.line(x=day_counts.index, y=day_counts.values, title="Successful Subscriptions by Day of Month", labels={'x': 'Day', 'y': 'Count'})
    st.plotly_chart(fig_day, use_container_width=True)

st.divider()

# Section 4: Marketing Campaigns
st.header("📢 Marketing Strategy")
col7, col8 = st.columns(2)
with col7:
    st.plotly_chart(plot_bar(filtered_df_yes, 'contact', "Most Effective Communication Channel", "Channel", "Count"), use_container_width=True)
with col8:
    st.plotly_chart(plot_bar(filtered_df_yes, 'default', "Impact of Credit Default history", "Has Default", "Count"), use_container_width=True)

st.subheader("5. Impact of Contact Frequency")
campaign_counts = filtered_df_yes['campaign'].value_counts().sort_index().head(10) # Top 10 frequencies
fig_camp = px.bar(x=campaign_counts.index, y=campaign_counts.values, title="Number of Contacts vs Subscriptions (Top 10)", labels={'x': 'Contacts', 'y': 'Count'})
st.plotly_chart(fig_camp, use_container_width=True)

st.info("**Insight:** A lower number of contacts (targeted approach) is often more effective than high-frequency persistence.")

st.divider()

st.subheader("6. Effectiveness of Previous Marketing Strategies")
poutcome_counts = filtered_df_yes['poutcome'].value_counts().sort_values()
fig_poutcome = px.pie(
    names=poutcome_counts.index, 
    values=poutcome_counts.values, 
    title="Outcome of Previous Campaigns",
    color_discrete_sequence=px.colors.qualitative.Prism,
    hole=0.4
)
st.plotly_chart(fig_poutcome, use_container_width=True)

st.markdown("""
<div style='background-color: #E0F2FE; padding: 15px; border-radius: 8px;'>
    <p style='margin: 0; color: #0369A1;'><b>Conclusion:</b> Successful previous campaigns are strong indicators of future success. However, data quality improvements are recommended for 'unknown' outcomes to further refine predictive accuracy.</p>
</div>
""", unsafe_allow_html=True)

