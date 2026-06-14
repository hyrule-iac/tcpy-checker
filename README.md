# TCP Checker – Async TCP Monitoring Tool

**TCP Checker** is a lightweight, asynchronous TCP monitoring utility built in Python.  
It performs concurrent TCP connection tests, generates structured reports, and integrates cleanly into DevOps, SRE, and observability workflows.  
The project is fully container‑ready and supports automated execution through scheduled pipelines.

---

# Features

- **Asynchronous TCP checks** using `asyncio`
- **Structured reporting** in JSON, CSV, and LOG formats
- **Detailed error classification** (timeout, refused, unreachable)
- **Dataclass‑based models** for clean, typed structures
- **Pure function** for filtering failed checks
- **Simple CLI interface**
- **Docker‑ready** for containerized execution
- **DevSecOps‑friendly** (linting, static analysis, dependency audit, tests)
- **Supports scheduled execution** (e.g., hourly GitHub Actions cron)

---

## Installation

 
  - Docker (optional)
  
  ### Install dependencies
  
  ```bash
  pip install -r requirements.txt
  ```
  
  ---
# Usage
  
    ### Run the checker
    
    ```bash
    python main.py --servers servers.json --out reports
    ```

### CLI Parameters

  | Flag | Description |
  |------|-------------|
  | `--servers` | Path to the JSON file containing server definitions |
  | `--out` | Output directory for generated reports |

---

## Example `servers.json`

  ```json
  [
    {
      "name": "Google DNS",
      "ip": "8.8.8.8",
      "port": 53
    },
    {
      "name": "Cloudflare DNS",
      "ip": "1.1.1.1",
      "port": 53
    }
  ]
  ```
  
  ---

## Project Structure

  ```
  .
  ├── main.py
  ├── tcp_checker.py
  ├── models.py
  ├── servers.json
  ├── reports/
  └── requirements.txt
  ```
  
  ---

## Docker Usage

    ### Build the image
    
    ```bash
    docker build -t tcp-checker .
    ```
    
    ### Run the checker inside Docker
    
    ```bash
    docker run --rm -v "%cd%\reports:/app/reports" tcp-checker
    ```
    
    (Use the Linux equivalent if running on Linux.)
    
    ---
    # DevSecOps Pipeline (Recommended)
    
    This project supports a full DevSecOps workflow including:
    
    - **flake8** (linting)
    - **bandit** (static security analysis)
    - **pip-audit** (dependency vulnerability scanning)
    - **pytest** (unit tests)
    - **Docker build & push**
    - **Scheduled hourly execution** via GitHub Actions

# License
  MIT License (or whatever you choose).

