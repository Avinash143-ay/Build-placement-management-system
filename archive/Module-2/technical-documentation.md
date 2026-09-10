# Technical Documentation

## System Boundary

The project is a placement management system. Module 1 defines the normalized
relational model, Module 3 exposes the workflow through a JWT-protected Flask
API, and Module 4 provides an independent indexed-storage experiment for lookup
heavy workloads.

## Main Workflow

1. A user authenticates through `/api/auth/login` and receives a signed JWT.
2. Role claims restrict student, recruiter, and administrator operations.
3. Students browse open jobs and create one application per job.
4. Recruiters create jobs and update application status.
5. Administrators read aggregate counts for operational reporting.

## Design Decisions

- Foreign keys and unique constraints enforce ownership and prevent duplicate
  applications at the database boundary.
- The local API uses SQLite for a zero-setup demonstration; the equivalent MySQL
  schema is provided in Module 1 for deployment.
- Passwords are hashed in the local demo seed. Production deployments should use
  a secret manager and rotate the JWT signing key.
- The B+ tree is evaluated against a linear scan using deterministic input and
  records both the machine and interpreter version.

## Performance Snapshot

The checked-in benchmark was run with 10,000 records, seed `42`, and Python 3.11.
On the development machine, exact lookup was approximately 57x faster and range
lookup approximately 40x faster with the B+ tree. Insertion was approximately
13x slower, which is the expected write/read tradeoff for a secondary index.
See `Module-4/database/benchmark_results.json` for raw measurements.