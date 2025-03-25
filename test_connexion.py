import pyodbc



# Variables for server and database
server = 'localhost\SQLEXPRESS'
database = 'nrj_data'

# Function to test connection to SQL Server using Windows Authentication
def test_connection():
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={server};'        # Using the variable for server
                              f'DATABASE={database};'    # Using the variable for database
                              'Trusted_Connection=yes')  # Use Windows Authentication
        print("Connection successful!")
        return conn  # Return the connection object
    except Exception as e:
        print(f"Failed to connect: {e}")

# Test the connection
test_connection()