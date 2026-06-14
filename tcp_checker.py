
import asyncio
import json
import os
import time
import csv
from models import CheckResult, Server
from pathlib import Path
from datetime import datetime, timezone
from typing import List


class ServerConfigError(Exception):
    pass


class MalformedServerJSONError(ServerConfigError):
    pass


async def check_server_async(server: Server) -> CheckResult:
    result = CheckResult(server)
    result.timestamp = datetime.now(timezone.utc).isoformat()

    max_attempts = 3
    timeout = 3
    backoff = 1

    for attempt in range(1, max_attempts + 1):
        result.attempts = attempt
        start_time = time.perf_counter()
        writer = None

        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(server.ip, server.port),
                timeout=timeout,
            )

            result.success = True
            result.latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            result.error_type = None
            result.error_message = None

            return result

        except asyncio.TimeoutError as error:
            result.success = False
            result.error_type = type(error).__name__
            result.error_message = f"Connection timed out after {timeout}s"

        except OSError as error:
            result.success = False
            result.error_type = type(error).__name__
            result.error_message = str(error)

        except Exception as error:
            result.success = False
            result.error_type = type(error).__name__
            result.error_message = str(error)

        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()

        if attempt < max_attempts:
            await asyncio.sleep(backoff)

    result.latency_ms = None
    return result

def load_servers_from_json(path: str) -> list[Server]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise MalformedServerJSONError(f"Invalid JSON file: {path}") from error

    if not isinstance(data, list):
        raise MalformedServerJSONError("Server JSON must contain a list of servers")

    servers = []

    for index, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise MalformedServerJSONError(f"Entry #{index} must be an object")

        required_fields = ["name", "ip", "port"]

        for field in required_fields:
            if field not in entry:
                raise MalformedServerJSONError(
                    f"Entry #{index} is missing required field: {field}"
                )

        server = Server(
            name=entry["name"],
            ip=entry["ip"],
            port=int(entry["port"]),
            service=entry.get("service"),
        )

        servers.append(server)

    return servers

def write_report(results: list[CheckResult], output_dir: str = "reports"):
    # If folder is not present, create it
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    
    # -------- Save JSON ------ #
    
    json_path = Path(output_dir) / "report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in results], f, indent=4, ensure_ascii=False)
        
    
    # -------- Save on CSV ------ #
    
    csv_path = Path(output_dir) / "report.csv"
    
    # Opening CSV file with Write privileges , Newline avoids blank spaces
    with open(csv_path,"w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # -------- Create Header Rows ------ #
        # Creating a CSV writer associated to json loaded file.
        # This creates rows with headers
        
        writer.writerow([
            "name", 
            "ip", 
            "port", 
            "service",
            "success", 
            "latency_ms", 
            "attempts",
            "error_type", 
            "error_message",
            "timestamp", 
            "source_host"
        ])
    
    # Writing a row per result
        for r in results:
            s = r.server # Shortcut to currently associated server object
            writer.writerow([
                s.name, 
                s.ip, 
                s.port, 
                s.service,
                r.success, 
                r.latency_ms, 
                r.attempts,
                r.error_type, 
                r.error_message,
                r.timestamp, 
                r.source_host
            ])
    # -------- Save LOGS as text ------ #
    
    log_path = Path(output_dir) / "report.log"
    
    # Opening report log to write a formatted log
    with open(log_path, "w", encoding="utf-8") as f:
        for r in results:
            s = r.server
            if r.success:
                # If Server is up
                f.write(f"[OK] {s.name} ({s.ip}:{s.port}) - {r.latency_ms} ms\n")
            else:
                f.write(
                # If Server is down
                    f"[FAIL] {s.name} ({s.ip}:{s.port}) - "
                    f"{r.error_type}: {r.error_message}\n"
                )
    # Returning routes of the generated files    
    return {
        "json": str(json_path),
        "csv" : str(csv_path),
        "log" : str(log_path),
    }

# ANSI Console Color Code
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

async def check_all_servers_async(servers: List[Server]) -> List[CheckResult]:
    """
    Executes parallel TCP checks using asyncio.
    Receives a list of Server objects and returns a list of CheckResult.
    """
    tasks = []
    
    # Create Asyncio tasks , this prepares execution
    for server in servers:
        print(f"Creating check for {server.name} ({server.ip}:{server.port})")
        tasks.append(check_server_async(server))
        
    # Executes now tasks in parallel, .Gather awaits for tasks to be done
    results = await asyncio.gather(*tasks)

    # Summary on console.
    
    print("\n=== RESULTS ===")
    for r in results:
        s = r.server
        if r.success:
            print(f"{GREEN}[OK]{RESET}   {s.name} ({s.ip}:{s.port}) - {r.latency_ms} ms")
        else:
            print(
                f"{RED}[FAIL]{RESET} {s.name} ({s.ip}:{s.port}) - "
                f"{YELLOW}{r.error_type}{RESET}: {r.error_message}"
            )
    return results

def get_failed_results(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if not r.success]

