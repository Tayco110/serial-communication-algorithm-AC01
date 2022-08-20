import subprocess
r = subprocess.run(['echo', 'hello timeout'], timeout=5)
print(
    f'''type(r)={type(r)}, 
    r.args={r.args}, 
    r.returncode={r.returncode}, 
    r.stdout={r.stdout}, 
    r.stderr={r.stderr}'''
)
try:
    r = subprocess.run(['ping', 'www.google.com'], timeout=5)
except subprocess.TimeoutExpired as e:
    print(e)