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

    # Add hashtag column to exercises table
    cur.execute("""
        ALTER TABLE exercises 
        ADD COLUMN IF NOT EXISTS hashtag VARCHAR(100)
    """)
    
    # Also add photo_path column if you want to use the web form
    cur.execute("""
        ALTER TABLE exercises 
        ADD COLUMN IF NOT EXISTS photo_path VARCHAR(255)
    """)
    
    conn.commit()
    print("Columns added successfully!")
    
    # Verify the table structure
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'exercises'
    """)
    columns = cur.fetchall()
    print("\nCurrent table structure:")
    for col in columns:
        print(f"  {col[0]}: {col[1]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
