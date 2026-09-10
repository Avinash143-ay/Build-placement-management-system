# DBMS Interview and Viva Preparation

## Project Explanation In One Minute

This is a campus placement management system. I designed a normalized ten-table
relational schema, built a Flask API with JWT authentication and role-based
authorization, and implemented student, recruiter, and admin workflows. I also
implemented a B+ Tree from scratch and benchmarked it against a linear scan. On
10,000 records, exact lookup was about 57x faster and range lookup about 40x
faster on the benchmark machine.

## DBMS Concepts Used

### Keys and relationships

A primary key uniquely identifies a row, for example `user_id`, `job_id`, and
`application_id`. A foreign key maintains a valid relationship, such as
`applications.student_id` referencing `students.student_id`. The pair
`(job_id, student_id)` is a composite unique key that prevents duplicate
applications.

`users` to `students` is one-to-one because `students.user_id` is unique. One
company can publish many jobs, so `job_postings` contains `company_id`. Students
and jobs are many-to-many, resolved through `applications`.

### Normalization

The schema reaches third normal form. Columns are atomic, relationship data is
separated into its own table, and non-key facts depend only on their table key.
Company information is stored once in `companies`, not repeated in every job.

### Indexing

An index organizes keys for faster access. The SQL schema adds indexes for job
deadlines and student application status. The custom B+ Tree demonstrates the
same idea independently of MySQL.

### B+ Tree versus B Tree

In a B+ Tree, records are stored in leaf nodes and leaf nodes are linked. Internal
nodes store routing keys. Linked leaves make range queries efficient because the
scan can continue after finding the first matching leaf.

### Transactions

The application commits after creating an application or job. A production
version should add explicit rollback handling around every multi-step transaction.

## Common Interview Questions

### Why use a separate applications table?

Students and jobs have a many-to-many relationship. The application row also
stores relationship attributes such as status and applied time.

### How are duplicate applications prevented?

The API handles the conflict and the database enforces `UNIQUE(job_id, student_id)`.
The database constraint is the final protection against race conditions.

### Why use JWT?

JWT lets the API verify identity without storing a server-side session for every
request. The token contains the user ID and role, is signed by the server, and
expires. Authentication verifies identity; authorization checks permissions.

### What is B+ Tree search complexity?

For a balanced tree, exact search is approximately $O(\log_m n)$, where $m$ is
the branching factor. A range query costs approximately $O(\log_m n + k)$,
where $k$ is the number of matching records.

### Why was insertion slower in the benchmark?

The linear list simply appends. The B+ Tree performs ordered insertion and may
split nodes, so writes pay index-maintenance cost in exchange for faster reads.

### Why use MySQL?

MySQL is the deployment database for this project. The API uses the canonical
MySQL schema and parameterized queries, so the application and database model
share one production-oriented contract.

### What would you improve next?

I would add pagination, refresh tokens, interview endpoints, Docker Compose,
database migrations, and load testing with realistic concurrent users.

## Demonstration Order

1. Run `python run.py`.
2. Open `http://127.0.0.1:5000`.
3. Log in with the student account and apply to the demo job.
4. Log in with the recruiter account and create a job.
5. Run `pytest -q` to show automated verification.
6. Run `python database/benchmark.py` to show indexing evidence.