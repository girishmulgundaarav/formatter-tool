# 🧹 Formatter Tool

A powerful Streamlit app for formatting, validating, and converting structured text formats like JSON, XML, YAML, CSV, and more. Includes a tree viewer, diff comparison, and multi-format conversion utilities.

## ✨ Features

- Format and pretty-print: JSON, XML, YAML, CSV, TOML, INI, Markdown, HTML, SQL, Python
- Validate: JSON Schema, XML XSD, YAML linting
- Tree Viewer for structured formats
- Diff Viewer: compare original vs modified content
- Convert between JSON ↔ XML
- Download formatted output

## 🚀 Live App

Try it on [Streamlit Cloud](https://neatify-tool.streamlit.app)  
*(Replace with your actual app URL after deployment)*

## 🛠️ Tech Stack

•  Python
•  Streamlit
•  xmltodict
•  jsonschema
•  PyYAML

## 📁 Project Structure

formatter-tool/
├── app.py                # Main Streamlit app
├── formatter.py          # Formatting and validation functions
├── tree_viewer.py        # Tree viewer utilities
├── requirements.txt      # Dependencies
├── .streamlit/
│   └── config.toml       # Theme configuration
└── .gitignore

## 👨‍💻 Author

Built by Girish  
Feel free to fork, star ⭐, or contribute!

## 📄 License
This project is licensed under the MIT License.


## 📦 Installation

```bash
git clone https://github.com/your-username/formatter-tool.git
cd formatter-tool
pip install -r requirements.txt
streamlit run app.py

