#!/usr/bin/env python3
"""
FIND-RLB Startup Manager
Orchestrates starting all system services for development/testing
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import List, Dict
import psutil
import sys

class StartupManager:
    """Manages starting all FIND-RLB services"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent
        self.processes = {}
        self.services = [
            {
                'name': 'Database',
                'command': None,
                'cwd': self.root_dir / 'backend',
                'ready_signal': 'sqlite3 loaded',
                'optional': True
            },
            {
                'name': 'Backend API',
                'command': [sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'],
                'cwd': self.root_dir / 'backend',
                'ready_signal': 'Quit the server with',
                'optional': False,
                'port': 8000
            },
            {
                'name': 'Frontend Dev Server',
                'command': ['npm', 'run', 'dev'],
                'cwd': self.root_dir / 'frontend',
                'ready_signal': 'Ready in',
                'optional': True,
                'port': 3000
            },
        ]
    
    def log(self, service: str, message: str):
        """Log service messages"""
        print(f"[{service:20s}] {message}")
    
    def check_port_available(self, port: int) -> bool:
        """Check if port is available"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return False
            return True
        except:
            return True
    
    def start_service(self, service: Dict) -> bool:
        """Start a single service"""
        name = service['name']
        self.log(name, f"Starting {name}...")
        
        if service.get('port') and not self.check_port_available(service['port']):
            self.log(name, f"ERROR: Port {service['port']} is already in use")
            return False
        
        if service['command'] is None:
            self.log(name, "Skipped (no command configured)")
            return True
        
        try:
            process = subprocess.Popen(
                service['command'],
                cwd=service['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            self.processes[name] = process
            self.log(name, f"Started (PID: {process.pid})")
            return True
        except Exception as e:
            self.log(name, f"ERROR: {str(e)}")
            return False
    
    def start_all_services(self):
        """Start all services"""
        print("="*60)
        print("FIND-RLB STARTUP MANAGER")
        print("="*60 + "\n")
        
        for service in self.services:
            if not self.start_service(service):
                if not service['optional']:
                    print("\n[ERROR] Critical service failed to start")
                    self.stop_all_services()
                    return False
            time.sleep(1)
        
        print("\n" + "="*60)
        print("ALL SERVICES STARTED SUCCESSFULLY")
        print("="*60)
        print("\nAccess points:")
        print("  Frontend:      http://localhost:3000")
        print("  Backend API:   http://localhost:8000/api/")
        print("  Django Admin:  http://localhost:8000/admin/")
        print("\nPress Ctrl+C to stop all services")
        print("="*60 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
                # Check if any process has died
                for name, process in list(self.processes.items()):
                    if process.poll() is not None:
                        self.log(name, f"Process died with return code {process.returncode}")
        except KeyboardInterrupt:
            print("\n\nShutting down services...")
            self.stop_all_services()
    
    def stop_all_services(self):
        """Stop all running services"""
        for name, process in self.processes.items():
            if process.poll() is None:  # Still running
                self.log(name, "Stopping...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    self.log(name, "Stopped")
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.log(name, "Killed")

if __name__ == '__main__':
    manager = StartupManager()
    try:
        manager.start_all_services()
    except Exception as e:
        print(f"Fatal error: {e}")
        manager.stop_all_services()
