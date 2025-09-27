import streamlit as st
import pandas as pd


# --- PAGE CONFIGURATION ---
st.set_page_config(
   page_title="Penguins Data Analysis",
   page_icon="🐧",
   layout="wide",
   initial_sidebar_state="expanded",
)


# --- DATA LOADING ---
# Using st.cache_data to avoid reloading data on every interaction
@st.cache_data
def load_data():
   """Loads the palmer penguins dataset from a public URL."""
   url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
   df = pd.read_csv(url)
   # Drop rows with missing values for simplicity in this demo
   df.dropna(inplace=True)
   return df


df = load_data()


# --- APP TITLE AND DESCRIPTION ---
st.title("🐧 Palmer Penguins Data Analysis")
st.markdown("""
This application performs a simple exploratory data analysis (EDA) on the Palmer Penguins dataset.
Use the filters in the sidebar to explore the relationships between different measurements of the penguins.
""")


# --- SIDEBAR FOR FILTERS ---
st.sidebar.header("Filter Your Penguins")


# Filter for species
species = st.sidebar.multiselect(
   "Select Species",
   options=df["species"].unique(),
)


# Filter for island
island = st.sidebar.multiselect(
   "Select Island",
   options=df["island"].unique(),
)


# Filter for sex
sex = st.sidebar.multiselect(
   "Select Sex",
   options=df["sex"].unique(),
)


# Filter for body mass
min_mass, max_mass = int(df["body_mass_g"].min()), int(df["body_mass_g"].max())
body_mass_slider = st.sidebar.slider(
   "Select Body Mass (g)",
   min_value=min_mass,
   max_value=max_mass,
   value=(min_mass, max_mass),
)


# --- FILTERING THE DATAFRAME ---
# Start with the full dataframe and apply filters sequentially
df_selection = df.copy()


# Apply multiselect filters only if a selection has been made for that filter
if species:
   df_selection = df_selection[df_selection["species"].isin(species)]
if island:
   df_selection = df_selection[df_selection["island"].isin(island)]
if sex:
   df_selection = df_selection[df_selection["sex"].isin(sex)]


# Always apply the slider filter
df_selection = df_selection[
   (df_selection["body_mass_g"] >= body_mass_slider[0]) &
   (df_selection["body_mass_g"] <= body_mass_slider[1])
]




# Display error message if no data is selected
if df_selection.empty:
   st.warning("No data available for the selected filters. Please adjust your selection.")
   st.stop() # Halts the app execution


# --- MAIN PAGE CONTENT ---
st.subheader("📊 Key Metrics")


# --- DISPLAY KEY METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
   st.metric(label="Total Penguins", value=df_selection.shape[0])
with col2:
   avg_bill_length = round(df_selection["bill_length_mm"].mean(), 1)
   st.metric(label="Avg. Bill Length (mm)", value=avg_bill_length)
with col3:
   avg_body_mass = round(df_selection["body_mass_g"].mean(), 1)
   st.metric(label="Avg. Body Mass (g)", value=f"{avg_body_mass / 1000:.2f} kg")


st.markdown("---")


# --- VISUALIZATIONS ---
st.subheader("📈 Visualizations")


# Arrange charts in columns
viz_col1, viz_col2 = st.columns(2)


with viz_col1:
   # Scatter plot: Bill Length vs. Bill Depth
   st.subheader("Bill Length vs. Bill Depth")
   # st.scatter_chart can use a color parameter to differentiate categories
   st.scatter_chart(
       data=df_selection,
       x="bill_length_mm",
       y="bill_depth_mm",
       color="species"
   )


with viz_col2:
   # Bar Chart: Average Body Mass by Species
   st.subheader("Average Body Mass by Species")
   # Group data to calculate average body mass for the bar chart
   avg_mass_by_species = df_selection.groupby('species')['body_mass_g'].mean().round(1)
   st.bar_chart(avg_mass_by_species)




# --- DISPLAY RAW DATA ---
with st.expander("View Raw Data"):
   st.dataframe(df_selection)
   st.markdown(f"**Data Dimensions:** {df_selection.shape[0]} rows, {df_selection.shape[1]} columns")


st.markdown("---")
st.write("Data Source: [Palmer Penguins Dataset](https://github.com/allisonhorst/palmerpenguins)")
