# 🧹 Neatify — Multi-Format Formatter

A professional-grade Streamlit app for formatting, previewing, validating, diffing, and converting structured text formats like JSON, XML, YAML, CSV, and more. Includes an expandable tree viewer, side-by-side diff, smart JSON diff, data previews, statistics, and a session history panel.

## ✨ Features

- Format and pretty-print: JSON, XML, YAML, CSV, TOML, INI, Markdown, HTML, SQL, Python
- Validate: JSON Schema, XML XSD, YAML linting
- Tree Viewer with expand/collapse for JSON/YAML and interactive XML tabs
- Diff Viewer: side-by-side colored highlights
- Smart Diff: semantic JSON differences (added/removed/changed keys)
- Data Preview: CSV/JSON table with statistics summary
- History Panel: restore past uploads and formatted outputs
- Convert between JSON ↔ XML
- Download formatted output
- Custom branding: logo and accent colors

## 🚀 Live App

Try it on [Streamlit Cloud](https://neatify-tool.streamlit.app)  
*(Replace with your actual app URL after deployment)*

## 🛠️ Tech Stack

• Python  
• Streamlit  
• pandas  
• xmltodict  
• jsonschema  
• PyYAML

## 📁 Project Structure

formatter-tool/
├── app.py                # Main Streamlit app (branding, previews, diff, history)
├── formatter.py          # Formatting and validation functions
├── tree_viewer.py        # Expand/collapse viewers and XML tabs
├── requirements.txt      # Dependencies
├── .streamlit/
│   └── config.toml       # Theme configuration (branding)
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