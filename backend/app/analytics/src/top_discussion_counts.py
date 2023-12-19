import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="womensdiary", user="master", password="secret", host="localhost", port="5432")
cur = conn.cursor()

# Execute the SQL query to retrieve the data
cur.execute("""
    SELECT a.id, COUNT(d.id) AS discussion_count
    FROM "Article" a
    LEFT JOIN "Discussion" d ON a.id = d.article_id
    GROUP BY a.id
    ORDER BY discussion_count DESC
    LIMIT 10
""")
rows = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
data = np.array(rows)
df = pd.DataFrame(data, columns=col_names)

# Create a bar chart to visualize the data
fig, ax = plt.subplots()
ax.bar(df['id'], df['discussion_count'], color='tab:blue')
ax.set_xlabel('Article ID')
ax.set_ylabel('Discussion Count')
ax.set_title('Top 10 Most Active Articles')

# Save the plot as a PNG file
fig.savefig('../static/analytics/images/plot/most_active_articles.png')

# Close the database connection
cur.close()
conn.close()
