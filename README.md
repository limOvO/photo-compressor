# Image Compressor Web Application

This project is a web-based image compression tool that allows users to upload images and compress them to a specified size. The application is built using Flask and provides a user-friendly interface for image compression.

## Features

- Upload single or multiple images for compression.
- Specify target size for compressed images.
- View results and download compressed images.

## Project Structure

```
image-compressor-web
├── src
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── main.js
│   ├── templates
│   │   ├── base.html
│   │   └── index.html
│   ├── app.py
│   └── compressor.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd image-compressor-web
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python src/app.py
   ```

4. **Access the web interface:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- On the main page, you can upload images by selecting files from your computer.
- Specify the target size for the compressed images.
- Click the "Compress" button to start the compression process.
- Once completed, you will be able to download the compressed images.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.