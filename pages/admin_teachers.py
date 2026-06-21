import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("👨‍🏫 Manage Teachers")
    tab1, tab2, tab3 = st.tabs(["➕ Add Teacher", "📋 View Teachers", "🗑️ Delete Teacher"])

    # ADD 
    with tab1:
        with st.form("add_teacher_form"):
            teacher_id = st.text_input("Teacher ID (e.g. TCH101)")
            name       = st.text_input("Teacher Name")
            department = st.text_input("Department")
            subject    = st.text_input("Subject")
            if st.form_submit_button("Add Teacher"):
                if teacher_id and name and department and subject:
                    try:
                        run_query(
                            "INSERT INTO teachers (teacher_id, name, department, subject) VALUES (%s,%s,%s,%s)",
                            (teacher_id, name, department, subject)
                        )
                        st.success(f"✅ Teacher '{name}' added successfully!")
                    except Exception:
                        st.error("⚠️ Teacher ID already exists. Use a unique ID.")
                else:
                    st.error("Please fill in all fields.")

    #  VIEW 
    with tab2:
        teachers = run_query(
            "SELECT teacher_id, name, department, subject FROM teachers ORDER BY name",
            fetch=True
        )
        if teachers:
            df = pd.DataFrame(teachers)
            df.columns = ["Teacher ID", "Name", "Department", "Subject"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No teachers added yet.")

    #  DELETE 
    with tab3:
        teachers_list = run_query(
            "SELECT teacher_id, name, subject FROM teachers ORDER BY name",
            fetch=True
        )
        if teachers_list:
            del_opts = {
                f"{t['name']} — {t['subject']}": t["teacher_id"]
                for t in teachers_list
            }
            sel = st.selectbox("Select Teacher to Delete", list(del_opts.keys()))
            st.warning(f"⚠️ This will also delete ALL feedback given to **{sel.split('—')[0].strip()}**.")
            if st.button("🗑️ Delete Teacher"):
                tid = del_opts[sel]
                run_query("DELETE FROM feedback WHERE teacher_id=%s", (tid,))
                run_query("DELETE FROM teachers WHERE teacher_id=%s", (tid,))
                st.success("✅ Teacher deleted successfully!")
                st.rerun()
        else:
            st.info("No teachers to delete.")
