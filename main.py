import streamlit as st

# Main Streamlit app
st.title("📺 TV Program Scheduling Optimizer")

# Sidebar for parameters
st.sidebar.header("Genetic Algorithm Parameters")

# Sliders for crossover and mutation rates
CO_R = st.sidebar.slider("Crossover Rate", 0.1, 1.0, 0.7, 0.05)
MUT_R = st.sidebar.slider("Mutation Rate", 0.1, 0.5, 0.3, 0.05)

# Display current parameters
st.write(f"**Current Parameters:**")
st.write(f"- Crossover Rate: {CO_R}")
st.write(f"- Mutation Rate: {MUT_R}")

if st.button("Run Genetic Algorithm"):
    with st.spinner("Running genetic algorithm..."):
        # This will call your genetic algorithm functions
        # You'll need to connect this to your main code
        pass
