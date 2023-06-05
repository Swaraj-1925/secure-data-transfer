import webbrowser

def open_gateway_url(cid):
    gateway = ".ipfs.w3s.link"
    gateway_url = f"{cid}{gateway}"
    webbrowser.open(gateway_url)

# Example usage
cid =input("Enter cid: ")
open_gateway_url(cid)
