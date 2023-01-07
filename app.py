import numpy as np
import pandas as pd
import streamlit as st

mtab, etab = st.tabs(["Home", "About"])

with mtab:
  col1, col2 = st.columns(2)
  
  with col1:
    st.header("A cat")
