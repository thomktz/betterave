import os
import socket

# Get the local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        # Default to localhost IP if any error occurs
        return "127.0.0.1"

# Generate .env contents
def generate_back_env_contents(ip_address):
    return f"LOCAL_IP={ip_address}\n"

def generate_front_env_contents(ip_address):
    return f"VUE_APP_BACKEND_URL=http://{ip_address}:5000\n"

if __name__ == "__main__":
    ip_address = get_local_ip()

    # Write .env to backend
    with open(os.path.join("backend", ".env"), "w") as backend_env:
        backend_env.write(generate_back_env_contents(ip_address))
    
    # Write .env to frontend (you can add more variables specific to frontend if required)
    with open(os.path.join("frontend", ".env"), "w") as frontend_env:
        frontend_env.write(generate_front_env_contents(ip_address))
    
    print(f".env files generated with IP address: {ip_address}")
