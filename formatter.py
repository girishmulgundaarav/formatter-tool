import json
import xml.dom.minidom
import yaml
import csv
import io

# --- Optional imports with safe fallbacks ---
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # fallback for <3.11

try:
    import tomli_w
except ImportError:
    tomli_w = None

import configparser
from bs4 import BeautifulSoup

# SQL formatter (optional)
try:
    import sqlparse
except ImportError:
    sqlparse = None

# Python formatter (optional)
try:
    import autopep8
except ImportError:
    autopep8 = None


# ------------------ Core Formatters ------------------

def format_json(text: str) -> str:
    """Format JSON string with indentation."""
    parsed = json.loads(text)
    return json.dumps(parsed, indent=4, ensure_ascii=False)


def format_xml(text: str) -> str:
    """Format XML string with indentation."""
    dom = xml.dom.minidom.parseString(text)
    return dom.toprettyxml(indent="    ")


def format_yaml(text: str) -> str:
    """Format YAML string with indentation."""
    parsed = yaml.safe_load(text)
    return yaml.dump(parsed, sort_keys=False, indent=4)


def format_csv(text: str) -> str:
    """Format CSV string with consistent spacing."""
    reader = csv.reader(io.StringIO(text))
    output = io.StringIO()
    writer = csv.writer(output)
    for row in reader:
        writer.writerow(row)
    return output.getvalue()


# ------------------ Config Formats ------------------

def format_toml(text: str) -> str:
    """Format TOML string with indentation."""
    data = tomllib.loads(text)
    if tomli_w:
        return tomli_w.dumps(data)
    else:
        # fallback: pretty JSON representation
        return json.dumps(data, indent=4)


def format_ini(text: str) -> str:
    """Format INI/CFG string with normalized sections."""
    cp = configparser.ConfigParser()
    cp.read_string(text)
    buf = io.StringIO()
    cp.write(buf)
    return buf.getvalue()


# ------------------ Docs / Markup ------------------

def format_markdown(text: str) -> str:
    """Normalize Markdown headings and spacing."""
    lines = text.splitlines()
    normalized = []
    for i, line in enumerate(lines):
        l = line.rstrip()
        if l.startswith("#") and (i == 0 or lines[i-1].strip() != ""):
            normalized.append("")  # ensure blank line before heading
        normalized.append(l)
    return "\n".join(normalized)


def format_html(text: str) -> str:
    """Prettify HTML using BeautifulSoup."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.prettify()


# ------------------ Developer Formats ------------------

def format_sql(text: str) -> str:
    """Beautify SQL queries."""
    if sqlparse:
        return sqlparse.format(text, reindent=True, keyword_case="upper")
    else:
        # fallback: naive keyword uppercasing
        keywords = ["select", "from", "where", "join", "insert", "update", "delete"]
        formatted = text
        for kw in keywords:
            formatted = formatted.replace(kw, kw.upper())
        return formatted


def format_python(text: str) -> str:
    """Format Python code using autopep8 if available."""
    if autopep8:
        return autopep8.fix_code(text)
    else:
        # fallback: just dedent
        import textwrap
        return textwrap.dedent(text)

# ------------------ Validation Tools ------------------

import jsonschema
import xmlschema
import yamllint.config
import yamllint.linter

def validate_json_schema(instance_text: str, schema_text: str) -> str:
    """Validate JSON against a schema."""
    instance = json.loads(instance_text)
    schema = json.loads(schema_text)
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return "✅ JSON is valid against schema."
    except jsonschema.ValidationError as e:
        return f"❌ JSON validation error: {e.message}"

def validate_xml_xsd(xml_text: str, xsd_text: str) -> str:
    """Validate XML against XSD schema."""
    schema = xmlschema.XMLSchema(xsd_text)
    try:
        schema.validate(xml_text)
        return "✅ XML is valid against XSD."
    except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
        return f"❌ XML validation error: {e}"

def lint_yaml(text: str) -> str:
    """Run yamllint checks on YAML content."""
    conf = yamllint.config.YamlLintConfig('extends: default')
    problems = list(yamllint.linter.run(text, conf))
    if not problems:
        return "✅ YAML passed lint checks."
    return "\n".join([f"{p.line}:{p.column} {p.desc}" for p in problems])