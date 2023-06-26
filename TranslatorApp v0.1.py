import sys, uuid, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the UI elements
        self.input_label = QLabel('Enter text to translate:')
        self.input_text = QLineEdit()
        self.output_label = QLabel('Translated text:')
        self.output_text = QLabel()
        self.translate_button = QPushButton('Translate')

        # Create the layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.input_label)
        hbox.addWidget(self.input_text)
        vbox.addLayout(hbox)
        vbox.addWidget(self.translate_button)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_text)
        self.setLayout(vbox)

        # Connect the button to the translation function
        self.translate_button.clicked.connect(self.translate_text)

        # Set the window properties
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Translator App')
        self.show()

    def translate_text(self):
        # Get the input text
        input_text = self.input_text.text()

        # Send the translation request
        key = "2ee57a45da3146faa3c8d9ea197fa71b"
        endpoint = "https://api.cognitive.microsofttranslator.com"
        location = "australiaeast"
        path = '/translate'
        constructed_url = endpoint + path
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': ['fr', 'es', 'it', 'de', 'ZH-Hant']
        }
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{
            'text': input_text
        }]
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()

        # Parse the response and update the output text
        translations = response.json()[0]['translations']
        output_text = ''
        for translation in translations:
            output_text += translation['text'] + '\n'
        self.output_text.setText(output_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    sys.exit(app.exec_())