import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetireWise Dashboard", layout="wide")

st.title("💼 RetireWise: Personal Finance Dashboard")

# Sidebar for CSV upload
st.sidebar.header("Upload Your Financial Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Sample columns expected: Month, Income, Expenses, Savings, Investments, KiwiSaver
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Net Worth'] = df['Savings'] + df['Investments'] + df['KiwiSaver']
    df['Net Savings'] = df['Income'] - df['Expenses']

    st.subheader("📊 Financial Overview")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(df, x='Month', y='Net Worth', title='Net Worth Over Time')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(df, x='Month', y='Net Savings', title='Net Savings Over Time')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📁 Category Breakdown")
    fig3 = px.bar(df, x='Month', y=['Income', 'Expenses', 'Savings', 'Investments', 'KiwiSaver'], 
                  title='Monthly Financial Breakdown', barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🎯 Retirement Goal Progress")
    goal_amount = st.sidebar.number_input("Set Retirement Goal (NZD)", value=1000000)
    final_net_worth = df['Net Worth'].iloc[-1]
    progress = min(final_net_worth / goal_amount, 1.0)
    st.progress(progress)
    st.write(f"Current Net Worth: ${final_net_worth:,.2f}")
    st.write(f"Goal: ${goal_amount:,.2f}")

    st.subheader("💬 Chatbot Assistant")
    query = st.text_input("Ask a question about your finances:")
    if query:
        if "reduce expenses" in query.lower():
            top_expense_month = df.loc[df['Expenses'].idxmax()]['Month']
            st.write(f"Your highest expenses occurred in {top_expense_month}. Consider reviewing spending that month.")
        elif "savings rate" in query.lower():
            savings_rate = (df['Savings'].sum() / df['Income'].sum()) * 100
            st.write(f"Your average savings rate is {savings_rate:.2f}%. Aim for at least 20% if possible.")
        elif "kiwisaver" in query.lower():
            st.write("KiwiSaver contributions help grow your retirement fund. Consider increasing your rate to 6–10% for better growth.")
        else:
            st.write("I'm still learning! Try asking about expenses, savings rate, or KiwiSaver.")
else:
    st.info("Please upload a CSV file to begin.")
