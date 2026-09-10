# Placement Management System: Project Report

## 1. Abstract

The Placement Management System digitizes campus recruitment workflows. Students
discover eligible jobs and submit applications, recruiters publish openings and
move candidates through a hiring pipeline, and administrators monitor aggregate
placement activity. The project demonstrates database design, backend API
development, authentication, authorization, documentation, and index
performance in one system.

## 2. Problem Statement

Placement data is commonly spread across spreadsheets, email, and disconnected
records. That makes duplicate applications, eligibility mistakes, status
tracking, and reporting difficult. This system centralizes the data and enforces
important rules at both the API and database layers.

## 3. Objectives

- Design a normalized relational database for placement operations.
- Provide secure login using signed JWTs.
- Enforce different permissions for students, recruiters, and administrators.
- Prevent duplicate applications and invalid student eligibility.
- Provide a portable MySQL schema and deployment configuration.
- Compare B+ Tree lookup performance with a linear scan.
- Document the architecture using ER, UML, sequence, state, and deployment views.

## 4. System Architecture

```text
Browser / API client
        |
        v
Flask application - routes, JWT, RBAC, validation
        |
        +--> MySQL deployment database
        |
        +--> B+ Tree indexing experiment
```

The application is implemented in [placement_system/app.py](../placement_system/app.py).
The canonical SQL model is in [database/schema.sql](../database/schema.sql).

## 5. Database Tables

| Table | Responsibility | Important relationships |
| --- | --- | --- |
| `roles` | Defines `admin`, `student`, and `recruiter` roles. | One role has many users. |
| `users` | Stores identity, email, password hash, and name. | Belongs to one role. |
| `students` | Stores roll number, department, CGPA, and graduation year. | One-to-one with a user. |
| `companies` | Stores employer information. | Has recruiters and job postings. |
| `recruiters` | Connects a user to a company. | One recruiter belongs to one company. |
| `job_postings` | Stores role, description, package, eligibility, and deadline. | Belongs to one company. |
| `applications` | Connects students to jobs and stores status. | Resolves the many-to-many relationship. |
| `interviews` | Stores interview schedule and mode. | Belongs to one application. |
| `recruiter_feedback` | Stores rating and comments for an application. | At most one feedback per application. |
| `placements` | Stores final placement date and package. | At most one placement per application. |

## 6. Normalization

The schema is designed to third normal form. First normal form is achieved by
using atomic columns and avoiding repeating groups. Second normal form is
achieved by resolving the student-job many-to-many relationship through
`applications`. Third normal form is achieved by storing company and role facts
once instead of repeating them in every job or user row.

## 7. Core Workflows

### Login

1. The client sends email and password.
2. The API loads the user and role.
3. Werkzeug verifies the password hash.
4. The API signs a JWT containing the user ID and role.
5. The client sends the token as a Bearer token on protected requests.

### Student application

1. The student requests open jobs.
2. The API identifies the student profile from the JWT user ID.
3. The API checks that the job is open.
4. The API compares the student CGPA with the job requirement.
5. The database unique constraint prevents a duplicate application.

### Recruiter review

1. The recruiter creates a job under the recruiter company.
2. The recruiter updates an application to `shortlisted`, `rejected`, or `hired`.
3. The update query verifies that the job belongs to the recruiter company.

## 8. Security

- Passwords are stored as Werkzeug-generated password hashes.
- Passwords are never returned by API responses.
- JWTs are signed with `SECRET_KEY` and expire after two hours.
- Every protected endpoint requires a Bearer token.
- Role decorators reject unauthorized operations with HTTP 403.
- SQL parameters are bound rather than concatenated into queries.
- Production deployments should use a secret manager and HTTPS.

## 9. B+ Tree Experiment

The custom index stores sorted keys in linked leaf nodes. Internal nodes guide
search, while leaf links make range scans efficient. The benchmark compares the
tree with a list-based linear scan over 10,000 deterministic records.

The checked-in run shows approximately 57x faster exact lookup and 40x faster
range queries. Insertions are slower because the tree maintains ordering and
splits nodes during writes. Raw measurements are in
[database/benchmark_results.json](../database/benchmark_results.json).

## 10. Limitations and Future Work

- Add refresh tokens and account lockout for production authentication.
- Add pagination and filtering for large job/application lists.
- Add interview scheduling and feedback API endpoints.
- Add a background job for placement analytics.
- Deploy behind Gunicorn and a reverse proxy.
- Add Docker Compose for Flask and MySQL.