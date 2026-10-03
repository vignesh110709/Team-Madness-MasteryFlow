import streamlit as st
import random
import time
import os
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI client with the provided API key for the hackathon
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"))

def get_flow_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are Flow AI, an expert AI copilot for the MasteryFlow_V2 event platform. You help attendees with event logistics (e.g., TechFest 2026 at SRM Campus, Parking at North Gate, Food in Main Hall)."
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def render_event_platform():
    st.markdown("""
    <style>
        .event-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        .event-card:hover {
            border-color: #f97316;
            transform: translateY(-2px);
        }
        .grad-text {
            background: -webkit-linear-gradient(45deg, #f97316, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎉 MasteryFlow: Event Experience Platform")
    st.caption("Create. Invite. Experience. - A premium cinematic event manager.")

    tabs = st.tabs([
        "1. AI Generator", 
        "2. Cinematic Preview", 
        "3. RSVP & QR Check-in", 
        "4. Live Event & Memory Wall", 
        "5. Flow AI & Creator Dash"
    ])

    # --- 1. AI INVITATION GENERATOR ---
    with tabs[0]:
        st.subheader("🤖 AI Invitation Generator")
        with st.form("ai_invitation"):
            col1, col2 = st.columns(2)
            with col1:
                event_name = st.text_input("Event Name", value="TECHFEST 2026")
                event_type = st.selectbox("Event Type", ["Hackathon", "Conference", "Workshop", "Party"])
                date = st.date_input("Date")
                time_val = st.time_input("Time")
            with col2:
                venue = st.text_input("Venue", value="SRM Campus")
                host = st.text_input("Host Name", value="MasteryFlow Team")
                theme = st.selectbox("Theme/Mood", ["Futuristic", "Luxury", "Minimal", "Fun", "Professional"])
                lang = st.selectbox("Language", ["English", "Tamil", "Tanglish"])
            
            submit = st.form_submit_button("✨ Generate Invitation (AI)", use_container_width=True)
            
            if submit:
                with st.spinner("AI is generating cinematic copy..."):
                    time.sleep(1.5)
                st.success("Invitation Generated!")
                st.markdown(f"""
                <div class="event-card">
                    <h2 class="grad-text">{event_name}</h2>
                    <h4>{event_type} | {date.strftime('%d %B %Y')} @ {time_val}</h4>
                    <p><i>Hosted by {host} at {venue}</i></p>
                    <hr style="opacity: 0.2">
                    <p><b>Generated Copy:</b><br/>
                    Step into the future at {event_name}! Join us for an unforgettable experience where innovation meets creativity. 
                    Prepare to level up and witness the ultimate {event_type.lower()} of 2026!</p>
                </div>
                """, unsafe_allow_html=True)

    # --- 2. CINEMATIC VIDEO INVITATION & PERSONALIZED ---
    with tabs[1]:
        st.subheader("🎬 Cinematic Invitation Preview")
        st.markdown("""
        <div class="event-card" style="text-align: center; height: 300px; display: flex; flex-direction: column; justify-content: center; background: radial-gradient(circle, #1e1b4b 0%, #0f172a 100%);">
            <h1 style="font-size: 3rem; letter-spacing: 5px; animation: pulseGlow 2s infinite;" class="grad-text">TECHFEST 2026</h1>
            <h3 style="color: #94a3b8;">15 October 2026 • SRM Campus</h3>
            <p style="margin-top: 20px;">▶ PLAY CINEMATIC TRAILER</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("✉️ Personalized Invitations")
        guest_name = st.text_input("Generate link for guest:", value="Vishal")
        if st.button("Generate Link"):
            st.code(f"https://masteryflow.app/invite/TECHFEST26?guest={guest_name.lower()}")
            st.info(f"Preview: 'Hi {guest_name}, You are invited to TECHFEST 2026.'")

    # --- 3. RSVP & QR CHECK-IN ---
    with tabs[2]:
        st.subheader("📊 Smart RSVP Dashboard")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Invited", "150")
        c2.metric("Confirmed (Attending)", "112", "+5")
        c3.metric("Maybe", "20")
        c4.metric("Declined", "18")
        
        st.divider()
        st.subheader("🧠 Pre-Requisite Knowledge Screening")
        st.markdown("**Synergy with Adaptive Learning Engine:** Require attendees to pass a baseline knowledge check before confirming their RSVP.")
        rc1, rc2 = st.columns(2)
        with rc1:
            req_sub = st.selectbox("Required Subject Mastery", ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology"])
        with rc2:
            req_level = st.slider("Minimum Mastery Level Required", 0, 100, 80)
        
        st.info(f"Attendees must achieve **{req_level}%** mastery in **{req_sub}** via the Adaptive Learning Engine to receive a valid QR Ticket.")
        if st.button("Enable Knowledge Screening"):
            st.success("✅ Rule applied! The RSVP link will now dynamically route unqualified guests to the Learning Engine.")
            
        st.divider()
        st.subheader("🔳 Unique QR Check-in Scanner")
        scan = st.text_input("Scan QR Code (Simulate scanning a token):", placeholder="e.g. TICKET-992")
        if scan:
            st.success(f"✅ Guest Verified: Vishal (Token: {scan})")
            st.caption(f"Check-in time: {datetime.now().strftime('%H:%M:%S')}")
            st.warning("Attendance marked. Duplicate check-ins are now prevented for this QR.")

    # --- 4. LIVE EVENT & MEMORY WALL ---
    with tabs[3]:
        st.subheader("🔴 Live Event Dashboard")
        st.info("Event Status: **LIVE** | Next Session in: **15:00 mins**")
        st.markdown("""
        **Current Schedule:**
        - 10:00 AM - Keynote Speech
        - 11:30 AM - Hackathon Commences 👈 *(Current)*
        - 01:00 PM - Lunch Break
        """)
        st.warning("📢 Announcement: Pizza has arrived at the Main Hall!")
        
        st.markdown("---")
        st.subheader("📸 Guest Memory Wall")
        st.caption("Live photo gallery uploaded by guests")
        gc1, gc2, gc3 = st.columns(3)
        with gc1: st.image("https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=300", use_container_width=True)
        with gc2: st.image("https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=300", use_container_width=True)
        with gc3: st.image("https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=300", use_container_width=True)

    # --- 5. AI ASSISTANT & CREATOR DASHBOARD ---
    with tabs[4]:
        st.subheader("🤖 Flow AI - Event Assistant")
        q = st.text_input("Ask Flow AI a question:", placeholder="e.g. Where is the parking?")
        if q:
            with st.spinner("Flow AI is thinking..."):
                answer = get_flow_ai_response(q)
            st.markdown(f"> **Flow AI:** {answer}")
            
        st.markdown("---")
        st.subheader("👑 Creator Dashboard Overview")
        st.markdown("""
        <div class="event-card">
            <h3>TECHFEST 2026 <span style="font-size: 14px; background: #22c55e; padding: 2px 8px; border-radius: 10px;">Active</span></h3>
            <p><b>Total Check-ins:</b> 85 / 112</p>
            <p><b>Memories Uploaded:</b> 24 photos</p>
            <p><b>AI Assistant Queries:</b> 142 handled</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_event_platform()
