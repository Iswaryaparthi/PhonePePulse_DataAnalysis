import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
import plotly.graph_objects as go

st.set_page_config(page_title= "Phonepe Pulse Data Visualization and Exploration:",
                    layout= "wide",
                   initial_sidebar_state= "expanded",
                   )

st.sidebar.header(":wave: :violet[**Welcome to the dashboard**]",divider='rainbow')

st.sidebar.subheader(":red[Technologies used:]")

st.sidebar.subheader("Github cloning - Extract data from the Phonepe pulse Github repository and clone it")

st.sidebar.subheader("Pandas,Plotly - Create a visualization dashboard using Streamlit and Plotly")

st.sidebar.subheader("Python, MySQL - Fetch the data from the MySQL database to display in the dashboard.")

# Custom CSS for the sidebar
#sidebar_custom_css = """
    #div.sidebar .sidebar-content {
        #background-color: #3498db;  /* Change the background color */
        #color: #ffffff;  /* Change the text color */
       # width: 150px;  /* Adjust the width */
   # }
#"""

# Apply the custom CSS
#st.markdown(f'<style>{sidebar_custom_css}</style>', unsafe_allow_html=True)


# Add a dropdown menu to the sidebar
#selected_option = st.sidebar.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])

# Add other widgets to the main section of the app
st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]")

#--------Transaction Analysis Year-wise------------#

# Function to connect to MySQL and fetch data
def get_data():
    connection = pymysql.connect(
                   host="localhost",
                   user="root",
                   password="Pwd@123456",
                   database="phonepe_pulse"
    )

    query = f"SELECT * FROM agg_trans"
    df = pd.read_sql(query, connection)

    connection.close()
    return df

# Dropdown for selecting a state
#selected_state = st.selectbox("Select a State:", ["andaman-&-nicobar-islands","andhra-pradesh","arunachal-pradesh","assam","bihar","chandigarh","chhattisgarh","dadra-&-nagar-haveli-&-daman-&-diu",
                                                 # "delhi", "goa", "gujarat","haryana", "himachal-pradesh", "jammu-&-kashmir",
                                                    #    "jharkhand","karnataka", "kerala","ladakh","lakshadweep","madhya-pradesh",
                                                     #   "maharashtra","manipur","meghalaya","mizoram","nagaland","odisha",
                                                    #    "puducherry", "punjab","rajasthan","sikkim", "tamil-nadu","telangana","tripura",                                                                                                              
                                                    #    "uttar-pradesh","uttarakhand","west-bengal"])
  
# Fetch data from MySQL based on the selected state
df = get_data()

# Streamlit app
st.title(":blue[Transaction Data Analysis]")

# Select a state to visualize
selected_state = st.selectbox("Select State:", df['States'].unique())

# Filter data based on selected state
filtered_data = df[df['States'] == selected_state]

# Display a pie chart for Transaction Count distribution
fig_pie = px.pie(
    filtered_data,
    names='Transaction_type',
    values='Transaction_count',
    title=f'Transaction Count Distribution in {selected_state}',
    color='Transaction_type',
)
st.plotly_chart(fig_pie)

# Display a scatter plot for Transaction Amount vs Transaction Count
fig_scatter = px.scatter(
    filtered_data,
    x='Transaction_count',
    y='Transaction_amount',
    title=f'Transaction Amount vs Transaction Count in {selected_state}',
    color='Transaction_type',
    size='Transaction_amount',
    hover_name='Transaction_type',
)
st.plotly_chart(fig_scatter)

# Bar chart for Transaction Amount
fig_amount = px.bar(df, x='Year', y='Transaction_amount', title=f'Transaction Amount year wise - {selected_state}')
fig_amount.update_layout(height=400,width = 500)                        
# Explicitly set the x-axis range to avoid auto-adjustment when zooming
#fig_amount.update_xaxes(range=[min(df['Year']), max(df['Year'])])
st.plotly_chart(fig_amount,use_container_width=True)

# Bar chart for Transaction Count
fig_count = px.bar(df, x='Year', y='Transaction_count', title=f'Transaction Count year wise - {selected_state}')
fig_count.update_layout(height=400, width =500)
# Explicitly set the x-axis range to avoid auto-adjustment when zooming
#fig_count.update_xaxes(range=[min(df['Year']), max(df['Year'])])
st.plotly_chart(fig_count,use_container_width=True)

#--------Transaction Analysis Quarter-wise------------#

# Function to connect to MySQL and fetch data
def get_data():
    connection = pymysql.connect(
                   host="localhost",
                   user="root",
                   password="Pwd@123456",
                   database="phonepe_pulse"
    )

    query = f"SELECT * FROM agg_trans"
    df = pd.read_sql(query, connection)

    connection.close()
    return df

# Streamlit app
def main():
    st.title(":blue[Transaction Analysis Quarter-wise]")
    
# Fetch data from MySQL
    data = get_data()
    
 # Create a pie chart using Plotly
    fig = px.pie(data, values='Transaction_amount', names='Quarters', title='Transaction amount Quarter-wise')

        # Display the pie chart using Streamlit
    st.plotly_chart(fig)
    
    fig = px.pie(data, values='Transaction_count', names='Quarters', title='Transaction count Quarter-wise')

        # Display the pie chart using Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
    
# Function to connect to MySQL and fetch data
def get_data():
    connection = pymysql.connect(
                   host="localhost",
                   user="root",
                   password="Pwd@123456",
                   database="phonepe_pulse"
    )

    query = f"SELECT * FROM agg_user"
    df = pd.read_sql(query, connection)

    connection.close()
    return df

# Streamlit app
def main():
    st.title(":orange[Brands Analysis]")

# Fetch data from MySQL
data = get_data()

st.title(":orange[Brands Analysis]")

# Bar Chart
fig_bar = px.bar(data, x='States', y='Count', color='Brands',
                 labels={'Count': 'Number of Smartphones'},
                 title='Distribution of Smartphone Brands by State')
st.plotly_chart(fig_bar)


# Treemap
fig_treemap = px.treemap(data, path=['States', 'Brands'], values='Count',
                         title='Overall Market Distribution')
st.plotly_chart(fig_treemap)


#------------Top 10 transactions --------#
def get_data():
    connection = pymysql.connect(
                   host="localhost",
                   user="root",
                   password="Pwd@123456",
                   database="phonepe_pulse"
    )

    query = f"SELECT * FROM top_trans"
    df = pd.read_sql(query, connection)

    connection.close()
    return df

# Streamlit app
def main():
    st.title(":green[Top 10 analysis for transactions]")

# Fetch data from MySQL
data = get_data()

# Group by State and Pincode to get total transaction count
grouped_data = data.groupby(['State', 'Pincode']).agg({'Transaction_count': 'sum'}).reset_index()

# Streamlit app
st.title(":green[Top Transaction Count Analysis]")

# Dropdown to select a state
selected_state = st.selectbox("Select a State", data['State'].unique())

# Filter data for the selected state
filtered_data = grouped_data[grouped_data['State'] == selected_state]

# Sort by Transaction_Count in descending order and get top 10
top_10 = filtered_data.sort_values(by=('Transaction_count'), ascending=False).head(10)

# Display the top 10 registered users based on state and pincode
st.write(f'Top 10 Transactions for {selected_state}:')
st.write(top_10.head(10))

# Create Plotly pie chart
fig = px.pie(top_10, values='Transaction_count', names='Pincode',
             labels={'Transaction_count': 'Total Transaction Count'},
             title=f'Top 10 Transaction Count Distribution for {selected_state}')

# Display the chart using Streamlit
st.plotly_chart(fig)

#------------Top 10 registered users----------#

def get_data():
    connection = pymysql.connect(
                   host="localhost",
                   user="root",
                   password="Pwd@123456",
                   database="phonepe_pulse"
    )

    query = f"SELECT * FROM top_user"
    df = pd.read_sql(query, connection)

    connection.close()
    return df

# Streamlit app
def main():
    st.title("Top 10 analysis for users")

# Fetch data from MySQL
data = get_data()

# Streamlit app
st.title(':green[Top Registered Users Analysis]')

# Dropdown for selecting the year
years = data['Year'].unique().tolist()
selected_year = st.selectbox('Select Year', years, index=len(years)-1)  # Set default to the latest year

# Filter data for the selected year
data_filtered = data[data['Year'] == selected_year]

# Group by state and pincode and sum the registered users
df_grouped = data_filtered.groupby(['States', 'Pincode'])['Registered_Users'].sum().reset_index()

# Sort by registered users in descending order
data_sorted = df_grouped.sort_values(by='Registered_Users', ascending=False)

# Display the top 10 registered users based on state and pincode
st.write(f'Top 10 Registered Users for {selected_year}:')
st.write(data_sorted.head(10))

# Create a Plotly bar chart
bar_fig = px.bar(data_sorted.head(10), x='Registered_Users', y='States', color='Pincode',
                 labels={'Registered_Users': 'Total Registered Users'},
                 title=f'Top 10 Registered Users by State and Pincode ({selected_year})')

# Display the bar chart using Streamlit
st.plotly_chart(bar_fig)


