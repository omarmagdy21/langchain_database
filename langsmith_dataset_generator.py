import pandas as pd
from langsmith import Client

usernames = []
inputs = []
ouputs = []
run_ids = []
feedback_stats = []

# Initialize the LangSmith client
client = Client(api_key='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')
# Get runs (modify filters based on your needs)
runs = client.list_runs(project_name="counseling", is_root=1)

jsons = []

for run in runs :
    jsons.append(run)
    usernames.append(run.metadata['username'])
    inputs.append(run.inputs['user_input'])
    ouputs.append(run.outputs['output'])
    run_ids.append(run.id)


# In[215]:


print(f'Total runs: {len(jsons)}')

#create a datfarame contains all the data from username, input, output, run_id
df = pd.DataFrame(list(zip(usernames, inputs, ouputs, run_ids)), columns =['username', 'input', 'output', 'run_id'])
df.to_csv('data.csv', index=False)

#remove any usernames containing more than 3 spaces after spliting by space
df = df[df['username'].apply(lambda x: len(x.split()) <= 3)]

#drop username hi
df = df[df['username'] != 'hi']

#make all usernames lowercase
df['username'] = df['username'].str.lower()

import matplotlib.pyplot as plt
user_counts = df["username"].value_counts()

# Define company colors
background_color = "#ffffff"  # Dark purple
text_color = "black"
bar_color = "#773095"  # Lighter purple shade

# Create the plot
plt.figure(figsize=(12, 6), facecolor=background_color)
ax = plt.gca()
ax.set_facecolor(background_color)

# Plot bar chart
user_counts.plot(kind="bar", color=bar_color, edgecolor="white")

# Set labels and title with custom colors
plt.xlabel("Username", fontsize=14, color=text_color)
plt.ylabel("Number of Records", fontsize=14, color=text_color)
plt.title("Leaderboard - Student Gator", fontsize=16, color=text_color)

# Modify tick colors
plt.xticks(rotation=45, ha="right", color=text_color, fontsize=12)
plt.yticks(range(0, max(user_counts) + 2, 2), color=text_color, fontsize=12)

# Grid styling
plt.grid(axis="y", linestyle="--", alpha=0.6, color="black")

# save the fig
plt.savefig('leaderboard.png')


