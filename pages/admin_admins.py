import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("🔐 Manage Admins")
    tab1, tab2 = st.tabs(["➕ Add Admin", "📋 View Admins"])

    #  ADD 
    with tab1:
        with st.form("add_admin_form"):
            admin_id = st.text_input("Admin ID (e.g. ADM002)")
            name     = st.text_input("Full Name")
            email    = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Add Admin"):
                if admin_id and name and email and password:
                    try:
                        run_query(
                            "INSERT INTO admins (admin_id, name, email, password) VALUES (%s,%s,%s,%s)",
                            (admin_id, name, email, password)
                        )
                        st.success(f"✅ Admin '{name}' added successfully!")
                    except Exception:
                        st.error("⚠️ Admin ID or Email already exists.")
                else:
                    st.error("Please fill in all fields.")

    #  VIEW 
    with tab2:
        admins = run_query(
            "SELECT admin_id, name, email FROM admins ORDER BY name",
            fetch=True
        )
        if admins:
            df = pd.DataFrame(admins)
            df.columns = ["Admin ID", "Name", "Email"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No admins found.")
