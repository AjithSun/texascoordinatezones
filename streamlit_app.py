import streamlit as st
import pandas as pd

file_path = 'TXzipcitycountycountycode.csv'
df = pd.read_csv(file_path)

plane_names = {
    4201: 'TX83-NF',
    4202: 'TX83-NCF',
    4203: 'TX83-CF',
    4204: 'TX83-SCF',
    4205: 'TX83-SF'
}

st.title("Texas Counties SPCS83 Zones")

combined_options = pd.concat([df['zip'].astype(str), df['city'], df['county']]).unique()
search_input = st.selectbox("Select a zip code, city, or county:", combined_options)

if search_input:
    zip_result = df[df['zip'].astype(str) == search_input]
    city_result = df[df['city'].str.capitalize() == search_input.capitalize()]
    county_result = df[df['county'].str.capitalize() == search_input.capitalize()]

    result = pd.concat([zip_result, city_result, county_result]).drop_duplicates(subset=['SPCS83_Code'])

    if not result.empty:
        for _, row in result.iterrows():
            spcs83_code = row['SPCS83_Code']
            plane_name = plane_names.get(spcs83_code, "Unknown")
            
            if row['city'].capitalize() == search_input.capitalize():
                result_type = "city"
            elif row['county'].capitalize() == search_input.capitalize():
                result_type = "county"
            else:
                result_type = "zip code"
            
            st.write(f"The plane name for {search_input} ({result_type}) is {plane_name}")

            st.code(plane_name, language="text")
            st.markdown("Click the button above to copy the plane name.")
            st.markdown("---")
    else:
        st.write(f"No data found for {search_input}")
