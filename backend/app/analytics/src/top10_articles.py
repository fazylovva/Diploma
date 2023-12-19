import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="womensdiary", user="master", password="secret", host="localhost", port="5432")
cur = conn.cursor()

# Execute the SQL query to retrieve the data
cur.execute("""
            SELECT a.title, COUNT(va.id) AS view_count, u.email, u.username FROM "Article" a
            INNER JOIN "Viewed Article" va ON a.id = va.article_id
            INNER JOIN "User" u ON a.author_id = u.id
            GROUP BY a.title, u.email, u.username
            ORDER BY view_count DESC
            LIMIT 10
""")
rows = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
data = np.array(rows)
df = pd.DataFrame(data, columns=col_names)

# Sort the dataframe by view count in descending order
df = df.sort_values('view_count', ascending=True)

# Close the database connection
cur.close()
conn.close()

# Create a column chart to visualize the data
fig, ax = plt.subplots(figsize=(10, 12))  # Adjust the figsize as desired
ax.bar(df['title'], df['view_count'])
ax.set_xlabel('Article Title')
ax.set_ylabel('Number of Views')
ax.set_title('Top 10 Most Popular Articles')

# Add the author's name as x-axis tick labels
plt.xticks(rotation=90)
ax.set_xticklabels(df['email'], rotation=90)

# Adjust the spacing between subplots
plt.subplots_adjust(bottom=0.2)  # Adjust the bottom value as needed

# Save the plot as a PNG file
fig.savefig('../static/analytics/images/plot/top10_articles.png', transparent=True)

# Show the plot
plt.show()
