import pandas as pd
from langsmith import Client
import plotly.express as px
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

# Function to plot the leaderboard using Plotly
def plot_leaderboard(df):
    user_counts = df["username"].value_counts().reset_index()
    user_counts.columns = ["Username", "Number of prompts"]

    # Create an interactive bar chart with Plotly
    fig = px.bar(
        user_counts,
        x="Username",
        y="Number of prompts",
        text="Number of prompts",
        color="Number of prompts",
        color_continuous_scale="purples",  # Use "purples" color scale
        title="Leaderboard - Student Gator",
    )

    # Update layout for better visual appeal and readability
    fig.update_layout(
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#FFFFFF",
        title_font=dict(size=20, color="#773095"),
        xaxis=dict(
            tickangle=-45, 
            showgrid=False,
            tickfont=dict(color="black"),  # Set x-axis text color to black
            title=dict(text="Username", font=dict(color="black")),  # Set x-axis title color to black
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor="lightgray",
            tickfont=dict(color="black"),  # Set y-axis text color to black
            title=dict(text="Number of prompts", font=dict(color="black")),  # Set y-axis title color to black
        ),
        font=dict(size=14, color="black"),  # Set global font color to black
    )

    # Update text on bars for better readability
    fig.update_traces(
        textfont=dict(size=14, color="black"),  # Set text color to white for contrast
        textposition="outside",  # Position text outside the bars
    )

    return fig


# Streamlit app
def main():
    st.title("Real-Time Leaderboard Dashboard")

    # Fetch data
    df = fetch_data()

    # Plot and display the leaderboard
    st.write("### Leaderboard")
    fig = plot_leaderboard(df)
    st.plotly_chart(fig, use_container_width=True)

    # Auto-refresh every 60 seconds
    time.sleep(60)
    st.rerun()

if __name__ == "__main__":
    main()