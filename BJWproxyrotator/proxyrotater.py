import subprocess
import time

def parse_proxy_list(filepath):
    with open(filepath, 'r') as f:
        long_string = f.read()
    return long_string.split()

proxy_list = parse_proxy_list('/Users/blakeweiss/Desktop/proxyrotator copy/proxylist.txt')

def rotate_proxy():
    current_proxy_output = subprocess.check_output(["networksetup", "-getsocksfirewallproxy", "Wi-Fi"]).decode()

    # This checks for the 'Enabled: No' condition more accurately
    if 'Enabled: No' in current_proxy_output:
        current_index = -1
    else:
        try:
            current_proxy = current_proxy_output.split('Server: ')[1].split('\n')[0]
            current_port = current_proxy_output.split('Port: ')[1].split('\n')[0].split(' ')[0] # Ensure we're only getting the port number
            current_proxy_with_port = f"{current_proxy}:{current_port}"
            current_index = proxy_list.index(current_proxy_with_port)
        except (ValueError, IndexError):
            current_index = -1
    
    next_index = (current_index + 1) % len(proxy_list)
    return proxy_list[next_index]

def set_proxy(proxy_with_port):
    proxy, port = proxy_with_port.split(':')
    # Corrected to use -setsocksfirewallproxy for setting the proxy
    subprocess.call(["networksetup", "-setsocksfirewallproxy", "Wi-Fi", proxy, port])
    print(f"Proxy set to: {proxy_with_port}")

while True:
    next_proxy = rotate_proxy()
    set_proxy(next_proxy)
    time.sleep(300)  # Adjust back to 300 seconds (5 minutes) for actual use
