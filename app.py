import re

import streamlit as st

# Translation dictionary
translations = {
    "en": {
        "page_title": "Tenth to Inch",
        "app_title": "Tenth to Inch",
        "app_description": """
        This app converts between three common measurement formats:
        * Decimal feet (e.g., 5.25 ft)
        * Architectural notation (e.g., 5'-3")
        * Decimal inches (e.g., 63.0")
        """,
        "language_selector": "Language / Idioma",
        "decimal_feet": "Decimal Feet",
        "decimal_feet_input": "Enter measurement in decimal feet",
        "arch_notation": "Architectural Notation",
        "arch_input": "Enter measurement (e.g., 5'-3 8/16\")",
        "arch_help": "Format: feet'-inches sixteenths/16\" (e.g., 5'-3 8/16\")",
        "decimal_inches": "Decimal Inches",
        "decimal_inches_input": "Enter measurement in decimal inches",
        "convert_from": "Convert from",
        "conversion_results": "Conversion Results",
        "converting_from": "Converting from",
        "invalid_arch": "Invalid architectural notation format. Please use the format: feet'-inches sixteenths/16\" (e.g., 5'-3 8/16\")",
    },
    "es": {
        "page_title": "Décimos a pulgadas",
        "app_title": "Décimos a pulgadas",
        "app_description": """
        Esta aplicación convierte entre tres formatos comunes de medidas:
        * Pies decimales (ej., 5.25 ft)
        * Notación arquitectónica (ej., 5'-3")
        * Pulgadas decimales (ej., 63.0")
        """,
        "language_selector": "Language / Idioma",
        "decimal_feet": "Pies Decimales",
        "decimal_feet_input": "Ingrese la medida en pies decimales",
        "arch_notation": "Notación Arquitectónica",
        "arch_input": "Ingrese la medida (ej., 5'-3 8/16\")",
        "arch_help": "Formato: pies'-pulgadas dieciseisavos/16\" (ej., 5'-3 8/16\")",
        "decimal_inches": "Pulgadas Decimales",
        "decimal_inches_input": "Ingrese la medida en pulgadas decimales",
        "convert_from": "Convertir desde",
        "conversion_results": "Resultados de la Conversión",
        "converting_from": "Convirtiendo desde",
        "invalid_arch": "Formato de notación arquitectónica inválido. Por favor use el formato: pies'-pulgadas dieciseisavos/16\" (ej., 5'-3 8/16\")",
    },
}


def decimal_feet_to_arch(decimal_feet):
    """Convert decimal feet to architectural notation (feet-inches-sixteenths)"""
    feet = int(decimal_feet)
    remaining_decimal = decimal_feet - feet
    total_inches = remaining_decimal * 12
    inches = int(total_inches)
    remaining_inches = total_inches - inches
    sixteenths = round(remaining_inches * 16)

    # Handle case where sixteenths rounds to 16
    if sixteenths == 16:
        sixteenths = 0
        inches += 1

    # Handle case where inches becomes 12
    if inches == 12:
        inches = 0
        feet += 1

    if sixteenths == 0:
        if inches == 0:
            return f"{feet}'"
        return f"{feet}'-{inches}\""
    return f"{feet}'-{inches} {sixteenths}/16\""


def decimal_feet_to_decimal_inches(decimal_feet):
    """Convert decimal feet to decimal inches"""
    return decimal_feet * 12


def arch_to_decimal_feet(arch_str):
    """Convert architectural notation to decimal feet"""
    # Parse the architectural string
    if not arch_str:
        return 0

    feet = 0
    inches = 0
    sixteenths = 0

    # Extract feet
    feet_match = re.search(r"(\d+)\'", arch_str)
    if feet_match:
        feet = int(feet_match.group(1))

    # Extract inches
    inches_match = re.search(r"-(\d+)\"", arch_str)
    if inches_match:
        inches = int(inches_match.group(1))

    # Extract sixteenths
    sixteenths_match = re.search(r"(\d+)/16", arch_str)
    if sixteenths_match:
        sixteenths = int(sixteenths_match.group(1))

    # Convert to decimal feet
    return feet + (inches / 12) + (sixteenths / (16 * 12))


def decimal_inches_to_decimal_feet(decimal_inches):
    """Convert decimal inches to decimal feet"""
    return decimal_inches / 12


# Initialize session state for language if it doesn't exist
if "language" not in st.session_state:
    st.session_state["language"] = "en"

# Set up the Streamlit app
st.set_page_config(
    page_title=translations[st.session_state["language"]]["page_title"], page_icon="📏"
)

# Language selector in the sidebar
with st.sidebar:
    selected_language = st.selectbox(
        "Language / Idioma",
        options=["English", "Español"],
        index=0 if st.session_state["language"] == "en" else 1,
    )

    # Update the language in session state based on selection
    if selected_language == "English" and st.session_state["language"] != "en":
        st.session_state["language"] = "en"
        st.rerun()
    elif selected_language == "Español" and st.session_state["language"] != "es":
        st.session_state["language"] = "es"
        st.rerun()

# Get current language
lang = st.session_state["language"]
t = translations[lang]

# Main app content
st.title(t["app_title"])
with st.sidebar:
    st.markdown(t["app_description"])

# Create three columns for input
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(t["decimal_feet"])
    decimal_feet_input = st.number_input(
        t["decimal_feet_input"],
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.3f",
        key="decimal_feet",
    )
    convert_from_decimal_feet = st.button(f"{t['convert_from']} {t['decimal_feet']}")

with col2:
    st.subheader(t["arch_notation"])
    arch_input = st.text_input(
        t["arch_input"], value="", help=t["arch_help"], key="arch"
    )
    convert_from_arch = st.button(f"{t['convert_from']} {t['arch_notation']}")

with col3:
    st.subheader(t["decimal_inches"])
    decimal_inches_input = st.number_input(
        t["decimal_inches_input"],
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.3f",
        key="decimal_inches",
    )
    convert_from_decimal_inches = st.button(
        f"{t['convert_from']} {t['decimal_inches']}"
    )

# Create a results section
st.markdown("---")
st.header(t["conversion_results"])

# Handle conversions based on button clicks
if convert_from_decimal_feet:
    # Convert from decimal feet to the other formats
    st.subheader(f"{t['converting_from']} {t['decimal_feet']}")

    feet_value = decimal_feet_input
    arch_value = decimal_feet_to_arch(feet_value)
    inches_value = decimal_feet_to_decimal_inches(feet_value)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t["decimal_feet"], f"{feet_value:.3f} ft")
    with col2:
        st.metric(t["arch_notation"], arch_value)
    with col3:
        st.metric(t["decimal_inches"], f'{inches_value:.3f}"')

elif convert_from_arch:
    # Convert from architectural notation to the other formats
    st.subheader(f"{t['converting_from']} {t['arch_notation']}")

    try:
        feet_value = arch_to_decimal_feet(arch_input)
        arch_value = arch_input
        inches_value = decimal_feet_to_decimal_inches(feet_value)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t["decimal_feet"], f"{feet_value:.3f} ft")
        with col2:
            st.metric(t["arch_notation"], arch_value)
        with col3:
            st.metric(t["decimal_inches"], f'{inches_value:.3f}"')
    except:
        st.error(t["invalid_arch"])

elif convert_from_decimal_inches:
    # Convert from decimal inches to the other formats
    st.subheader(f"{t['converting_from']} {t['decimal_inches']}")

    feet_value = decimal_inches_to_decimal_feet(decimal_inches_input)
    arch_value = decimal_feet_to_arch(feet_value)
    inches_value = decimal_inches_input

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t["decimal_feet"], f"{feet_value:.3f} ft")
    with col2:
        st.metric(t["arch_notation"], arch_value)
    with col3:
        st.metric(t["decimal_inches"], f'{inches_value:.3f}"')
