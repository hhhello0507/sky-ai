import serial


class SkyArduino:
    def __init__(self):
        self.sky_serial = self._get_serial()

    def _get_serial(self):
        return serial.Serial(port="COM3",
                             baudrate=9600)

    def send_classification_result(self, index: int):
        encoded_data = str(index).encode()
        self.sky_serial.write(encoded_data)
