from db_manager import Database 
from table import  Table

# Create or load the database
db = Database('placement_db')



# --- STUDENTS TABLE ---
db.delete_table('college')  # Clean slate
college = db.create_table(
    name='college',
    columns={
        'student_id': int,
        'name': str,
        'email': str,
        'phone': str,
        'department': str,
        'cgpa': float,
        'placement_status': str,
        'image': bytes,
        'company_id': int,
        'password': str
    },
    primary_key='student_id'
)

college.insert({
    'student_id': 1,
    'name': 'Alice',
    'email': 'alice@example.com',
    'phone': '1234567890',
    'department': 'CSE',
    'cgpa': 8.9,
    'placement_status': 'Placed',
    'image': b'',
    'company_id': 101,
    'password': 'secure123'
})

college.insert({
    'student_id': 2,
    'name': 'Bob',
    'email': 'bob@example.com',
    'phone': '9876543210',
    'department': 'ECE',
    'cgpa': 7.8,
    'placement_status': 'Not Placed',
    'image': b'',
    'company_id': 102,
    'password': 'password123'
})

# --- COMPANIES TABLE ---
db.delete_table('companies')  # Clean slate
companies = db.create_table(
    name='companies',
    columns={
        'company_id': int,
        'name': str,
        'industry': str,
        'contact_email': str,
        'contact_phone': str
    },
    primary_key='company_id'
)

companies.insert({
    'company_id': 101,
    'name': 'Google',
    'industry': 'Tech',
    'contact_email': 'contact@google.com',
    'contact_phone': '1112223333'
})

companies.insert({
    'company_id': 102,
    'name': 'Amazon',
    'industry': 'E-Commerce',
    'contact_email': 'hr@amazon.com',
    'contact_phone': '4445556666'
})

# Show data
print(" college table:")
college.show()

print(" Companies Table:")
companies.show()

# --- SAVE / PERSIST THE DATABASE ---
# Saving (persisting) tables
companies.persist('saved_tables')
college.persist('saved_tables')



print("Database 'placement_db' has been saved to disk (each table saved as .pkl)")