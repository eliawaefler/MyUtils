import os
import psycopg2


def write_to_db(table, data):
    """
    Write data to the specified table in the database after fetching the column names.

    Parameters:
        table (str): The name of the table to write to.
        data (list of tuples): A list of tuples containing the data to insert, aligning with the table's columns.
    """
    connection_string = os.environ.get('NEON_URL')
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    # Fetch column names from the table
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = [row[0] for row in cur.fetchall() if row[0] != 'id']  # Assuming 'id' is auto-increment and not needed in the insert

    # Prepare the SQL command using the column names
    columns_sql = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table} ({columns_sql}) VALUES ({placeholders})"

    # Execute SQL commands to write to the database
    cur.executemany(query, data)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("Records inserted successfully")


def read_db(table, criteria='1=1'):
    """
    Read data from the specified table in the database based on criteria.

    Parameters:
        table (str): The name of the table to read from.
        criteria (str): SQL criteria for filtering data (default is '1=1' which selects all).
    """
    connection_string = os.environ.get('NEON_URL')
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    # Execute a select statement to read the data
    query = f"SELECT * FROM {table} WHERE {criteria}"
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()


def main():
    table_name = "home"
    data_to_insert = [("John", "Dog"), ("Jane", "Cat")]

    # Read all entries from the table
    print("Reading all entries from the database:")
    read_db(table_name)

    # Write new entries to the table
    write_to_db(table_name, data_to_insert)

    # Read specific entries from the table
    print("\nReading specific entries from the database:")
    read_db(table_name, "name='John' AND pet='Dog'")

    print("")
    print("")
    print("")
    read_db(table_name)


if __name__ == "__main__":
    main()
