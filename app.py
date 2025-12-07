import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import make_pattern_rectpack as mpr

st.title("Pattern Fitting Web App")
st.write("Use Sample CSV or choose your own CSV file.")
st.write("""
**CSV file format:**

- The CSV should have the following columns:
    - `pattern_name`: Name or identifier for the pattern piece.
    - `width`: Width of the pattern piece (in the same units as fabric).
    - `height`: Height of the pattern piece (in the same units as fabric).
- The fabric dimensions should be specified in a row where `pattern_name` is 'fabric'.
""")         

col1, col2 = st.columns(2)
with col1:
    sample_csv_btn = st.button("Use Sample CSV")
with col2:
    download_sample_csv = st.button("Download sample CSV")
st.write("Or choose your own CSV file:")    
if download_sample_csv:
    csv = open("fabric.csv", "rb").read()
    st.download_button(
        label="Click here to download sample CSV",
        data=csv,
        file_name="sample_fabric.csv",
        mime="text/csv"
    )
    
if sample_csv_btn:
    uploaded_file = open("fabric.csv", "rb")
else:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    fabric_width, fabric_height, pattern_list = mpr.read_fabric_csv(uploaded_file)
    uploaded_file.seek(0)
    if uploaded_file.read().strip() == "":
        st.error("Uploaded CSV file is empty.")
        st.stop()
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
    st.write("CSV Preview:")
    st.dataframe(df)
    packer, rectangles, bins, all_rects = mpr.pack_patterns(pattern_list, fabric_width, fabric_height)
    #fig = plot_patterns(fabric_width, fabric_height, patterns)
    fig =mpr.visualize_packing(packer, fabric_width, fabric_height)
    st.pyplot(fig)
