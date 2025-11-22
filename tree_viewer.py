import streamlit as st
import json
import yaml
import xml.etree.ElementTree as ET

# Add a helper to inject larger fonts
def set_tree_viewer_style():
    st.markdown(
        """
        <style>
        .tree-viewer * {
            font-size: 18px !important;  /* Increase font size */
        }
        .stJson { 
            font-size: 18px !important;  /* JSON/YAML viewer */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_json_yaml(data):
    """Use st.json for JSON/YAML with larger fonts."""
    set_tree_viewer_style()
    st.json(data)

def render_xml_interactive(element):
    """Interactive XML viewer using tabs for children."""
    set_tree_viewer_style()
    st.markdown(f"**Tag:** `{element.tag}`", unsafe_allow_html=True)
    if element.attrib:
        st.write("Attributes:", element.attrib)
    if element.text and element.text.strip():
        st.write("Text:", element.text.strip())

    children = list(element)
    if children:
        tab_labels = [child.tag for child in children]
        tabs = st.tabs(tab_labels)
        for tab, child in zip(tabs, children):
            with tab:
                render_xml_interactive(child)

def show_tree(raw_text, fmt_type):
    """Entry point: parse and render tree based on format type."""
    try:
        set_tree_viewer_style()
        if fmt_type == "JSON":
            data = json.loads(raw_text)
            render_json_yaml(data)
        elif fmt_type == "YAML":
            data = yaml.safe_load(raw_text)
            render_json_yaml(data)
        elif fmt_type == "XML":
            root = ET.fromstring(raw_text)
            st.subheader("🌳 XML Tree Viewer")
            render_xml_interactive(root)
        else:
            st.warning("Tree view not supported for this format.")
    except Exception as e:
        st.error(f"Error building tree: {e}")