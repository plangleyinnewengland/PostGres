import psycopg2

try:
    # Connect to the exercise_tracker database
    conn = psycopg2.connect(
        host="localhost",
        database="exercise_tracker",
        user="postgres",
        password="admin"
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