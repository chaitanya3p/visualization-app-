import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load file
@st.cache_data
def load_file(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                return pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                return pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file type")
                return None
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

# Streamlit App
st.title('Multi-Visualization Streamlit App with Selection')

uploaded_file = st.file_uploader("Upload any data file (CSV, Excel, JSON)", type=['csv', 'xlsx', 'xls', 'json'])
data = load_file(uploaded_file)

if data is not None:
    st.write('Data Preview:')
    st.dataframe(data.head())

    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_columns) < 2:
        st.warning('Need at least two numeric columns for visualizations')
    else:
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox('Select X axis', numeric_columns, index=0)
        with col2:
            y_axis = st.selectbox('Select Y axis', numeric_columns, index=1)

        st.subheader('Select Visualizations to Display')
        show_scatter = st.checkbox('Scatter Plot', value=True)
        show_histogram = st.checkbox(f'Histogram of {x_axis}', value=True)
        show_boxplot = st.checkbox(f'Boxplot of {y_axis}', value=True)

        if show_scatter:
            st.subheader('Scatter Plot')
            fig1, ax1 = plt.subplots()
            sns.scatterplot(data=data, x=x_axis, y=y_axis, ax=ax1)
            st.pyplot(fig1)

        if show_histogram:
            st.subheader(f'Histogram of {x_axis}')
            fig2, ax2 = plt.subplots()
            sns.histplot(data[x_axis], bins=20, kde=True, ax=ax2)
            st.pyplot(fig2)

        if show_boxplot:
            st.subheader(f'Boxplot of {y_axis}')
            fig3, ax3 = plt.subplots()
            sns.boxplot(y=data[y_axis], ax=ax3)
            st.pyplot(fig3)
else:
    st.info('Upload a data file to get started.')
