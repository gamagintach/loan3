import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(
    page_title="Demo Dashboard",
    page_icon=".",
    layout='wide'
)


st.title("Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("----")

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

#loan = pd.read_csv('data_input/loan.csv')
#loan['issue_date'] = pd.to_datetime(loan['issue_date'])
loan = pd.read_pickle('data_input/loan_clean')

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Total Loans', f"{loan['id'].count():,.0f}",help="Total Number of Loans")
        st.metric('Total Loan Amount', f"${loan['loan_amount'].sum():,.0f}")

    with col2:
        st.metric('Average Interest Rate', f"{loan['interest_rate'].mean():,.2f}")
        st.metric('Average Loan Amount', f"${loan['loan_amount'].mean():,.0f}")

import plotly.express as px

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loans Issued Over Time','Loan Amount Over Time','Issue Date Analysis'])

    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()

        line_count = px.line(
            loan_date_count,
            markers=True,
            title="Number of Loans Issued Over Time",
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
	        },
            template='seaborn'
        ).update_layout(showlegend = False)

        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        line_sum = px.line(
            loan_date_sum,
            markers=True,
            title='Total Loan Amount Issued Over Time',
            labels={
            'value':'Total Loan Amount',
            'issue_date':'Issue Date'
	        },
            template='seaborn'
        ).update_layout(showlegend = False)

        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()

        bar_count = px.bar(
            loan_day_count,
            category_orders={
            'issue_weekday' : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            },
            title='Distribution of Loans by Day of the Week',
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
	        },
            template='seaborn'
        ).update_layout(showlegend = False)

        st.plotly_chart(bar_count)


st.subheader("Loan Performance")

#with st.container(border=True):
with st.expander("Click Here to Expand Visualization"):
    col3, col4 = st.columns(2)

    with col3:
        pie = px.pie(
            loan,
            names='loan_condition',
            title='Distribution of Loans by Condition',
            hole=0.4
        ).update_traces(textinfo='percent + value')
        
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()

        bar = px.bar(
            grade,
            title='Distribution of Loans by Grade',
            labels={
            'grade':'Grade',
            'value':'Number of Loans'
            },
            template='seaborn'
        ).update_layout(showlegend = False)

        st.plotly_chart(bar)

st.subheader("Financial Analysis")

condition= st.selectbox("Select Loan Condition",["Good Loan","Bad Loan"])

loan_condition = loan[loan['loan_condition'] == condition]

with st.container(border=True):
    tab4, tab5 = st.tabs(['Loan Amount Distribution by Period','Loan Amount Distribution by Purpose'])

    with tab4:
        histo = px.histogram(
        loan_condition,
        x='loan_amount',
        nbins=20,
        color='term',
        color_discrete_sequence=['darkslateblue', 'tomato'],
        title='Loan Amount Distribution by Condition',
        labels={
            'loan_amount': 'Loan Amount',
            'count': 'Number of Loans',
            'term' : 'Loan Term'
            }
        )
        st.plotly_chart(histo)

    with tab5:
        box = px.box(
        loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        color_discrete_sequence=['darkslateblue', 'tomato','lightblue'],
        title='Loan Amount Distribution by Purpose',
        labels={
            'loan_amount': 'Loan Amount',
            'term': 'Loan Term',
            'purpose': 'Loan Purpose'
            }
        )
        st.plotly_chart(box)