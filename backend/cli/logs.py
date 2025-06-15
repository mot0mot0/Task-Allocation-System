import argparse
from pathlib import Path
from datetime import datetime, timedelta


def get_log_file(log_type: str) -> Path:
    log_dir = Path(__file__).parent.parent / "logs"
    log_files = {
        "backend": "backend.log",
        "llm": "llm.log",
        "pocketbase": "pocketbase.log",
        "startup": "startup.log",
        "allocator": "allocator.log",
        "matching": "matching.log",
        "all": "all"  # Специальный тип для просмотра всех логов
    }

    if log_type not in log_files:
        raise ValueError(
            f"Unknown log type: {log_type}. Available types: {', '.join(log_files.keys())}"
        )

    if log_type == "all":
        return log_dir
    return log_dir / log_files[log_type]


def view_logs(args):
    try:
        log_path = get_log_file(args.type)
    except ValueError as e:
        print(e)
        return

    if args.type == "all":
        # Просмотр всех логов
        log_files = list(log_path.glob("*.log"))
        if not log_files:
            print("No log files found")
            return

        for log_file in sorted(log_files):
            print(f"\n=== {log_file.name} ===")
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    if args.tail:
                        lines = f.readlines()
                        for line in lines[-args.tail:]:
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
                print(f"Error reading {log_file.name}: {e}")
    else:
        # Просмотр конкретного лога
        if not log_path.exists():
            print(f"Log file {log_path} not found")
            return

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                if args.tail:
                    lines = f.readlines()
                    for line in lines[-args.tail:]:
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
    parser = argparse.ArgumentParser(description="View application logs")
    parser.add_argument(
        "--type",
        type=str,
        default="all",
        help="Type of logs to view (backend, llm, pocketbase, startup, allocator, matching, all)",
    )
    parser.add_argument("--tail", type=int, help="Show last N lines of log")
    parser.add_argument("--since", type=int, help="Show logs for the last N hours")

    args = parser.parse_args()
    view_logs(args)


if __name__ == "__main__":
    main()
