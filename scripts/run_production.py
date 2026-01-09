#!/usr/bin/env python3
"""
Production startup script using Gunicorn for optimal performance
"""
import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Start TikTok Scraper in production mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5001, help='Port to bind to (default: 5001)')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker processes (default: 4)')
    parser.add_argument('--threads', type=int, default=2, help='Number of threads per worker (default: 2)')
    parser.add_argument('--timeout', type=int, default=120, help='Worker timeout in seconds (default: 120)')
    parser.add_argument('--max-cpu', type=int, default=80, help='Maximum CPU usage percentage (default: 80)')
    
    args = parser.parse_args()
    
    print("🚀 Starting TikTok Scraper in PRODUCTION mode with Gunicorn")
    print(f"📡 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"👥 Workers: {args.workers}")
    print(f"🧵 Threads per worker: {args.threads}")
    print(f"⏱️  Timeout: {args.timeout}s")
    print(f"🖥️  Max CPU: {args.max_cpu}%")
    print("-" * 60)
    
    # Gunicorn command with optimized settings
    cmd = [
        'gunicorn',
        '--bind', f'{args.host}:{args.port}',
        '--workers', str(args.workers),
        '--threads', str(args.threads),
        '--timeout', str(args.timeout),
        '--worker-class', 'gthread',  # Use threaded workers
        '--worker-connections', '1000',
        '--max-requests', '1000',  # Restart workers after 1000 requests
        '--max-requests-jitter', '100',  # Add jitter to prevent thundering herd
        '--preload-app',  # Load app before forking workers
        '--access-logfile', '-',  # Log to stdout
        '--error-logfile', '-',   # Log errors to stdout
        '--log-level', 'info',
        '--capture-output',  # Capture stdout/stderr
        'src.app:app'  # Import app from src.app
    ]
    
    try:
        # Start Gunicorn
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gracefully...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Gunicorn failed to start: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Gunicorn not found. Install with: pip install gunicorn")
        sys.exit(1)

if __name__ == '__main__':
    main()
