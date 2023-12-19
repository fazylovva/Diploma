import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import pandas as pd

# connect to the PostgreSQL database
conn = psycopg2.connect(database="womensdiary", user="master", password="secret", host="localhost", port="5432")
cur = conn.cursor()

# execute the SQL query and retrieve the data as a Pandas DataFrame
cur.execute("SELECT * FROM discussion_likes_dislikes")
rows = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
data = np.array(rows)
df = pd.DataFrame(data, columns=col_names)

# convert likes and dislikes counts to integers
df['likes'] = df['likes'].astype(int)
df['dislikes'] = df['dislikes'].astype(int)

# calculate the total count and percentage difference between likes and dislikes
likes_count = df['likes'].sum()
dislikes_count = df['dislikes'].sum()
total_count = likes_count + dislikes_count

if likes_count == dislikes_count:
    sizes = [total_count / 2, total_count / 2]
    colors = ['tab:red', 'tab:blue']
    labels = [f'Likes ({likes_count})', f'Dislikes ({dislikes_count})']
else:
    percentage_diff = abs(likes_count - dislikes_count) / total_count * 100
    sizes = [likes_count, dislikes_count]
    colors = ['tab:red', 'tab:blue']
    labels = [f'Likes ({likes_count}) {likes_count/total_count*100:.2f}%',
              f'Dislikes ({dislikes_count}) {dislikes_count/total_count*100:.2f}%']

# create a pie chart to visualize the data
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.set_title('Discussion Likes/Dislikes')

# save the plot as a PNG file with a transparent background
fig.savefig('../static/analytics/images/plot/discussion_like_dislike.png', transparent=True)

# close the database connection
cur.close()
conn.close()
