import argparse
from pathlib import Path
from datetime import datetime, timedelta


def view_logs(args):
    log_file = Path(__file__).parent.parent / "logs" / "llm.log"

    if not log_file.exists():
        print("Logs file not found")
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            if args.tail:
                lines = f.readlines()
                for line in lines[-args.tail :]:
                    print(line.strip())
            elif args.since:
                since_time = datetime.now() - timedelta(hours=args.since)
                for line in f:
                    try:
                        log_time = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                        if log_time >= since_time:
                            print(line.strip())
                    except ValueError:
                        continue
            else:
                print(f.read())
    except Exception as e:
        print(f"Error reading logs: {e}")


def main():
    parser = argparse.ArgumentParser(description="View LLM interface logs")
    parser.add_argument("--tail", type=int, help="Show last N lines of log")
    parser.add_argument("--since", type=int, help="Show logs for the last N hours")

    args = parser.parse_args()
    view_logs(args)


if __name__ == "__main__":
    main()
