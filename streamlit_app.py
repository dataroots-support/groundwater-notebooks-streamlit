import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Injecting custom CSS
st.markdown(
    """
    <style>
    header {
        display: none !important;
    }
    .block-container {
        padding: 2rem 0 !important;
    }
    
    /* Light theme background and text colors */
    body {
        background-color: white;
        color: black;
    }
    .stApp {
        background-color: white;
    }
    .block-container {
        padding: 0 !important;
    }
    /* Change the header color */
    .stMarkdown h1, h2, h3, h4, h5, h6 {
        color: black;
    }
    /* Style input fields, buttons, and widgets */
    input[type="number"], input[type="text"],
    .stNumberInput > div, .stTextInput > div,
    .stTextInput, .stNumberInput, .stSlider, .stButton {
        color: black;
        background-color: white;
        border-color: black;
    }
    .stNumberInput input {
        background-color: white;
        color: black;
    }
    .stSlider .st-bx, .stSlider .st-slider, p {
        color: black;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Function for catchment width
def ymax_conf(Q, K, i, b):
    return Q / (2. * K * i * b)

# Function for the culmination point
def x0_conf(Q, K, i, b):
    return -Q / (2. * np.pi * K * i * b)

# Computation of the well catchment
def plot_catchment(Q, K, i, b, x_scale, y_scale, x_point, y_point):
    x_max = 1000  # Internal parameter to define the number range
    ymax = ymax_conf(Q, K, i, b)
    x0 = x0_conf(Q, K, i, b)

    y = np.arange(-ymax * 0.999, ymax, 0.1)
    x = -1 * y / (np.tan(2 * np.pi * K * i * b * y / Q))

    # Scale the plot as per user input
    x_plot = 500 * x_scale
    y_plot = 1000 * y_scale

    # Creating the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(x, y, label='Stream divide')
    plt.plot(x_point, y_point, marker='o', color='r', linestyle='None', label='Marked point')
    ax.set(xlabel='x (m)', ylabel='y (m)', title='Catchment area of a pumping well')
    ax.set(xlim=(-x_plot, 10 * x_plot), ylim=(-y_plot, y_plot))
    plt.fill_between(x, y, color='blue', alpha=.1)
    plt.fill_between(x, -y, color='blue', alpha=.1)
    ax.grid()
    plt.legend()
    st.pyplot(fig)

    st.write("y_max: %5.2f" % ymax)
    st.write('x_0:  %5.2f' % x0)

# Hydraulic conductivity (K) as a normal input field
K = st.number_input('Hydraulic conductivity (K)', value=457.5 / 86400, format="%.6e", key="K_input")

# Other input fields as number inputs
Q = st.number_input('Abstraction rate (Q)', value=4320 / 86400, format="%.6f", key="Q_input")
i = st.number_input('Regional gradient (i)', value=0.003, step=0.001, format="%.3f", key="i_input")  # Three decimal places
b = st.number_input('Aquifer thickness (b)', value=23, key="b_input")
x_scale = st.slider('X Scale', min_value=0.1, max_value=10.0, value=0.3, step=0.1, key="x_scale_slider")
y_scale = st.slider('Y Scale', min_value=0.1, max_value=10.0, value=0.3, step=0.1, key="y_scale_slider")
x_point = st.number_input('X point', value=0, key="x_point_input")
y_point = st.number_input('Y point', value=0, key="y_point_input")

# Automatically plot the catchment area on load and update when inputs change
plot_catchment(Q, K, i, b, x_scale, y_scale, x_point, y_point)
