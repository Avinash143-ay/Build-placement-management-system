import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

import jwt
from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-secret"),
        MYSQL_HOST=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        MYSQL_PORT=int(os.environ.get("MYSQL_PORT", "3306")),
        MYSQL_DATABASE=os.environ.get("MYSQL_DATABASE", "placement_system"),
        MYSQL_USER=os.environ.get("MYSQL_USER", "root"),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD", ""),
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db:
            db.close()

    with app.app_context():
        db = get_db(app)
        initialize_database(app, db)
        seed_demo_data(db)
        db.commit()

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "placement-api"})

    @app.post("/api/auth/login")
    def login():
        payload = request.get_json(silent=True) or {}
        user = query_one(
            """SELECT u.user_id, u.email, u.full_name, u.password_hash, r.name AS role
               FROM users u JOIN roles r ON r.role_id = u.role_id WHERE u.email = ?""",
            (payload.get("email"),),
        )
        if not user or not check_password_hash(user["password_hash"], payload.get("password", "")):
            return jsonify({"error": "Invalid email or password"}), 401
        token = jwt.encode(
            {"sub": str(user["user_id"]), "role": user["role"], "exp": datetime.now(timezone.utc) + timedelta(hours=2)},
            app.config["SECRET_KEY"], algorithm="HS256"
        )
        return jsonify({"token": token, "user": public_user(user)})

    @app.get("/api/jobs")
    def jobs():
        rows = query_all(
            """SELECT j.*, c.name AS company_name FROM job_postings j
               JOIN companies c ON c.company_id = j.company_id
               WHERE j.status = 'open' ORDER BY j.application_deadline"""
        )
        return jsonify([dict(row) for row in rows])

    @app.get("/api/me")
    @requires_auth
    def me():
        return jsonify(g.current_user)

    @app.post("/api/jobs/<int:job_id>/applications")
    @requires_auth
    @requires_role("student")
    def apply(job_id):
        student = query_one("SELECT student_id FROM students WHERE user_id = ?", (g.current_user["user_id"],))
        job = query_one("SELECT job_id, minimum_cgpa FROM job_postings WHERE job_id = ? AND status = 'open'", (job_id,))
        if not student or not job:
            return jsonify({"error": "Open job or student profile not found"}), 404
        profile = query_one("SELECT cgpa FROM students WHERE student_id = ?", (student["student_id"],))
        if profile["cgpa"] < job["minimum_cgpa"]:
            return jsonify({"error": "Student does not meet the CGPA requirement"}), 400
        try:
            db = get_db(app)
            cursor = db.execute("INSERT INTO applications (job_id, student_id) VALUES (?, ?)", (job_id, student["student_id"]))
            db.commit()
        except Exception as error:
            if error.__class__.__name__ not in {"IntegrityError", "DuplicateEntryError"}:
                raise
            return jsonify({"error": "Application already exists"}), 409
        return jsonify({"application_id": cursor.lastrowid, "status": "applied"}), 201

    @app.get("/api/applications")
    @requires_auth
    @requires_role("student")
    def student_applications():
        rows = query_all(
            """SELECT a.application_id, a.status, a.applied_at, j.title, c.name AS company_name
               FROM applications a JOIN students s ON s.student_id = a.student_id
               JOIN job_postings j ON j.job_id = a.job_id JOIN companies c ON c.company_id = j.company_id
               WHERE s.user_id = ? ORDER BY a.applied_at DESC""",
            (g.current_user["user_id"],),
        )
        return jsonify([dict(row) for row in rows])

    @app.post("/api/recruiter/jobs")
    @requires_auth
    @requires_role("recruiter")
    def create_job():
        payload = request.get_json(silent=True) or {}
        required = ["title", "description", "application_deadline"]
        if any(not payload.get(field) for field in required):
            return jsonify({"error": "title, description, and application_deadline are required"}), 400
        recruiter = query_one("SELECT company_id FROM recruiters WHERE user_id = ?", (g.current_user["user_id"],))
        if not recruiter:
            return jsonify({"error": "Recruiter profile not found"}), 404
        db = get_db(app)
        cursor = db.execute(
            """INSERT INTO job_postings (company_id, title, description, location, package_lpa, minimum_cgpa, application_deadline)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (recruiter["company_id"], payload["title"], payload["description"], payload.get("location"),
             payload.get("package_lpa"), payload.get("minimum_cgpa", 0), payload["application_deadline"]),
        )
        db.commit()
        return jsonify({"job_id": cursor.lastrowid}), 201

    @app.patch("/api/recruiter/applications/<int:application_id>")
    @requires_auth
    @requires_role("recruiter")
    def update_application(application_id):
        status = (request.get_json(silent=True) or {}).get("status")
        if status not in {"shortlisted", "rejected", "hired"}:
            return jsonify({"error": "status must be shortlisted, rejected, or hired"}), 400
        recruiter = query_one("SELECT company_id FROM recruiters WHERE user_id = ?", (g.current_user["user_id"],))
        db = get_db(app)
        result = db.execute(
            """UPDATE applications SET status = ? WHERE application_id = ? AND job_id IN
               (SELECT job_id FROM job_postings WHERE company_id = ?)""",
            (status, application_id, recruiter["company_id"]),
        )
        db.commit()
        if result.rowcount == 0:
            return jsonify({"error": "Application not found"}), 404
        return jsonify({"application_id": application_id, "status": status})

    @app.get("/api/admin/stats")
    @requires_auth
    @requires_role("admin")
    def stats():
        result = query_one(
            """SELECT (SELECT COUNT(*) FROM users) AS users, (SELECT COUNT(*) FROM job_postings) AS jobs,
                      (SELECT COUNT(*) FROM applications) AS applications, (SELECT COUNT(*) FROM placements) AS placements"""
        )
        return jsonify(dict(result))

    @app.get("/api/cims/verify/<roll_number>")
    @requires_auth
    def verify_cims(roll_number):
        student = query_one("SELECT roll_number, full_name, department FROM students WHERE roll_number = ?", (roll_number,))
        return jsonify({"verified": bool(student), "record": dict(student) if student else None})

    return app


def get_db(app):
    if "db" not in g:
        import mysql.connector

        connection = mysql.connector.connect(
            host=app.config["MYSQL_HOST"],
            port=app.config["MYSQL_PORT"],
            database=app.config["MYSQL_DATABASE"],
            user=app.config["MYSQL_USER"],
            password=app.config["MYSQL_PASSWORD"],
        )
        g.db = MySQLDatabase(connection)
    return g.db


class MySQLDatabase:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql, params=()):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(sql.replace("?", "%s"), params)
        return cursor

    def executemany(self, sql, params):
        cursor = self.connection.cursor(dictionary=True)
        cursor.executemany(sql.replace("?", "%s"), params)
        return cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def initialize_database(app, db):
    schema_path = Path(__file__).resolve().parents[1] / "database" / "schema.sql"
    statements = schema_path.read_text(encoding="utf-8").split(";")
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.upper().startswith(("CREATE DATABASE", "USE ")):
            db.execute(statement)
    db.commit()


def query_one(sql, params=()):
    return get_db(current_app()).execute(sql, params).fetchone()


def query_all(sql, params=()):
    return get_db(current_app()).execute(sql, params).fetchall()


def current_app():
    from flask import current_app as flask_current_app
    return flask_current_app


def seed_demo_data(db):
    if db.execute("SELECT COUNT(*) AS user_count FROM users").fetchone()["user_count"]:
        return
    db.executemany("INSERT INTO roles (role_id, name) VALUES (?, ?)", [(1, "admin"), (2, "student"), (3, "recruiter")])
    users = [
        (1, "admin@example.com", "admin123", "Placement Admin"),
        (2, "student@example.com", "student123", "Aarav Sharma"),
        (3, "recruiter@example.com", "recruiter123", "Maya Rao"),
    ]
    for role_id, email, password, name in users:
        db.execute("INSERT INTO users (role_id, email, password_hash, full_name) VALUES (?, ?, ?, ?)", (role_id, email, generate_password_hash(password), name))
    db.execute("INSERT INTO students (user_id, roll_number, department, cgpa, graduation_year) VALUES (2, '221100', 'Computer Science', 8.7, 2026)")
    db.execute("INSERT INTO companies (name, industry, website) VALUES ('Acme Technologies', 'Software', 'https://example.com')")
    db.execute("INSERT INTO recruiters (user_id, company_id) VALUES (3, 1)")
    db.execute("""INSERT INTO job_postings (company_id, title, description, location, package_lpa, minimum_cgpa, application_deadline)
                  VALUES (1, 'Software Engineer', 'Build reliable services for placement teams.', 'Bengaluru', 18.5, 7.5, '2030-12-31')""")


def public_user(user):
    return {"user_id": user["user_id"], "email": user["email"], "full_name": user["full_name"], "role": user["role"]}


def requires_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Bearer token required"}), 401
        try:
            payload = jwt.decode(header[7:], current_app().config["SECRET_KEY"], algorithms=["HS256"])
            user = query_one(
                "SELECT u.user_id, u.email, u.full_name, r.name AS role FROM users u JOIN roles r ON r.role_id = u.role_id WHERE u.user_id = ?",
                (int(payload["sub"]),),
            )
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({"error": "Invalid or expired token"}), 401
        if not user:
            return jsonify({"error": "User not found"}), 401
        g.current_user = public_user(user)
        return view(*args, **kwargs)
    return wrapped


def requires_role(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if g.current_user["role"] != role:
                return jsonify({"error": f"{role} role required"}), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)