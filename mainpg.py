import streamlit as st

# Set the title and icon for the page
st.set_page_config(
    page_title="Program Schedule Optimizer using GA", #untuk header taskbar
    page_icon="📺", #untuk header taskbar
)

ori_slider = st.Page('gen_algo.py', title='Original: Program Schedule Optimizer')
edited_slider = st.Page('tsp.py', title='Edited: Program Schedule Optimizer')

pg = st.navigation(
        {
            "Menu": [ori_slider, edited_slider]
        }
    )

pg.run()
