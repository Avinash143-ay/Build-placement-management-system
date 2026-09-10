# API and Demo Guide

## Start The Application

```powershell
python run.py
```

The server runs at `http://127.0.0.1:5000`.

## Health Check

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
```

Expected response:

```json
{"service":"placement-api","status":"ok"}
```

## Login And Student Application

```powershell
$login = Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5000/api/auth/login `
  -ContentType "application/json" `
  -Body '{"email":"student@example.com","password":"student123"}'
$token = $login.token
$headers = @{ Authorization = "Bearer $token" }

Invoke-RestMethod -Method Get -Uri http://127.0.0.1:5000/api/jobs

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5000/api/jobs/1/applications `
  -Headers $headers
```

The first application returns HTTP 201. Repeating it returns HTTP 409 because the
same student cannot apply twice to the same job.

## Test Role Protection

```powershell
Invoke-RestMethod -Method Get `
  -Uri http://127.0.0.1:5000/api/admin/stats `
  -Headers $headers
```

The student token receives HTTP 403. This proves RBAC is active.

## Automated Verification

```powershell
pytest -q
python -m compileall -q placement_system database
```

## MySQL Verification

Set `PLACEMENT_DB_DRIVER=mysql` and the `MYSQL_*` variables from
[.env.example](../.env.example), load [schema.sql](../database/schema.sql) and
[seed.sql](../database/seed.sql), then run `python run.py` again.