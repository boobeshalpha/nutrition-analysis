import mysql.connector
from NEU import df_obesity, df_malnutrition

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="7904",   
    database="nutrition"
)

cursor = conn.cursor()

# Step 2: Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS obesity (
        Region VARCHAR(100),
        Gender VARCHAR(10),
        Year INT,
        LowerBound FLOAT,
        UpperBound FLOAT,
        Mean_Estimate FLOAT,
        Country VARCHAR(100),
        age_group VARCHAR(50),
        CI_Width FLOAT,
        obesity_level VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS malnutrition (
        Region VARCHAR(100),
        Gender VARCHAR(10),
        Year INT,
        LowerBound FLOAT,
        UpperBound FLOAT,
        Mean_Estimate FLOAT,
        Country VARCHAR(100),
        age_group VARCHAR(50),
        CI_Width FLOAT,
        malnutrition_level VARCHAR(50)
    )
''')

# Step 3: Insert data into tables
for _, row in df_obesity.iterrows():
    cursor.execute('''
        INSERT INTO obesity VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', tuple(row))

for _, row in df_malnutrition.iterrows():
    cursor.execute('''
        INSERT INTO malnutrition VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', tuple(row))

# Step 4: Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into MySQL successfully.")
