import qrcode

def generate_qr(table_id):
    qr_data = f"https://restaurant-chat.com/join/{table_id}"
    qr = qrcode.make(qr_data)
    qr.save(f"qr_codes/table_{table_id}.png")
