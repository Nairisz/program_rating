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
st.write(f"- Population Size: {POP}")
st.write(f"- Elitism Size: {EL_S}")

if st.button("Run Genetic Algorithm"):
    with st.spinner("Running genetic algorithm..."):
        # Your existing genetic algorithm code here
        initial_best_schedule = finding_best_schedule(all_possible_schedules)
        rem_t_slots = len(all_time_slots) - len(initial_best_schedule)
        genetic_schedule = genetic_algorithm(initial_best_schedule, generations=GEN, population_size=POP, elitism_size=EL_S)
        final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

        st.success("Optimization Complete!")
        
        st.subheader("Final Optimal Schedule:")
        for time_slot, program in enumerate(final_schedule):
            st.write(f"Time Slot {all_time_slots[time_slot]:02d}:00 - Program {program}")

        st.metric("Total Ratings", f"{fitness_function(final_schedule):.2f}")
