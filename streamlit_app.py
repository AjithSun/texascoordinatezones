import streamlit as st
import pandas as pd

# Load the CSV file with zip, city, county, and SPCS83 codes
file_path = 'TXzipcitycountycountycode.csv'  # Update the path if necessary
df = pd.read_csv(file_path)

# Add plane names corresponding to SPCS83 codes
plane_names = {
    4201: 'TX83-NF',
    4202: 'TX83-NCF',
    4203: 'TX83-CF',
    4204: 'TX83-SCF',
    4205: 'TX83-SF'
}

# Streamlit UI
st.title("Texas Counties SPCS83 Zones")

# Search options
search_option = st.radio("Search by:", ["Zip Code", "City", "County"])

# Search input based on the selected option
if search_option == "Zip Code":
    search_input = st.selectbox("Select a zip code:", df['zip'].unique())
    result = df[df['zip'] == search_input]
elif search_option == "City":
    search_input = st.selectbox("Select a city:", df['city'].str.capitalize().unique())
    result = df[df['city'].str.capitalize() == search_input]
else:
    search_input = st.selectbox("Select a county:", df['county'].str.capitalize().unique())
    result = df[df['county'].str.capitalize() == search_input]

# Display the result
if not result.empty:
    spcs83_code = result.iloc[0]['SPCS83_Code']
    plane_name = plane_names.get(spcs83_code, "Unknown")
    st.write(f"The plane name for {search_input} is {plane_name}")
    
    # Display the relevant code name and add a copy button
    st.code(plane_name, language="text")
    st.markdown("Click the button above to copy the plane name.")
else:
    st.write(f"No data found for {search_input}")
