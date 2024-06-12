import streamlit as st
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import LogColorMapper, ColumnDataSource
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.sampledata import download as download_sample_data
from bokeh.sampledata.us_counties import data as counties
import os

# Ensure Bokeh sample data is downloaded
def ensure_sample_data():
    data_dir = os.path.join(os.path.expanduser("~"), ".bokeh", "data")
    if not os.path.exists(data_dir):
        download_sample_data()

ensure_sample_data()

# Convert palette to a list and reverse it
palette = list(palette)
palette.reverse()

# Load the CSV file with counties and their SPCS83 codes
file_path = 'texas_counties_spcs83.csv'  # Update the path if necessary
df = pd.read_csv(file_path)

# Add plane names corresponding to SPCS83 codes
plane_names = {
    4201: 'TX-North',
    4202: 'TX-N Central',
    4203: 'TX-Central',
    4204: 'TX-S Central',
    4205: 'TX-South'
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
st.title("Texas Counties SPCS83 Codes")

# Search bar for finding SPCS83 code by county
county = st.text_input("Enter county name to find the plane name:")

if county:
    result = df[df['County'].str.lower() == county.lower()]
    if not result.empty:
        spcs83_code = result.iloc[0]['SPCS83_Code']
        plane_name = plane_names.get(spcs83_code, "Unknown")
        st.write(f"The plane name for {county} is {plane_name}")
        
        # Highlight the searched county
        searched_county = result.iloc[0]['County']
        merged_df['highlight'] = merged_df['County'].apply(lambda x: x == searched_county)
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
