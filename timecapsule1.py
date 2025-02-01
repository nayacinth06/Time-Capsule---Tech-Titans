import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import base64  # Required for encoding images

def set_background_image(image_path):
    """Set a background image from a local file."""
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_database():
    conn = sqlite3.connect("time_capsule.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS capsule (
            id INTEGER PRIMARY KEY,
            message TEXT,
            open_date TEXT,
            created_on TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_time_capsule(message, open_date):
    try:
        open_date_obj = datetime.strptime(open_date, "%Y-%m-%d")
        conn = sqlite3.connect("time_capsule.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO capsule (message, open_date, created_on) VALUES (?, ?, ?)", 
                      (message, open_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True, f"Time capsule created! Come back on {open_date} to open it."
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def get_all_capsules():
    conn = sqlite3.connect("time_capsule.db")
    df = pd.read_sql_query("SELECT * FROM capsule", conn)
    conn.close()
    return df

def open_time_capsule(capsule_id):
    conn = sqlite3.connect("time_capsule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, open_date FROM capsule WHERE id = ?", (capsule_id,))
    result = cursor.fetchone()
    
    if not result:
        return False, "No time capsule found!"
    
    message, open_date = result
    open_date_obj = datetime.strptime(open_date, "%Y-%m-%d")
    current_date = datetime.now()
    
    if current_date >= open_date_obj:
        cursor.execute("DELETE FROM capsule WHERE id = ?", (capsule_id,))
        conn.commit()
        conn.close()
        return True, message
    else:
        conn.close()
        return False, f"It's not time yet! Come back on {open_date} to open it."

def main():
    st.set_page_config(page_title="Digital Time Capsule", page_icon="🕰️")

    # Set the background image (replace with the correct local path)
    set_background_image("background.jpg")  # Ensure the image file is in the same directory

    st.title("🕰️ Digital Time Capsule")
    create_database()
    
    tab1, tab2 = st.tabs(["Create Capsule", "View Capsules"])
    
    with tab1:
        st.header("Create a New Time Capsule")
        with st.form("create_capsule"):
            message = st.text_area("Enter a message for your future self:", height=150)
            open_date = st.date_input("Select the date to open the capsule:")
            submit_button = st.form_submit_button("Create Time Capsule")
            
            if submit_button:
                if message.strip():
                    success, result = create_time_capsule(message, open_date.strftime("%Y-%m-%d"))
                    if success:
                        st.success(result)
                    else:
                        st.error(result)
                else:
                    st.error("Please enter a message!")
    
    with tab2:
        st.header("Your Time Capsules")
        capsules = get_all_capsules()
        
        if not capsules.empty:
            for _, capsule in capsules.iterrows():
                with st.expander(f"Capsule #{capsule['id']} - Opens on {capsule['open_date']}"):
                    st.write(f"Created on: {capsule['created_on']}")
                    if st.button("Try to Open", key=f"open_{capsule['id']}"):
                        success, result = open_time_capsule(capsule['id'])
                        if success:
                            st.success("Time Capsule Opened!")
                            st.write("Message from the past:")
                            st.info(result)
                        else:
                            st.warning(result)
        else:
            st.info("No time capsules found. Create one in the 'Create Capsule' tab!")

if __name__ == "__main__":
    main()
