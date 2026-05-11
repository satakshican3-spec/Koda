import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Koda Planner", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

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
mode = st.sidebar.radio("Navigate", ["Note Vault", "Story Lab", "Travel % Packing"])
if st.sidebar.button("Lock System"):
    st.session_state.authenticated = False
    st.rerun()

if mode == "Note Vault":
    st.header("Note Vault")
    if 'notes' not in st.session_state:
        st.session_state.notes = []

    with st.form("note_entry", clear_on_submit=True):
        new_note = st.text_input("New Entry:")
        if st.form_submit_button("Save to Vault"):
            st.session_state.notes.append({"text": new_note, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})

    for n in reversed(st.session_state.notes):
        st.info(f"{n['time']}: {n['text']}")

elif mode == "Story Lab":
    st.header("Story Lab")
    title = st.text_input("Draft Title", value="Untitled")
    content = st.text_area("Write your story here...", height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Draft", data=content, file_name=f"{title}.txt")
    with col2:
        st.write(f"Word Count: {len(content.split())}")

elif mode == "Travel & Packing":
    st.header("Travel Logistics")

    if 'trips' not in st.session_state:
        st.session_state.trips = []

    with st.expander("Add New Destination"):
        d_name = st.text_input("Destination")
        d_date = st.date_input("Date")
        if st.button("Add Stop"):
            st.session_state.trips.append({"Place": d_name, "Date": str(d_date)})
            st.rerun()


    if st.session_state.trips:
        st.table(pd.DataFrame(st.session_state.trips))

    st.write("---")
    st.subheader("Packing Checklist")
    items = ["Passport/ID", "Phone Charger", "Laptop", "Clothes", "Headphones"]
    for item in items:
        st.checkbox(item)
      
st.write("---")
st.caption("Koda v1.0 | Calgary Developer Portfolio")
