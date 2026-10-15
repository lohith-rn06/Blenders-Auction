
import streamlit as st
import sqlite3
import hashlib
import secrets
import re
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Blenders-11 | Join the Squad",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_FILE = Path(__file__).parent / "blenders11.db"


# --------------------------------------------------
# CUSTOM UI DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #071710, #102d20);
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 1px;
}

.green {
    color: #61f2a4;
}

.hero {
    font-size: clamp(38px, 5vw, 65px);
    line-height: 1.08;
    font-weight: 800;
    margin-top: 20px;
}

.subtitle {
    color: #bdd0c2;
    font-size: 17px;
    line-height: 1.8;
}

.panel {
    background: #10271c;
    border: 1px solid #2b503b;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 15px;
}

.feature {
    background: #153524;
    border: 1px solid #315940;
    padding: 16px;
    border-radius: 12px;
    margin: 12px 0;
}

.feature p {
    color: #bdd0c2;
    margin-bottom: 0;
}

div[data-testid="stForm"] {
    background: #10271c;
    padding: 22px;
    border: 1px solid #2b503b;
    border-radius: 18px;
}

.stTextInput input {
    background: #081a11;
    color: white;
    border: 1px solid #3b6048;
    border-radius: 9px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #61f2a4;
    color: #071710;
    font-weight: 800;
    border: none;
    border-radius: 10px;
    min-height: 45px;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #a1ffcb;
    color: #071710;
}

.footer {
    text-align: center;
    color: #9bb6a3;
    padding: 30px 0 10px;
}

@media (max-width: 640px) {
    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------

def initialize_database():
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                role TEXT NOT NULL,
                cricket_format TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def hash_password(password):
    salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        310000,
    )

    return salt + "$" + hashed.hex()


initialize_database()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "registered_member" not in st.session_state:
    st.session_state.registered_member = None


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="brand">🏏 BLENDERS<span class="green">-11</span></div>',
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# SUCCESS PAGE
# --------------------------------------------------

if st.session_state.registered_member:

    member = st.session_state.registered_member

    st.balloons()

    st.markdown(f"""
    <div class="panel">
        <h4 style="color:#61f2a4;">REGISTRATION SUCCESSFUL</h4>
        <h1>Welcome to the squad, {member['name']}! 🎉</h1>
        <p class="subtitle">
            Your journey with Blenders-11 starts today.
            Get ready to bring your talent, energy, and ideas to the team.
        </p>
        <div class="feature">
            <h2>🔓 PROJECTS UNLOCKED!</h2>
            <p>
                Congratulations! Your registration is complete.
                Explore the exclusive project previews below.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🚀 Your project previews")

    col1, col2, col3 = st.columns(3)

    projects = [
        (
            col1,
            "🏆 Tournament Central",
            "Explore tournament planning, fixtures, and match-day activities.",
        ),
        (
            col2,
            "📊 Performance Hub",
            "Discover player statistics, progress, and team goals.",
        ),
        (
            col3,
            "🎨 Creative Studio",
            "Share ideas for team branding, posters, and announcements.",
        ),
    ]

    for column, title, description in projects:
        with column:
            st.markdown(f"""
            <div class="feature" style="min-height:155px;">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

    st.success(
        f"Your member profile has been created for {member['email']}."
    )

    st.caption(
        "These are demonstration project previews, not protected project access."
    )

    if st.button("Register another member"):
        st.session_state.registered_member = None
        st.rerun()


# --------------------------------------------------
# REGISTRATION PAGE
# --------------------------------------------------

else:

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <p style="color:#61f2a4;letter-spacing:3px;font-weight:700;">
            YOUR TEAM. YOUR MOMENT.
        </p>

        <div class="hero">
            Your next<br>
            innings starts<br>
            <span class="green">here.</span>
        </div>

        <p class="subtitle">
            Join Blenders-11 and unlock exclusive project previews,
            team opportunities, and unforgettable experiences.
            Your next chapter begins here.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature">
            <h3>🔓 Exclusive projects</h3>
            <p>Explore opportunities for squad members.</p>
        </div>
        <div class="feature">
            <h3>🏏 Team spirit</h3>
            <p>Connect through a shared love of cricket.</p>
        </div>
        <div class="feature">
            <h3>🚀 Make an impact</h3>
            <p>Bring your ideas and talent to the team.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
            <h2>Create your profile</h2>
            <p class="subtitle">
                Complete the form to join the squad.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("registration_form"):

            full_name = st.text_input(
                "Full name *",
                placeholder="Enter your full name",
                max_chars=80,
            )

            email = st.text_input(
                "Email address *",
                placeholder="you@example.com",
                max_chars=254,
            )

            phone = st.text_input(
                "Phone number *",
                placeholder="Enter your phone number",
                max_chars=20,
            )

            role = st.selectbox(
                "Your role",
                ["Player", "Volunteer", "Team Organizer", "Supporter"],
            )

            cricket_format = st.selectbox(
                "Favorite cricket format",
                ["T20", "ODI", "Test Cricket", "All Formats"],
            )

            password = st.text_input(
                "Create password *",
                type="password",
                help="Use at least 8 characters.",
            )

            confirm_password = st.text_input(
                "Confirm password *",
                type="password",
            )

            agreed = st.checkbox(
                "I agree to the Blenders-11 community guidelines."
            )

            submitted = st.form_submit_button(
                "CREATE MY ACCOUNT →",
                use_container_width=True,
            )

        if submitted:

            # Validate required fields
            if not all([
                full_name.strip(),
                email.strip(),
                phone.strip(),
                password,
                confirm_password,
            ]):
                st.error("Please complete all required fields.")

            elif not re.fullmatch(
                r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
                r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
                email.strip(),
            ):
                st.error("Please enter a valid email address.")

            elif not re.fullmatch(
                r"[0-9+() .-]{7,20}",
                phone.strip(),
            ):
                st.error("Please enter a valid phone number.")

            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif password != confirm_password:
                st.error("Your passwords do not match.")

            elif not agreed:
                st.error("Please accept the community guidelines.")

            else:
                try:
                    with sqlite3.connect(DB_FILE) as connection:
                        connection.execute("""
                            INSERT INTO members (
                                full_name,
                                email,
                                phone,
                                role,
                                cricket_format,
                                password_hash
                            )
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            full_name.strip(),
                            email.strip().lower(),
                            phone.strip(),
                            role,
                            cricket_format,
                            hash_password(password),
                        ))

                    st.session_state.registered_member = {
                        "name": full_name.strip().split()[0],
                        "email": email.strip().lower(),
                        "role": role,
                    }

                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error(
                        "This email is already registered. "
                        "Please use another email address."
                    )

                except sqlite3.Error:
                    st.error(
                        "Unable to save your registration. "
                        "Please check the database and try again."
                    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    BLENDERS-11 · BUILT FOR THE LOVE OF CRICKET 🏏
</div>
""", unsafe_allow_html=True)
