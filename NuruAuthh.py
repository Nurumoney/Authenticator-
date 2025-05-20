import pyotp
import qrcode
import os

# Configuration
SECRET_FILE = "secrets.txt"
BACKUP_CODES_FILE = "backup_codes.txt"

def generate_secret():
    "Generate a new base16 secret"
    return pyotp.random_base32()

def generate_qr_code(secret, username, issuer):
    "Generate a QR code for authenticator app setup"
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)
    qr = qrcode.QRCode()
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii() 
    img = qrcode.make(uri)
    img.save(f"{username}_qrcode.png")
    return uri

def verify_code(secret, user_code):
    "Verify if the user's code matches the generated code"
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code)

def save_secret(username, secret):
    "Store secret securely (for demonstration purposes only)"
    with open(SECRET_FILE, "a") as f:
        f.write(f"{username}:{secret}\n")

def main():
    print("TOTP Authenticator Demo")
    
    # User setup
    username = input("Enter username: ")
    issuer = "EllamsAuthApp"
    
    # Generate and save secret
    secret = generate_secret()
    save_secret(username, secret)
    
    # Generate QR code
    uri = generate_qr_code(secret, username, issuer)
    print(f"QR code generated: {username}_qrcode.png")
    

    # Verification demo
    print("\nTest authentication:")
    while True:
        user_code = input("Enter 6-digit code from authenticator app (or 'q' to quit): ")
        if user_code.lower() == 'q':
            break
        
        if verify_code(secret, user_code):
            print("✓ Valid code!")
        else:
            print("✗ Invalid code!")

if __name__ == "__main__":
    main()