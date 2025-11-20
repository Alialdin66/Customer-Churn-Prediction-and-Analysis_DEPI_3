# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import kagglehub
# from kagglehub import KaggleDatasetAdapter
 

# st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# st.title(" Customer Churn Analysis Dashboard")
# st.markdown("### Explore customer behavior, churn trends, and insights interactively")




# @st.cache_data
# def load_data():
#     file_path = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
#     df = kagglehub.load_dataset(
#         KaggleDatasetAdapter.PANDAS,
#         "blastchar/telco-customer-churn",
#         file_path,
#     )
#     return df

# df = load_data()


# # Sidebar Filters

# st.sidebar.header(" Filters")
# contract_filter = st.sidebar.multiselect("Contract Type", df['Contract'].unique(), default=df['Contract'].unique())
# internet_filter = st.sidebar.multiselect("Internet Service", df['InternetService'].unique(), default=df['InternetService'].unique())
# payment_filter = st.sidebar.multiselect("Payment Method", df['PaymentMethod'].unique(), default=df['PaymentMethod'].unique())
# dependents_filter = st.sidebar.multiselect("Dependents", df['Dependents'].unique(), default=df['Dependents'].unique())

# df_filtered = df[
#     (df['Contract'].isin(contract_filter)) &
#     (df['InternetService'].isin(internet_filter)) &
#     (df['PaymentMethod'].isin(payment_filter)) &
#     (df['Dependents'].isin(dependents_filter))
# ]


# #  KPIs

# total_customers = len(df_filtered)
# churned = df_filtered[df_filtered['Churn'] == 'Yes']
# churn_rate = round(len(churned) / total_customers * 100, 2)
# avg_monthly = round(df_filtered['MonthlyCharges'].mean(), 2)
# avg_tenure = round(df_filtered['tenure'].mean(), 2) if 'tenure' in df_filtered.columns else 0

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Total Customers", total_customers)
# col2.metric("Churned Customers", len(churned))
# col3.metric("Churn Rate (%)", churn_rate)
# col4.metric("Avg Monthly Charges", avg_monthly)

# st.divider()


# # Demographics

# st.subheader("👤 Demographic Insights")
# fig_demo = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
# fig_demo.add_trace(go.Pie(labels=['Male','Female'], values=df_filtered['gender'].value_counts(), name="Gender"), 1, 1)
# fig_demo.add_trace(go.Pie(labels=['No','Yes'], values=df_filtered['Churn'].value_counts(), name="Churn"), 1, 2)
# fig_demo.update_traces(hole=.4, hoverinfo="label+percent+name", textfont_size=14)
# fig_demo.update_layout(
#     title_text="Gender and Churn Distributions",
#     annotations=[dict(text='Gender', x=0.18, y=0.5, font_size=16, showarrow=False),
#                  dict(text='Churn', x=0.82, y=0.5, font_size=16, showarrow=False)]
# )
# st.plotly_chart(fig_demo, use_container_width=True)


# # Payment Method

# st.subheader("💳 Payment Method Analysis")
# fig_pay = px.histogram(df_filtered, x="Churn", color="PaymentMethod", barmode="group",
#                        title="Customer Payment Method distribution w.r.t. Churn")
# fig_pay.update_layout(width=600, height=400)
# st.plotly_chart(fig_pay, use_container_width=False)


# # Internet Service vs Churn

# st.subheader("🌐 Internet Service Analysis")
# fig_int = px.histogram(df_filtered, x="Churn", color="InternetService", barmode="group", title="Internet Service Distribution w.r.t Churn")
# st.plotly_chart(fig_int, use_container_width=True)


# # Monthly Charges vs Churn

# st.subheader("💰 Monthly Charges vs Churn")
# fig_charges = px.box(df_filtered, x="Churn", y="MonthlyCharges", color="Churn", title="Monthly Charges Distribution")
# st.plotly_chart(fig_charges, use_container_width=True)


# # Dependents

# st.subheader("👪 Dependents Impact on Churn")
# fig_dep = px.histogram(df_filtered, x="Churn", color="Dependents", barmode="group", title="Dependents distribution")
# st.plotly_chart(fig_dep, use_container_width=True)


# # Contract Type
# st.subheader("📄 Contract Type Analysis")
# fig_contract = px.histogram(df_filtered, x="Churn", color="Contract", barmode="group", title="Contract Distribution")
# st.plotly_chart(fig_contract, use_container_width=True)

# # Internet vs Payment Method
# st.subheader("🌐💳 Internet Service vs Payment Method")
# fig_stack = px.histogram(df_filtered, x="InternetService", color="PaymentMethod", facet_col="Churn", barmode="stack",
#                          title="Internet Service vs Payment Method vs Churn")
# st.plotly_chart(fig_stack, use_container_width=True)

# # Correlation Heatmap
# st.subheader("📈 Correlation Heatmap")
# num_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
# if len(num_cols) > 0:
#     fig_corr = px.imshow(df_filtered[num_cols].corr(), text_auto=True, color_continuous_scale='RdBu_r', title="Correlation Heatmap")
#     st.plotly_chart(fig_corr, use_container_width=True)


# # Summary

# st.subheader("🧠 Key Takeaways")
# st.markdown("""
# - **Fiber Optic** users churn the most → potential dissatisfaction.  
# - **Electronic Check** payment users also have high churn.  
# - **No dependents** or **month-to-month contracts** increase churn likelihood.  
# - Gender has minimal effect on churn rate.  
# - Higher monthly charges slightly increase churn risk.  
# """)

# st.success("✅ Dashboard loaded successfully!")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Advanced Customer Churn Dashboard", layout="wide")

st.title("Advanced Customer Churn Analysis Dashboard")
st.markdown("### Explore customer behavior, churn trends, and insights interactively with notes and insights under each chart")

# Load data
@st.cache_data
def load_data():
    csv_path = "./strelmint_dashboard.csv"
    df = pd.read_csv(csv_path)
    advanced_cols = [
        'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'MultipleLines', 
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 
        'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
    ]
    # Keep only available columns
    df = df[[col for col in advanced_cols if col in df.columns]]
    # Optional derived columns
    if 'charges_per_month' not in df.columns:
        df['charges_per_month'] = df['TotalCharges'] / df['tenure'].replace(0,1)
    if 'is_long_term' not in df.columns:
        df['is_long_term'] = df['tenure'].apply(lambda x: 'Yes' if x >= 12 else 'No')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
contract_filter = st.sidebar.multiselect("Contract Type", df['Contract'].unique(), default=df['Contract'].unique())
internet_filter = st.sidebar.multiselect("Internet Service", df['InternetService'].unique(), default=df['InternetService'].unique())
payment_filter = st.sidebar.multiselect("Payment Method", df['PaymentMethod'].unique(), default=df['PaymentMethod'].unique())
dependents_filter = st.sidebar.multiselect("Dependents", df['Dependents'].unique(), default=df['Dependents'].unique())

df_filtered = df[
    (df['Contract'].isin(contract_filter)) &
    (df['InternetService'].isin(internet_filter)) &
    (df['PaymentMethod'].isin(payment_filter)) &
    (df['Dependents'].isin(dependents_filter))
]

# KPIs
total_customers = len(df_filtered)
churned = df_filtered[df_filtered['Churn'] == 'Yes']
churn_rate = round(len(churned) / total_customers * 100, 2)
avg_monthly = round(df_filtered['MonthlyCharges'].mean(), 2)
avg_tenure = round(df_filtered['tenure'].mean(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", len(churned))
col3.metric("Churn Rate (%)", churn_rate)
col4.metric("Avg Monthly Charges", avg_monthly)

st.divider()

# 1️⃣ Demographics
st.subheader("👤 Senior Citizen Analysis")
fig_demo = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig_demo.add_trace(go.Pie(labels=['Senior','Non-Senior'], values=df_filtered['SeniorCitizen'].value_counts(), name="SeniorCitizen"), 1, 1)
fig_demo.add_trace(go.Pie(labels=['No','Yes'], values=df_filtered['Churn'].value_counts(), name="Churn"), 1, 2)
fig_demo.update_traces(hole=.4, hoverinfo="label+percent+name", textfont_size=14)
fig_demo.update_layout(
    title_text="SeniorCitizen and Churn Distributions",
    annotations=[dict(text='SeniorCitizen', x=0.18, y=0.5, font_size=16, showarrow=False),
                 dict(text='Churn', x=0.82, y=0.5, font_size=16, showarrow=False)]
)
st.plotly_chart(fig_demo, use_container_width=True)
st.markdown("**Note:** Senior citizens may have slightly higher churn due to longer tenure and preference for certain services. Churn distribution shows proportion of all customers who left.")

# 2️⃣ Payment Method Analysis
st.subheader("💳 Payment Method vs Churn")
fig_pay = px.histogram(df_filtered, x="Churn", color="PaymentMethod", barmode="group",
                       title="Customer Payment Method distribution w.r.t. Churn")
st.plotly_chart(fig_pay, use_container_width=True)
st.markdown("**Note:** Customers using 'Electronic Check' tend to churn more. Payment method affects convenience and satisfaction.")

# 3️⃣ Internet Service Analysis
st.subheader("🌐 Internet Service vs Churn")
fig_int = px.histogram(df_filtered, x="Churn", color="InternetService", barmode="group", title="Internet Service Distribution w.r.t Churn")
st.plotly_chart(fig_int, use_container_width=True)
st.markdown("**Note:** Fiber optic users show higher churn, likely due to cost or service issues. DSL and No internet customers churn less.")

# 4️⃣ Monthly Charges vs Churn
st.subheader("💰 Monthly Charges vs Churn")
fig_charges = px.box(df_filtered, x="Churn", y="MonthlyCharges", color="Churn", title="Monthly Charges Distribution")
st.plotly_chart(fig_charges, use_container_width=True)
st.markdown("**Note:** Customers who churn often have slightly higher monthly charges. Indicates pricing may influence churn decisions.")

# 5️⃣ Dependents Impact
st.subheader("👪 Dependents Impact on Churn")
fig_dep = px.histogram(df_filtered, x="Churn", color="Dependents", barmode="group", title="Dependents distribution")
st.plotly_chart(fig_dep, use_container_width=True)
st.markdown("**Note:** Customers without dependents show higher churn; family obligations may reduce likelihood to churn.")

# 6️⃣ Contract Type Analysis
st.subheader("📄 Contract Type vs Churn")
fig_contract = px.histogram(df_filtered, x="Churn", color="Contract", barmode="group", title="Contract Distribution")
st.plotly_chart(fig_contract, use_container_width=True)
st.markdown("**Note:** Month-to-month contracts have higher churn. Long-term contracts reduce churn risk.")

# 7️⃣ Internet vs Payment Method vs Churn
st.subheader("🌐💳 Internet Service vs Payment Method")
fig_stack = px.histogram(df_filtered, x="InternetService", color="PaymentMethod", facet_col="Churn", barmode="stack",
                         title="Internet Service vs Payment Method vs Churn")
st.plotly_chart(fig_stack, use_container_width=True)
st.markdown("**Note:** Certain combinations like Fiber + Electronic Check show higher churn. Bundling or preferred payment methods reduce churn risk.")

# 8️⃣ Correlation Heatmap
st.subheader("📈 Correlation Heatmap")
num_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
if len(num_cols) > 0:
    fig_corr = px.imshow(df_filtered[num_cols].corr(), text_auto=True, color_continuous_scale='RdBu_r', title="Correlation Heatmap")
    st.plotly_chart(fig_corr, use_container_width=True)
st.markdown("**Note:** Strong positive correlation between TotalCharges and tenure. MonthlyCharges moderately correlated with churn.")

# Summary
st.subheader("🧠 Key Takeaways")
st.markdown("""
- **Fiber Optic** users churn more than others → review service quality.  
- **Electronic Check** users show high churn → review payment options.  
- **No dependents** or **month-to-month contracts** → higher churn risk.  
- SeniorCitizen status affects churn risk.  
- Higher MonthlyCharges slightly increase churn likelihood.  
- Tenure positively correlates with TotalCharges and reduces churn risk over time.
""")

st.success("✅ Advanced Dashboard loaded successfully!")
