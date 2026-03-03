import os
env_path = "/data/openclaw/keys/jupiter.env"
print("Exists:", os.path.exists(env_path))
print("Perms:", oct(os.stat(env_path).st_mode))
with open(env_path) as f:
    content = f.read()
print("Content:", repr(content))
key = None
for line in content.splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        k, v = line.split("=", 1)
        if k == "JUPITER_API_KEY":
            key = v
            break
print("Found key:", key)
