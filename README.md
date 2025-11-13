# Python
Run the excercise DB
cd C:\Users\plangley.PROGRESS\Desktop
python exercise_app.py
http://localhost:5000

## SQL

## All databases
```
SELECT datname FROM pg_database;
```

## Retun all the tables in a database
```
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```
## Return all the data in the excercises table
`Select * from exercises`

## insert record into database
```
import psycopg2

try:
    # Connect to the exercise_tracker database
    conn = psycopg2.connect(
        host="localhost",
        database="exercise_tracker", #The name of the database
        user="postgres", #the database user
        password="admin" #the password
    )

    # Create a cursor
    cur = conn.cursor()

    # Create the exercises table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
        )
    """)
    print("Table created/verified")

    # Insert the exercise record
    cur.execute(
        "INSERT INTO exercises (name, description) VALUES (%s, %s)",
        ("pullups", "do some pullups")
    )
    print("Record inserted")

    # Commit the transaction
    conn.commit()
    print("Transaction committed")

    # Verify the insert
    cur.execute("SELECT * FROM exercises")
    rows = cur.fetchall()
    print(f"\nAll records in exercises table:")
    for row in rows:
        print(row)

    # Close cursor and connection
    cur.close()
    conn.close()

    print("\nExercise record added successfully!")

except Exception as e:
    print(f"Error: {e}")
```
