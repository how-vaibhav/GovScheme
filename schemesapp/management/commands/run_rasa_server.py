"""
Django management command to run RASA actions server in background
"""
import os
import subprocess
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start RASA actions server in background'

    def handle(self, *args, **options):
        rasa_project_path = os.environ.get(
            'RASA_PROJECT_PATH',
            r'c:\Users\LENOVO\rasa_project'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Starting RASA server from {rasa_project_path}...'))
        
        try:
            # Start RASA actions server
            cmd = [sys.executable, '-m', 'rasa', 'run', 'actions', '--port', '5055']
            
            # Change to RASA project directory
            os.chdir(rasa_project_path)
            
            # Start in background
            if sys.platform == 'win32':
                # Windows
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            
            self.stdout.write(self.style.SUCCESS('✅ RASA server started on port 5055'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to start RASA server: {str(e)}'))
            sys.exit(1)
