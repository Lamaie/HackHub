import subprocess
import sys
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run-tool', methods=['POST'])
def run_tool():
  tool = request.form['tool']
  adapter = request.form['adapter']
  output = subprocess.run([tool, '-i', adapter], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return output.stdout

@app.route('/execute-command', methods=['POST'])
def execute_command():
  command = request.form['command']
  output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return output.stdout

@app.route('/technical-info')
def technical_info():
  usage = subprocess.run('df', stdout=subprocess.PIPE).stdout.decode()
  ip_address = subprocess.run('hostname -I', shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
  network = subprocess.run('ip route', shell=True, stdout=subprocess.PIPE).stdout.decode()
  return jsonify({
    'usage': usage,
    'ip_address': ip_address,
    'network': network
  })

@app.route('/adapters')
def adapters():
  adapters = subprocess.run('ip link', shell=True, stdout=subprocess.PIPE).stdout.decode().split('\n')
  available_adapters = []
  for adapter in adapters:
    if ': ' in adapter:
      name = adapter.split(': ')[1]
      if 'LOOPBACK' not in adapter:
        available_adapters.append(name)
  return jsonify(available_adapters)

@app.route('/terminal-output')
def terminal_output():
  output = subprocess.run('tail -n 1000 /var/log/syslog', shell=True, stdout=subprocess.PIPE).stdout.decode()
  return output

def check_dependencies(verbose):
  dependencies = ['apache2', 'python3', 'python3-pip']
  missing = []
  for dependency in dependencies:
    try:
      subprocess.run(['which', dependency], check=True)
      if verbose:
        print(f'\033[32m{dependency} is installed\033[0m')
    except subprocess.CalledProcessError:
      missing.append(dependency)
  if missing:
    print(f'\033[31mError: The following dependencies are missing: {", ".join(missing)}\033[0m')
    print('Please install them and run the script again')
    sys.exit(1)

def download_requirements(verbose):
  if verbose:
    print('\033[36mDownloading requirements...\033[0m')
  try:
    subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], check=True)
  except subprocess.CalledProcessError:
    print('\033[31mError: Could not download requirements\033[0m')
    sys.exit(1)
  if verbose:
    print('\033[32mRequirements downloaded successfully\033[0m')

def run_server(verbose):
  if verbose:
    print('\033[36mStarting web server...\033[0m')
  try:
    subprocess.run(['service', 'apache2', 'start'], check=True)
  except subprocess.CalledProcessError:
    print('\033[31mError: Could not start web server\033[0m')
    sys.exit(1)
  if verbose:
    print('\033[32mWeb server started successfully\033[0m')

def serve_frontend(verbose):
  if verbose:
    print('\033[36mServing frontend...\033[0m')
  os.chdir('frontend')
  try:
    subprocess.run(['python3', '-m', 'http.server', '5000'], check=True)
  except subprocess.CalledProcessError:
    print('\033[31mError: Could not serve frontend\033[0m')
    sys.exit(1)
  if verbose:
    print('\033[32mFrontend served successfully\033[0m')

def main():
  verbose = '--verbose' in sys.argv
  print('\033[36mPreparing to run HackHub...\033[0m')
  check_dependencies(verbose)
  download_requirements(verbose)
  run_server(verbose)
  serve_frontend(verbose)
  print('\033[32mHackHub is now running!\033[0m')
  print('\033[32mYou can access it at http://localhost:5000/\033[0m')
  print('\033[33mYou can close this terminal and HackHub will continue running in the background\033[0m')

if __name__ == '__main__':
  main()

