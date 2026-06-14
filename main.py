import asyncio
import argparse
from tcp_checker import load_servers_from_json, write_report, check_all_servers_async, get_failed_results

def main():
    # Configure cmd arguments
    parser = argparse.ArgumentParser(description="Async TCP Checker")
    parser.add_argument("--servers",default="servers.json" ,help="Route of the JSON file")
    parser.add_argument("--out", default="reports", help="Folder to store report results CSV")
    args = parser.parse_args()
    
    # Load servers from JSON
    
    print(f"Loading servers from {args.servers}....")
    servers = load_servers_from_json(args.servers)
    
    # Execute TCP Checks in parallel
    print("Executing TCP async checks...\n")
    results = asyncio.run(check_all_servers_async(servers))
    
    # Save reports (JSON, CSV, LOG)
    print("\nSaving reports...")
    failed = get_failed_results(results)
    paths = write_report(failed, args.out)
    
    # Show generated Routes
    print("\nGenerated reports")
    for k, v in paths.items():
        print(f"  {k}: {v}")
        
if __name__ == "__main__":
    main()   
    