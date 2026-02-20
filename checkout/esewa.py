import hashlib
import hmac
import base64

class eSewa:
    def __init__(self):
        self.product_code = "EPAYTEST"
        self.secret_key = "8gBm/:&EnhH.1/q",

    def generate_signature(self, total_amount, transaction_uuid):
        # Construct the message string exactly as required by eSewa v2
        # total_amount must match the form value exactly
        message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={self.product_code}"
        
        key = self.secret_key.encode('utf-8')
        message_bytes = message.encode('utf-8')
        
        # HMAC SHA256
        hmac_sha256 = hmac.new(key, message_bytes, hashlib.sha256).digest()
        
        # Base64 Encode
        signature = base64.b64encode(hmac_sha256).decode('utf-8')
        return signature