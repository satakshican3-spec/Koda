import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Koda Planner", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "folders" not in st.session_state:
    st.session_state.folders = {"Main": []}
if "trips" not in st.session_state:
    st.session_state.trips = []

if not st.session_state.authenticated:
    st.title("Koda: System Locked")
    password = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock"):
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Access Denied")
    st.stop()

st.sidebar.title("Koda Suite")
mode = st.sidebar.radio("Navigate", ["Document Manager", "Story Lab", "Travel Planner"])

if st.sidebar.button("Lock System"):
    st.session_state.authenticated = Falase
    st.rerun()

if mode == "Document Manager":
    st.header("Document Manager")

    col1, col2 = st.columns([1, 2])
    with col1:
        new_folder = st.text_input("New Folder Name:")
        if st.button("Create Folder"):
            if new_folder and new_folder not in st.session_state.folders:
                st.session_state.folders[new_folders] = []
                st.success(f"Folder '{new_folder}' created")
                st.rerun()
    st.write("---")

    selected_folder = st.selectbox("Current Directory:", options=list(st.session_state.folders.keys()))

    with st.expander(f"New Document in/{selected_folder}"):
        doc_title = st.text_input("Document Title")
        doc_content = st.text_area("Content")
        if st.button("Save to Folder"):
            st.session_state.folders[selected_folder].append({
                "title": doc_title,
                "content": doc_content,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Document Saved")
            st.rerun()

    st.subheader(f"Files in /{selected_folder}")
    if st.session_state.folders[selected_folder]:
        for idx, doc in enumerate(st.session_state.folders[selected_folder):
            with st.expander(f"{doc['title']} (Created: {doc['date']})"):
                st.write(doc['content'])
                if st.button(f"Delete {doc['title']}", key=f"del_{idx}"):
                    st.session_state.folders[selected_folder].pop(idx)
                    st.rerun()
    else:
        st.info("This folder is empty.")

elif mode == "Story Lab":
    st.header("Story Lab")
    title = st.text_input("Story Title", value="Untitled")
    content = st.text_area("Write your draft...", height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Export as .txt", data=content, file_name=f"{title}.txt")
    with col2:
        words = len(content.split())
        st.write(f"Word Count: {words}")

elif mode == "Travel Planner":
    st.header("Travel Logistics")

    with st.expander("Add Trip Destination"):
        d_name = st.text_input("Place")
        d_date = st.date_input("Date")
        d_notes = st.text_input("Quick Notes")
        if st.button("Add to Itinerary"):
            st.session_state.trips.append({"Destination": d_name, "Date": str(d_date), "Notes": d_notes})
            st.rerun()

    if st.session_state.trips:
        st.table(pd.DataFrame(st.session_state.trips))
    else:
        st.write("No trips planned yet.")

st.write("---")
st.caption("Koda v1.0 | Student Developer Portfolio | Calgary, AB")
