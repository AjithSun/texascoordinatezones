import streamlit as st
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import LogColorMapper, ColumnDataSource
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.sampledata.us_counties import data as counties

# Convert palette to a list and reverse it
palette = list(palette)
palette.reverse()

# Load the CSV file with counties and their SPCS83 codes
file_path = 'texas_counties_spcs83.csv'  # Update the path if necessary
df = pd.read_csv(file_path)

# Add plane names corresponding to SPCS83 codes
plane_names = {
    4201: 'TX83-NF',
    4202: 'TX83-NCF',
    4203: 'TX83-CF',
    4204: 'TX83-SCF',
    4205: 'TX83-SF'
}

# Filter counties to get only Texas
texas_counties = {code: county for code, county in counties.items() if county["state"] == "tx"}

# Create a DataFrame for Texas counties
texas_df = pd.DataFrame(texas_counties).T
texas_df = texas_df.reset_index()
texas_df['county_name'] = texas_df['name'].str.lower()

# Merge with the SPCS83 codes DataFrame
df['County'] = df['County'].str.lower()
merged_df = pd.merge(texas_df, df, left_on='county_name', right_on='County')

# Create a color mapper
color_mapper = LogColorMapper(palette=palette)

# Streamlit UI
st.title("Texas Counties SPCS83 Zones")

# Create a dropdown for selecting the county
county = st.selectbox("Select a county to find the plane name:", df['County'].str.capitalize().unique())

if county:
    result = df[df['County'].str.capitalize() == county]
    if not result.empty:
        spcs83_code = result.iloc[0]['SPCS83_Code']
        plane_name = plane_names.get(spcs83_code, "Unknown")
        st.write(f"The plane name for {county} is {plane_name}")
        
        # Highlight the searched county
        searched_county = result.iloc[0]['County']
        merged_df['highlight'] = merged_df['County'].apply(lambda x: x == searched_county)
        
        # Display the relevant code name and add a copy button
        st.code(plane_name, language="text")
        st.markdown("Click the button above to copy the plane name.")
    else:
        st.write("County not found")
        merged_df['highlight'] = False
else:
    merged_df['highlight'] = False

# Create Bokeh plot
p = figure(title="Texas Counties by SPCS83 Code", toolbar_location="left",
           width=800, height=800)

source = ColumnDataSource(merged_df)
highlight_source = ColumnDataSource(merged_df[merged_df['highlight']])

p.patches("lons", "lats", source=source,
          fill_color={'field': 'SPCS83_Code', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

# Highlight the searched county in red
p.patches("lons", "lats", source=highlight_source,
          fill_color="red", fill_alpha=0.7, line_color="white", line_width=0.5)

# Display the Bokeh plot
st.bokeh_chart(p)
