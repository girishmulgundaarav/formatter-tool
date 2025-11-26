import streamlit as st
import difflib
import json
import xmltodict
import pandas as pd
from formatter import (
    format_json, format_xml, format_yaml, format_csv,
    format_toml, format_ini, format_markdown, format_html,
    format_sql, format_python,
    validate_json_schema, validate_xml_xsd, lint_yaml
)
from tree_viewer import show_tree

# ---------------- Session state init ----------------
for key in ["raw_text_value", "diff_original", "diff_modified"]:
    if key not in st.session_state:
        st.session_state[key] = ""

def clear_text(key="raw_text_value"):
    st.session_state[key] = ""   # reset the bound key

def clear_on_section_change():
    for key in ["raw_text_value", "diff_original", "diff_modified"]:
        st.session_state[key] = ""

# ---------------- Page config ----------------
st.set_page_config(page_title="Multi-Format Formatter", layout="wide")

# ---------------- Sidebar branding ----------------
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("### Multi-Format Formatter")

# Sidebar: choose section
section = st.sidebar.radio(
    "Choose section:",
    ["Introduction", "Formatter", "Diff Viewer", "Multi-Format Conversion", "CSV Analysis"],
    key="section",
    on_change=clear_on_section_change
)

# ---------------- Introduction Section ----------------
if section == "Introduction":
    st.title("🧹 Multi-Format Formatter")
    st.subheader("Your all-in-one tool for formatting, validating, converting, and analyzing data")

    st.markdown("---")

    st.markdown(
        """
        Welcome to **Multi-Format Formatter** — a professional utility built with Streamlit to make your data clean, structured, and insightful.  

        ### ✨ Features
        - **Formatter**: Beautify JSON, XML, YAML, CSV, TOML, INI, Markdown, HTML, SQL, and Python code.
        - **Validation**: Validate JSON against schemas, XML with XSD, and lint YAML for correctness.
        - **Tree Viewer**: Explore structured formats interactively.
        - **Diff Viewer**: Compare original vs modified content side by side.
        - **Conversion**: Seamlessly convert JSON ↔ XML.
        - **CSV Analysis**: Upload CSVs for previews, summary statistics, column insights, and visualizations.
        - **Download Output**: Export your formatted or validated content instantly.

        ---
        ### 🚀 Get Started
        Use the sidebar to select a section and begin formatting, validating, or analyzing your data.
        """
    )

    if st.button("Start Now", type="primary", icon=":material/auto_fix_high:"):
        st.success("Choose a section from the sidebar to begin!")


# ---------------- Formatter Section ----------------
if section == "Formatter":
    fmt_type = st.sidebar.radio(
        "Choose format type:",
        ["JSON", "XML", "YAML", "CSV", "TOML", "INI", "Markdown", "HTML", "SQL", "Python"],
        key="fmt_type",
        on_change=clear_on_section_change
    )

    st.title(f"🧹 Formatter Tool — {fmt_type}")

    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["json","xml","yaml","yml","csv","txt","toml","ini","cfg","md","html","sql","py"]
    )
    if uploaded_file is not None:
        st.session_state.raw_text_value = uploaded_file.read().decode("utf-8")

    raw_text = st.text_area("Or paste your content here:", height=300, key="raw_text_value")

    btn_col1, btn_col2 = st.columns([1, 1])
    format_clicked = btn_col1.button("Format", type="primary", icon=":material/tune:")
    btn_col2.button("Clear", on_click=lambda: clear_text("raw_text_value"), type="primary", icon=":material/delete:")

    if format_clicked:
        text = st.session_state.raw_text_value.strip()
        if text == "":
            st.warning("Please provide content via upload or paste.")
        else:
            try:
                if fmt_type == "JSON":
                    formatted = format_json(text)
                elif fmt_type == "XML":
                    formatted = format_xml(text)
                elif fmt_type == "YAML":
                    formatted = format_yaml(text)
                elif fmt_type == "CSV":
                    formatted = format_csv(text)
                elif fmt_type == "TOML":
                    formatted = format_toml(text)
                elif fmt_type == "INI":
                    formatted = format_ini(text)
                elif fmt_type == "Markdown":
                    formatted = format_markdown(text)
                elif fmt_type == "HTML":
                    formatted = format_html(text)
                elif fmt_type == "SQL":
                    formatted = format_sql(text)
                elif fmt_type == "Python":
                    formatted = format_python(text)

                st.success(f"Formatted {fmt_type} successfully:")
                st.code(formatted, language=fmt_type.lower(), line_numbers=True)

                st.download_button(
                    label=f"Download formatted {fmt_type}",
                    data=formatted,
                    file_name=f"formatted.{fmt_type.lower()}",
                    mime="text/plain", icon=":material/file_download:",
                    type="primary"
                )

                if fmt_type in ["JSON", "XML", "YAML", "TOML", "INI"]:
                    st.subheader("🌳 Tree Viewer")
                    show_tree(text, fmt_type)

            except Exception as e:
                st.error(f"Error formatting {fmt_type}: {e}")

    # Validation tools
    st.markdown("---")
    st.subheader("🔍 Validation / Linting")
    if fmt_type == "JSON":
        schema_text = st.text_area("Paste JSON Schema (optional):", key="json_schema")
        if st.button("Validate JSON", type="primary", icon=":material/fact_check:"):
            if schema_text.strip():
                st.info(validate_json_schema(st.session_state.raw_text_value, schema_text))
            else:
                st.warning("Please provide a JSON Schema to validate against.")
    elif fmt_type == "XML":
        xsd_text = st.text_area("Paste XSD Schema (optional):", key="xml_xsd")
        if st.button("Validate XML", type="primary", icon=":material/fact_check:"):
            if xsd_text.strip():
                st.info(validate_xml_xsd(st.session_state.raw_text_value, xsd_text))
            else:
                st.warning("Please provide an XSD Schema to validate against.")
    elif fmt_type == "YAML":
        if st.button("Lint YAML", type="primary"):
            st.info(lint_yaml(st.session_state.raw_text_value))

# ---------------- Diff Viewer Section ----------------
elif section == "Diff Viewer":
    st.title("Diff Viewer (Side by Side)")

    # Initialize defaults
    if "diff_original" not in st.session_state:
        st.session_state.diff_original = "def hello():\n    print('Hello world')"
    if "diff_modified" not in st.session_state:
        st.session_state.diff_modified = "def hello():\n    print('Hello, Girish!')"

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.session_state.diff_original = st.text_area(
            " ", value=st.session_state.diff_original, height=300, key="diff_original_area"
        )
    with col2:
        st.subheader("Modified")
        st.session_state.diff_modified = st.text_area(
            " ", value=st.session_state.diff_modified, height=300, key="diff_modified_area"
        )

    if st.button("View Diff (Side by Side)", type="primary"):
        original_text = st.session_state.diff_original or ""
        modified_text = st.session_state.diff_modified or ""

        if not original_text.strip() or not modified_text.strip():
            st.warning("Please provide both original and modified content.")
        else:
            import difflib
            hd = difflib.HtmlDiff(wrapcolumn=80)
            html_table = hd.make_table(
                original_text.splitlines(),
                modified_text.splitlines(),
                fromdesc="Original",
                todesc="Modified",
                context=True,
                numlines=2
            )

            # Add CSS for GitHub-style coloring
            html = f"""
            <style>
              table.diff {{ font-family: Menlo, Monaco, Consolas, monospace; width: 100%; border-collapse: collapse; }}
              .diff_header {{ background: #f6f8fa; font-weight: bold; }}
              td, th {{ border: 1px solid #e1e4e8; padding: 6px 8px; vertical-align: top; }}
              .diff_next {{ background: #fffbe6; }}
              .diff_add {{ background: #e6ffed; }}     /* additions: green */
              .diff_sub {{ background: #ffeef0; }}     /* deletions: red */
              .diff_chg {{ background: #fff5b1; }}     /* changes: yellow */
            </style>
            {html_table}
            """
            st.components.v1.html(html, height=500, scrolling=True)

# ---------------- Multi-Format Conversion Section ----------------
elif section == "Multi-Format Conversion":
    st.title("🔄 Multi-Format Conversion (JSON ↔ XML ↔ TOML ↔ TOON)")
    uploaded_file = st.file_uploader("Upload JSON, XML, or TOML file", type=["json","xml","toml","txt"])
    if uploaded_file is not None:
        st.session_state.raw_text_value = uploaded_file.read().decode("utf-8")

    raw_text = st.text_area("Paste JSON, XML, or TOML:", height=400, key="raw_text_value")
    st.button("Clear", on_click=lambda: clear_text("raw_text_value"), type="primary", icon=":material/delete:")

    col1, col2, col3, col4 = st.columns([1,1,1,1])

    # JSON → XML
    if col1.button("Convert JSON → XML", type="primary", icon=":material/swap_horiz:"):
        try:
            obj = json.loads(st.session_state.raw_text_value)
            xml_str = xmltodict.unparse({"root": obj}, pretty=True)
            st.success("Converted JSON to XML:")
            st.code(xml_str, language="xml")
            st.download_button("Download XML", xml_str, "converted.xml", "text/xml", type="primary", icon=":material/file_download:")
        except Exception as e:
            st.error(f"Conversion failed: {e}")

    # XML → JSON
    if col2.button("Convert XML → JSON", type="primary", icon=":material/swap_horiz:"):
        try:
            obj = xmltodict.parse(st.session_state.raw_text_value)
            json_str = json.dumps(obj, indent=4)
            st.success("Converted XML to JSON:")
            st.code(json_str, language="json")
            st.download_button("Download JSON", json_str, "converted.json", "application/json", type="primary", icon=":material/file_download:")
        except Exception as e:
            st.error(f"Conversion failed: {e}")

    # JSON → TOML
    if col3.button("Convert JSON → TOML", type="primary", icon=":material/swap_horiz:"):
        try:
            obj = json.loads(st.session_state.raw_text_value)
            import toml
            toml_str = toml.dumps(obj)
            st.success("Converted JSON to TOML:")
            st.code(toml_str, language="toml")
            st.download_button("Download TOML", toml_str, "converted.toml", "text/plain", type="primary", icon=":material/file_download:")
        except Exception as e:
            st.error(f"Conversion failed: {e}")

    # JSON → TOON (stub implementation)
    if col4.button("Convert JSON → TOON", type="primary", icon=":material/swap_horiz:"):
        try:
            obj = json.loads(st.session_state.raw_text_value)
            if isinstance(obj, list) and all(isinstance(d, dict) for d in obj):
                keys = list(obj[0].keys())
                toon_lines = [f"{len(obj)} " + " ".join(keys)]
                for item in obj:
                    toon_lines.append(" ".join(str(item.get(k, "")) for k in keys))
                toon_str = "\n".join(toon_lines)
                st.success("Converted JSON to TOON:")
                st.code(toon_str, language="text")
                st.download_button("Download TOON", toon_str, "converted.toon", "text/plain", type="primary", icon=":material/file_download:")
            else:
                st.warning("TOON demo currently supports only arrays of objects with identical keys.")
        except Exception as e:
            st.error(f"Conversion failed: {e}")


elif section == "CSV Analysis":
    st.title("📊 CSV Data Analysis")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            st.success("CSV uploaded successfully!")

            # Preview
            st.subheader("🔎 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # Summary stats
            st.subheader("📈 Summary Statistics")
            st.write(df.describe(include="all"))
            st.markdown("""
            **Explanation of statistics:**
            - count: number of non-null entries
            - mean: average (numeric columns)
            - std: spread of values
            - min/max: smallest and largest values
            - 25%, 50%, 75%: quartiles (distribution spread)
            - unique/top/freq: categorical column insights
            """)

            # Column-wise insights
            st.subheader("📋 Column Insights")
            for col in df.columns:
                st.write(f"**{col}**")
                if pd.api.types.is_numeric_dtype(df[col]):
                    st.write(f"- Numeric column with mean = {df[col].mean():.2f}, std = {df[col].std():.2f}")
                    st.bar_chart(df[col].dropna())
                else:
                    st.write(f"- Categorical column with {df[col].nunique()} unique values")
                    st.bar_chart(df[col].value_counts())

            # Extra analytics if certain columns exist
            if "Salary" in df.columns:
                max_salary_row = df.loc[df["Salary"].idxmax()]
                st.subheader("💰 Highest Salary")
                st.write(f"{max_salary_row['Name']} ({max_salary_row['Team']}) — ${max_salary_row['Salary']:,.0f}")

                st.subheader("💵 Salary Distribution")
                st.bar_chart(df["Salary"].dropna())

                st.subheader("📊 Average Salary per Group")
                avg_salary = df.groupby("Team")["Salary"].mean().sort_values(ascending=False)
                st.bar_chart(avg_salary)

                st.subheader("🏆 Top 10 Highest Paid")
                top10 = df.nlargest(10, "Salary")[["Name", "Salary"]].set_index("Name")
                st.bar_chart(top10)

            if "Team" in df.columns:
                st.subheader("🏀 Players per Team")
                st.bar_chart(df["Team"].value_counts())

                st.subheader("📋 Players by Team")
                for team, players in df.groupby("Team")["Name"]:
                    st.markdown(f"**{team}**: {', '.join(players.dropna().tolist())}")

            if "Position" in df.columns:
                st.subheader("🧩 Position Distribution")
                st.bar_chart(df["Position"].value_counts())

        except Exception as e:
            st.error(f"Error reading CSV: {e}")