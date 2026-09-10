USE placement_system;

INSERT INTO roles (name) VALUES ('admin'), ('student'), ('recruiter');

INSERT INTO users (role_id, email, password_hash, full_name) VALUES
    ((SELECT role_id FROM roles WHERE name = 'admin'), 'admin@example.com', 'scrypt:32768:8:1$k6AU886iZFjiue06$718be49255e84cc9801c6edff5795b3cd52caf211fa7417adcb0fffd4c953eafaf6e330031467d3e4f187a0f7a3ae3ed3c0c598eb8d27210c3f1f9b860152e9e', 'Placement Admin'),
    ((SELECT role_id FROM roles WHERE name = 'student'), 'student@example.com', 'scrypt:32768:8:1$6J4fpJgVp6LL76W4$4063f50dfcbaafd8ea8722e19d89de31161534b83f02163ecf9ae0f1beced2446423ac0be1688a1ef5ad7e3b479740fb5720f2a5e021f67825c508003a86ea45', 'Aarav Sharma'),
    ((SELECT role_id FROM roles WHERE name = 'recruiter'), 'recruiter@example.com', 'scrypt:32768:8:1$qalIxDCEwl095ooe$2fcaa52914c579be7b3381cb6d8e88989c1dc6a54668607f88d48d0e065d57b9a28adf66777dded1985e83100991398315c5fc7d4603b67a324c3c194987a5db', 'Maya Rao');

INSERT INTO students (user_id, roll_number, department, cgpa, graduation_year)
VALUES ((SELECT user_id FROM users WHERE email = 'student@example.com'), '221100', 'Computer Science', 8.70, 2026);

INSERT INTO companies (name, industry, website)
VALUES ('Acme Technologies', 'Software', 'https://example.com');

INSERT INTO recruiters (user_id, company_id)
VALUES (
    (SELECT user_id FROM users WHERE email = 'recruiter@example.com'),
    (SELECT company_id FROM companies WHERE name = 'Acme Technologies')
);

INSERT INTO job_postings
    (company_id, title, description, location, package_lpa, minimum_cgpa, application_deadline)
VALUES
    ((SELECT company_id FROM companies WHERE name = 'Acme Technologies'),
     'Software Engineer', 'Build reliable services for placement teams.', 'Bengaluru', 18.50, 7.50, '2030-12-31');