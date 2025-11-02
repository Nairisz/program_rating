import streamlit as st
import pandas as pd
from ga_ratings import run_genetic_algorithm # import GA logic

st.title("Scheduling using Genetic Algorithm")

co_r = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8)
mut_r = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02)

if st.button("Run Genetic Algorithm"):
    schedule = ga_ratings.run_genetic_algorithm(co_r, mut_r)
    st.subheader("Generated Schedule")
    st.table(schedule)
