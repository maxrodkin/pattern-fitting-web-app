import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import make_pattern_rectpack as mpr

def plot_patterns(fabric_width, fabric_height, patterns):
    fig, ax = plt.subplots(1)
    ax.set_xlim(0, fabric_width)
    ax.set_ylim(0, fabric_height)
    ax.add_patch(patches.Rectangle((0, 0), fabric_width, fabric_height, edgecolor='black', facecolor='none'))
    current_x = 0
    current_y = 0
    max_row_height = 0
    for _, row in patterns.iterrows():
        width = int(row['width'])
        height = int(row['height'])
        if current_x + width > fabric_width:
            current_x = 0
            current_y += max_row_height
            max_row_height = 0
        if current_y + height > fabric_height:
            continue
        ax.add_patch(patches.Rectangle((current_x, current_y), width, height, edgecolor='blue', facecolor='lightblue'))
        ax.text(current_x + width/2, current_y + height/2, row['pattern'], ha='center', va='center')
        current_x += width
        max_row_height = max(max_row_height, height)
    plt.gca().set_aspect('equal', adjustable='box')
    return fig

st.title("Pattern Fitting Web App")
st.write("Upload your CSV and visualize pattern fitting.")

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
    # # Example: extract fabric and patterns (adapt as needed)
    # fabric = df[df['pattern'] == 'fabric'].iloc[0]
    # patterns = df[df['pattern'] != 'fabric']
    # fabric_width = int(fabric['width'])
    # fabric_height = int(fabric['height'])
    packer, rectangles, bins, all_rects = mpr.pack_patterns(pattern_list, fabric_width, fabric_height)
    #fig = plot_patterns(fabric_width, fabric_height, patterns)
    fig =mpr.visualize_packing(packer, fabric_width, fabric_height)
    st.pyplot(fig)
