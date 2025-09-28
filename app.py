import streamlit as st

st.set_page_config(page_title="RetireWise Chatbot", layout="wide")

st.title("💬 RetireWise: KiwiSaver Financial Chatbot")
st.write("Welcome to your personal financial dashboard and chatbot for retirement planning in New Zealand.")

# Sidebar inputs
st.sidebar.header("📊 KiwiSaver Simulator")
current_balance = st.sidebar.number_input("Current KiwiSaver Balance", min_value=0.0, value=20000.0)
employee_rate = st.sidebar.selectbox("Employee Contribution Rate (%)", [3, 4, 6, 8, 10], index=0)
employer_rate = st.sidebar.selectbox("Employer Contribution Rate (%)", [3, 4, 6, 8, 10], index=0)
annual_return = st.sidebar.slider("Expected Annual Return (%)", 2.0, 10.0, 6.0)
years_to_retirement = st.sidebar.slider("Years Until Retirement", 1, 40, 30)

# KiwiSaver projection calculation
def project_kiwisaver(balance, employee_rate, employer_rate, return_rate, years):
    monthly_contribution = 6000 * (employee_rate + employer_rate) / 100 / 12
    projected = []
    for year in range(years + 1):
        balance += monthly_contribution * 12
        balance *= (1 + return_rate / 100)
        projected.append((year, round(balance, 2)))
    return projected

projection = project_kiwisaver(current_balance, employee_rate, employer_rate, annual_return, years_to_retirement)

# Display projection
st.subheader("📈 Projected KiwiSaver Balance")
for year, value in projection:
    st.write(f"Year {year}: ${value:,.2f}")

# Chatbot logic
st.subheader("💬 Chat with RetireWise")
user_input = st.text_input("Ask a question about KiwiSaver, budgeting, or retirement:")

def respond_to_query(query):
    query = query.lower()
    if "contribution rate" in query:
        return "The default KiwiSaver employee rate is 3%, but you can choose up to 10%. A 5% rate is considered adequate for most New Zealanders."
    elif "withdraw" in query or "retire" in query:
        return "You can withdraw your KiwiSaver savings from age 65. If you joined before July 2019, you may have a 5-year lock-in period."
    elif "keep invested" in query:
        return "Yes, many retirees keep their KiwiSaver invested to maintain growth and combat inflation. You can make partial or lump sum withdrawals."
    elif "retirement income" in query or "how much do i need" in query:
        return "A single person in a metro area with a 'No Frills' lifestyle needs about $43,000/year. NZ Super provides around $25,000/year, so KiwiSaver helps fill the gap."
    elif "provider" in query:
        return "Top KiwiSaver providers include Pathfinder (ethical), Simplicity (low fees), and Milford (high performance)."
    elif "fund" in query or "risk" in query:
        return "Conservative funds suit 2–5 year goals, Balanced for 5–10 years, Growth for 8–15 years, and Aggressive for 10+ years. Milford Active Growth has ~10.1% return."
    else:
        return "I'm here to help with KiwiSaver, budgeting, and retirement planning. Try asking about contribution rates, providers, or fund types."

if user_input:
    response = respond_to_query(user_input)
    st.markdown(f"**RetireWise:** {response}")
