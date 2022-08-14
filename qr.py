import qrcode


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=0
)

qr.add_data('EdgeWave')

qr.make()
img = qr.make_image()

img.show()