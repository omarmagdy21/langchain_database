import pandas as pd
from langsmith import Client
import matplotlib.pyplot as plt
import streamlit as st
import time

# Initialize the LangSmith client
client = Client(api_key='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')

# Cache the data fetching function to avoid reloading data unnecessarily
@st.cache_data(ttl=60)  # Refresh every 60 seconds
def fetch_data():
    runs = client.list_runs(project_name="counseling", is_root=1)
    usernames = []
    inputs = []
    outputs = []
    run_ids = []

    for run in runs:
        usernames.append(run.metadata['username'])
        inputs.append(run.inputs['user_input'])
        outputs.append(run.outputs['output'])
        run_ids.append(run.id)

    # Create a DataFrame
    df = pd.DataFrame(list(zip(usernames, inputs, outputs, run_ids)), columns=['username', 'input', 'output', 'run_id'])

    # Remove any usernames containing more than 3 spaces after splitting by space
    df = df[df['username'].apply(lambda x: len(x.split()) <= 3)]

    # Drop username 'hi'
    df = df[df['username'] != 'hi']

    # Make all usernames lowercase
    df['username'] = df['username'].str.lower()

    return df

# Function to plot the leaderboard
def plot_leaderboard(df):
    user_counts = df["username"].value_counts()

    # Define company colors
    background_color = "#ffffff"  # Dark purple
    text_color = "black"
    bar_color = "#773095"  # Lighter purple shade

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=background_color, dpi=400)
    ax.set_facecolor(background_color)

    # Plot bar chart
    user_counts.plot(kind="bar", color=bar_color, edgecolor="white", ax=ax)

    # Set labels and title with custom colors
    ax.set_xlabel("Username", fontsize=14, color=text_color)
    ax.set_ylabel("Number of Records", fontsize=14, color=text_color)
    ax.set_title("Leaderboard - Student Gator", fontsize=16, color=text_color)

    # Modify tick colors
    ax.tick_params(axis='x', rotation=45, colors=text_color, labelsize=12)
    ax.tick_params(axis='y', colors=text_color, labelsize=12)

    # Set y-axis ticks to whole numbers
    max_count = user_counts.max()  # Get the maximum count
    ax.set_yticks(range(0, max_count + 1))  # Set ticks from 0 to max_count + 1

    return fig

# Streamlit app
def main():
    st.title("Real-Time Leaderboard Dashboard")

    # Fetch data
    df = fetch_data()


    # Plot and display the leaderboard
    st.write("### Leaderboard")
    fig = plot_leaderboard(df)
    st.pyplot(fig)

    # Auto-refresh every 60 seconds
    time.sleep(60)
    st.rerun()

if __name__ == "__main__":
    main()