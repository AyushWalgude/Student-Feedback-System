import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("🧑‍🎓 Manage Students")
    tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View Students", "🗑️ Delete Student"])

    #  ADD 
    with tab1:
        with st.form("add_student_form"):
            student_id = st.text_input("Student ID (e.g. CS101)")
            name       = st.text_input("Full Name")
            department = st.text_input("Department")
            email = st.text_input("Email Id") #changed
            if st.form_submit_button("Add Student"):
                if student_id and name and department and email :
                    try:
                        run_query(
                            "INSERT INTO students (student_id, name, department, email) VALUES (%s,%s,%s,%s)",
                            (student_id, name, department, email)
                        )
                        st.success(f"✅ Student '{name}' added! They can now register an account.") # chnagedSSS
                    except Exception:
                        st.error("⚠️ Student ID already exists. Use a unique ID.")
                else:
                    st.error("Please fill in all fields.")

    #  VIEW 
    with tab2:
        students = run_query(
            "SELECT student_id, name, department, email, is_registered FROM students ORDER BY name",
            fetch=True
        )
        if students:
            df = pd.DataFrame(students)
            df.columns = ["Student ID", "Name", "Department", "Email", "Registered?"]
            df["Registered?"] = df["Registered?"].apply(lambda x: "✅ Yes" if x else "❌ No")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No students added yet.")

    #  DELETE 
    with tab3:
        students_list = run_query(
            "SELECT student_id, name, department FROM students ORDER BY name",
            fetch=True
        )
        if students_list:
            del_opts = {
                f"{s['name']} ({s['student_id']}) — {s['department']}": s["student_id"]
                for s in students_list
            }
            sel = st.selectbox("Select Student to Delete", list(del_opts.keys()))
            st.warning(f"⚠️ This will also delete ALL feedback by **{sel.split('(')[0].strip()}**.")
            if st.button("🗑️ Delete Student"):
                sid = del_opts[sel]
                run_query("DELETE FROM feedback WHERE student_id=%s", (sid,))
                run_query("DELETE FROM students WHERE student_id=%s", (sid,))
                st.success("✅ Student deleted successfully!")
                st.rerun()
        else:
            st.info("No students to delete.")
