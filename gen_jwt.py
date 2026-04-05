import time
import jwt
import os
import sys

def generate_token():
    try:
        # Pull inputs from environment variables
        key_id = os.environ.get("KEY_ID")
        issuer_id = os.environ.get("ISSUER_ID")
        private_key = os.environ.get("PRIVATE_KEY")

        if not all([key_id, issuer_id, private_key]):
            raise ValueError("Missing required environment variables for JWT generation.")

        # Apple JWT Header and Payload
        header = {
            "kid": key_id,
            "typ": "JWT",
            "alg": "ES256"
        }

        payload = {
            "iss": issuer_id,
            "exp": int(time.time()) + 1000, # 10-minute expiry
            "aud": "appstoreconnect-v1"
        }

        # Sign and encode
        token = jwt.encode(
            payload, 
            private_key, 
            algorithm="ES256", 
            headers=header
        )
        return token

    except Exception as e:
        sys.stderr.write(f"JWT Generation Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    print(generate_token())