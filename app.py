import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Koda: Multi-Modal Suite", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "folders" not in st.session_state:
    st.session_state.folders = {"Main": []}
if "matrix_data" not in st.session_state:
    st.session_state.matrix_data = []

if not st.session_state.authenticated:
    st.title("Koda: Authentication Required")
    st.write("System Status: Locked")

    access_token = st.text_input("Enter Master Session Key", type="password")

    if st.button("Initialize Decryption"):
        if access_token == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Token. Authorization Denied.")
    st.stop()

st.sidebar.title("Koda Suite")
st.sidebar.write("Core Status: Active")
module = st.sidebar.radio("Select Module Profile", ["Document Manager", "Story Lab", "Travel Planner"])

if st.sidebar.button("Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()

if module == "Document Manager":
    st.header("Hierarchical File Explorer")

    col1, col2 = st.columns([1, 2])
    with col1:
        new_dir = st.text_input("Provision New Directory Name:")
        if st.button("Register Folder"):
            if new_dir and new_dir not in st.session_state.folders:
                st.session_state.foldes[new_dir] = []
                st.success(f"Directory /{new_dir} appended to mapping data.")
                st.rerun()

    st.write("---")

    current_dir = st.selectbox("Navigate Virtual File System:", options=list(st.session_state.folders.keys()))

    with st.expander(f"Construct Document Payload under /{current_dir}"):
        doc_title = st.text_input("Document Node Title")
        doc_payload = st.text_area("Document Content Payload")
        if st.button("Write to Node Array"):
            if doc_title:
                st.session_state.folders[current_dir].append({
                    "title": doc_title,
                    "content": doc_payload,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Data written safely to memory storage node.")
                st.rerun()

    st.subheader(f"Directory Audit for Location: /{current_dir}")
    if st.session_state.folders[current_dir]:
        for node_idx, document_node in enumerate(st.session_state.folders[current_dir]):
            with st.expander(f"Node File: {document_node['title']} [Timestamp: {document_node['date']}]"):
                st.text(document_node['content'])
                if st.button(f"Purge File Node", key=f"purge_{current_dir}_{node_idx}"):
                    st.session_state.folders[current_dir].pop(node_idx)
                    st.rerun()
    else:
        st.info("Target directory array contains 0 file items.")

elif module == "Story Lab":
    st.header("Narrative Design Studio & Workspace")
    story_node_title = st.text_input("Production Title", value="Draft_Segment")
    input_buffer = st.text_area("Narrative Input Buffer Stream", height=400)

    word_count_vector = len(input_buffer.split())
    character_density = len(input_buffer)

    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.write(f"Runtime Word Metrics: {word_count_vector}")
    with metrics_col2:
        st.write(f"Raw Character Density: {character_density}")

    st.download_button(
        label="Download Plain Text Document (.txt)",
        data=input_buffer,
        file_name=f"{story_node_title}.txt",
        mime="text/plain"
    )

elif module == "Travel Planner":
    st.header("Logistics Relational Data Matrix")

    with st.expander("Ingest New Matrix Vector Point"):
        geo_target = st.text_input("Geographical Node Location")
        temporal_target = st.date_input("Temporal Coordinate Date")
        logistics_notes = st.text_area("Logistics Context Payload")

        if st.button("Append Vector Entry"):
            if geo_target:
                st.session_state.matrix_data.append({
                    "Destination Vector": geo_target,
                    "Temporal Stamp": str(temporal_target),
                    "Logistics Context": logistics_notes
                })
                st.success("Vector successfully appended to global dataframe array.")
                st.rerun()

    st.subheader("Tabular Data Visualization Canvas")
    if st.session_state.matrix_data:
        dataframe_matrix = pd.DataFrame(st.session_state.matrix_data)
        st.dataframe(dataframe_matrix, use_container_width=True)

        if st.button("Wipe Matrix Memory"):
            st.session_state.matrix_data = []
            st.rerun()
        else:
            st.info("Logistics matrix array currently empty. Awaiting operational input data points.")

st.write("---")
st.caption("Koda Software Suite v1.0 | Calgary Portfolio Project Asset")
