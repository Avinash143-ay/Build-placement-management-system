# Placement Management System

A complete campus-placement product combining a normalized relational model,
JWT-secured workflows, role-based access control, architecture documentation, and
a custom B+ tree index.

## Product Structure

```text
placement_system/        Flask application package and web portal
database/                 Canonical SQL, B+ tree, benchmark, and results
docs/                     Nine-view architecture source, SVG, and design notes
tests/                    Project-level API and indexing tests
run.py                    Single development entry point
requirements.txt          Reproducible Python dependencies
archive/                   Original coursework archive and source history
```

The `archive/` folder is retained for traceability. The directories above are
the canonical project structure used by the application and README commands.

## Features

- Student, recruiter, and administrator roles
- JWT authentication with role-based authorization
- Job discovery and one-application-per-job enforcement
- Recruiter job posting and application status management
- Admin placement statistics
- Mock CIMS student verification endpoint
- Ten-table normalized MySQL schema with seed data
- Local SQLite demo mode with no external database required
- B+ tree exact lookup and range-query benchmark against a linear scan
- Nine architecture diagrams exported as SVG

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`. The local demo creates its SQLite database under
the Flask instance directory on first run.

Demo accounts:

| Role | Email | Password |
| --- | --- | --- |
| Student | `student@example.com` | `student123` |
| Recruiter | `recruiter@example.com` | `recruiter123` |
| Admin | `admin@example.com` | `admin123` |

## API Surface

| Method | Endpoint | Access |
| --- | --- | --- |
| `GET` | `/api/health` | Public |
| `POST` | `/api/auth/login` | Public |
| `GET` | `/api/jobs` | Public |
| `POST` | `/api/jobs/<job_id>/applications` | Student |
| `GET` | `/api/applications` | Student |
| `POST` | `/api/recruiter/jobs` | Recruiter |
| `PATCH` | `/api/recruiter/applications/<id>` | Recruiter |
| `GET` | `/api/admin/stats` | Admin |
| `GET` | `/api/cims/verify/<roll_number>` | Authenticated |

## Database Deployment

The local demo uses SQLite. For MySQL deployment, execute
[database/schema.sql](database/schema.sql) followed by [database/seed.sql](database/seed.sql).
The schema defines roles, users, students, companies, recruiters, job postings,
applications, interviews, feedback, and placements with constraints and indexes.

To run the Flask API against MySQL, first create the database and load the
canonical schema:

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS placement_system;"
mysql -u root -p placement_system < database/schema.sql
mysql -u root -p placement_system < database/seed.sql
```

Then set the variables shown in [.env.example](.env.example) in PowerShell and
start the application:

```powershell
$env:PLACEMENT_DB_DRIVER = "mysql"
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_DATABASE = "placement_system"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "your-password"
python run.py
```

The app uses the canonical `database/schema.sql` table names in MySQL mode. The
old SQL dump remains in `archive/` and is not part of the active application.

## Indexing Evidence

Run the deterministic benchmark from the repository root:

```powershell
python database/benchmark.py
```

Results are saved to [database/benchmark_results.json](database/benchmark_results.json).
The checked-in run shows approximately 57x faster exact lookup and 40x faster
range queries on 10,000 records, while insertion is slower because the index
maintains tree structure during writes.

## Verification

```powershell
pytest -q
python -m compileall -q placement_system database
```

## Placement Preparation Documents

- [Project report](docs/PROJECT_REPORT.md): complete system explanation and design decisions.
- [DBMS interview preparation](docs/DBMS_INTERVIEW_PREPARATION.md): project-specific viva questions and answers.
- [API and demo guide](docs/API_AND_DEMO_GUIDE.md): commands for demonstrating every major workflow.
- [ER diagram](docs/er_diagram.svg) and [ER source](docs/er_diagram.dot): database entities and relationships.
- [UML class diagram](docs/uml_class_diagram.svg) and [UML source](docs/uml_class_diagram.dot): application classes and responsibilities.
- [Architecture diagram](docs/architecture.svg): sequence, use-case, state, deployment, security, and data-flow views.



