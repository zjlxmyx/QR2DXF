import qrcode


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=5,
    border=0
)

qr.add_data('123456789012345678901234567')

qr.make()
img = qr.make_image()

img.show()