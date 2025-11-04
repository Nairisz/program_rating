
import csv
import streamlit as st
import random

random.seed() # For reproducibility

# Function to read the CSV file and convert it to the desired format
def read_csv_to_dict(file_path):
    program_ratings = {}
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            # Skip the header
            header = next(reader)
            
            for row in reader:
                if not row: continue # Skip empty rows
                program = row[0]
                # Ensure conversion to float, handle potential errors
                try:
                    ratings = [float(x) for x in row[1:]]
                    program_ratings[program] = ratings
                except ValueError:
                    st.error(f"Error converting ratings for program: {program}. Skipping.")
        
        if not program_ratings:
            st.error("No data loaded from CSV. Is the file empty or formatted incorrectly?")
            return None

        # Check if all programs have the same number of rating slots
        it = iter(program_ratings.values())
        first_len = len(next(it))
        if not all(len(ratings) == first_len for ratings in it):
            st.warning("Warning: Programs have a different number of rating slots. This may cause issues.")
            
        return program_ratings, first_len

    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return None, 0
    except Exception as e:
        st.error(f"An error occurred while reading the CSV: {e}")
        return None, 0

# Path to the CSV file
file_path = "program_ratings.csv"

# Get the data in the required format
program_ratings_dict, num_slots_from_csv = read_csv_to_dict(file_path)

# Stop execution if CSV reading failed
if program_ratings_dict is None:
    st.stop()


##################################### DEFINING PARAMETERS AND DATASET ################################################################
# Sample rating programs dataset for each time slot.
ratings = program_ratings_dict

GEN = 200 #asal 100
POP = 150 # asal 50
EL_S = 2 #2

all_programs = list(ratings.keys()) # all programs
# Use the number of slots from the CSV file
all_time_slots = list(range(6, 6 + num_slots_from_csv)) 

if not all_programs:
    st.error("No programs were loaded. Cannot run algorithm.")
    st.stop()

if len(all_time_slots) == 0:
    st.error("No time slots available (check CSV columns). Cannot run algorithm.")
    st.stop()

######################################### DEFINING FUNCTIONS ########################################################################
# defining fitness function
def fitness_function(schedule):
    total_rating = 0
    # Ensure schedule length matches time slots
    schedule_len = min(len(schedule), len(all_time_slots))
    for time_slot in range(schedule_len):
        program = schedule[time_slot]
        if program in ratings:
            total_rating += ratings[program][time_slot]
    return total_rating

############################################# GENETIC ALGORITHM #############################################################################

# Crossover
def crossover(schedule1, schedule2):
    # Handle schedules of potentially different lengths (though they should be the same)
    min_len = min(len(schedule1), len(schedule2))
    if min_len < 2:
        return schedule1, schedule2 # Not enough length to cross over

    crossover_point = random.randint(1, min_len - 1)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

# mutating
def mutate(schedule):
    # Ensure schedule is not empty
    if not schedule:
        return schedule
        
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

# calling the fitness func.
def evaluate_fitness(schedule):
    return fitness_function(schedule)

# genetic algorithms with parameters
def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP, crossover_rate=0.7, mutation_rate=0.3, elitism_size=EL_S):

    population = [initial_schedule]

    # Create initial population by shuffling the seed
    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []

        # Elitism
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

    # Ensure population is returned to the correct size
    population = new_population[:population_size]

    # Return the best schedule found
    population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
    return population[0]

##################################################### RESULTS ###################################################################################

st.title("📺 TV Program Schedule Optimizer (Original)")
st.markdown(" ##### (This is using Original CSV) ")

# --- Sliders ---
co_r = st.slider(
    "Crossover Rate", 
    min_value=0.1, 
    max_value=0.95, 
    value=0.8,  # Default value
    step=0.01
)
mut_r = st.slider(
    "Mutation Rate", 
    min_value=0.0, 
    max_value=0.5, 
    value=0.2,  # Default value
    step=0.1
)

# --- "Run" Button ---
if st.button("Run Genetic Algorithm"):
    st.subheader("Running Optimization...")
    progress_bar = st.progress(0, "Initializing...")

    # Create ONE random initial schedule
    # The correct way to seed a GA
    initial_schedule = [random.choice(all_programs) for _ in all_time_slots]

    # Run the genetic algorithm
    #  Pass the slider values (co_r, mut_r) to the function
    final_schedule = genetic_algorithm(
        initial_schedule, 
        generations=GEN, 
        population_size=POP, 
        crossover_rate=co_r,  # <-- Using slider value
        mutation_rate=mut_r,   # <-- Using slider value
        elitism_size=EL_S
    )

    progress_bar.progress(100, "Optimization Complete!")

    # Display the final results
    st.subheader("\n🏆 Final Optimal Schedule")
    
    # Create a simple table for results
    results_data = []

    for time_slot_index, program in enumerate(final_schedule):
        # Handle case where schedule is shorter than time slots
        if time_slot_index < len(all_time_slots):
            time_str = f"{all_time_slots[time_slot_index]:02d}:00"
            
            # Get the specific rating for this program at this time
            program_rating = ratings[program][time_slot_index] 
            
            results_data.append({
                "Time Slot": time_str, 
                "Program": program,
                "Rating": f"{program_rating:.1f}" # Format to 1 decimal places
            })
    
    st.table(results_data)
    
    st.write("---")
    st.header(f"⭐ Total Ratings: {fitness_function(final_schedule):.1f}")

else:
    st.info("Adjust parameters on the sliders and click 'Run Genetic Algorithm' to start.")
