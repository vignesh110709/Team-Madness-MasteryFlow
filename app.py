import streamlit as st
from datetime import datetime
from openai import OpenAI
import os

# Initialize OpenAI client for the AI Mentor
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"))

def get_tutor_explanation(question, correct_answer, user_answer):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are MasteryFlow's elite AI Mentor, designed to train students for deep mastery. The student got a question wrong. Do not just give them the answer. First, gently explain the flaw in their specific logic. Second, break the concept down into a simple, memorable analogy. Finally, leave them with a short, highly-actionable tip or mini-exercise so they can conquer this concept in the future. Be incredibly encouraging, patient, and engaging!"
                },
                {"role": "user", "content": f"Question: {question}\nCorrect Answer: {correct_answer}\nMy Wrong Answer: {user_answer}"}
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI Mentor: {str(e)}"

st.set_page_config(page_title="MasteryFlow V2", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

if "show_landing" not in st.session_state:
    st.session_state.show_landing = True
    st.session_state.mode = "learning"

import questions_db
PREREQS = questions_db.PREREQS
Q = questions_db.Q

def init():
    if "learners" not in st.session_state:
        st.session_state.learners={
        "Aarav":{"m":{c:0 for c in PREREQS},"a":[],"o":[]},
        "Diya":{"m":{c:0 for c in PREREQS},"a":[],"o":[]}}
        st.session_state.learners["Aarav"]["m"].update({"Computer Science":.92,"Biology":.82,"Physics":.76,"Chemistry":.68,"Mathematics":.50})
        st.session_state.learners["Diya"]["m"].update({"Computer Science":.45,"Biology":.38,"Physics":.30,"Chemistry":.22,"Mathematics":.15})

def action(d,c):
    # Normalize c mapping if needed, e.g., 'Math' -> 'Mathematics'
    norm_c = "Mathematics" if c in ["Math", "Maths"] else c
    weak=[p for p in PREREQS.get(norm_c, []) if d["m"].get(p, 0)<.55]
    hints=sum(x["hint"] for x in d["a"] if x["c"]==norm_c)
    m=d["m"].get(norm_c, 0)
    if weak:return "Remediate Prerequisite",f"{weak[0]} mastery is only {d['m'].get(weak[0], 0)*100:.0f}%."
    if m<.45:return "Practice",f"Mastery is {m*100:.0f}%; more evidence is needed."
    if m<.70 or hints>=2:return "Review",f"Mastery is {m*100:.0f}% with {hints} hint(s)."
    if m<.85:return "Challenge",f"Mastery is {m*100:.0f}%; test deeper transfer."
    return "Advance",f"Mastery is {m*100:.0f}% with prerequisites strong."

def target(m):
    return 1 if m<.45 else 2 if m<.65 else 3 if m<.82 else 4

def pick(d,c):
    used={x["id"] for x in d["a"]}
    pool=[x for x in Q if x[1]==c and x[0] not in used] or [x for x in Q if x[1]==c]
    return sorted(pool,key=lambda x:abs(x[2]-target(d["m"].get(c, 0))))[0]

def update(old,ok,conf,diff,hint,time):
    e=(.65 if ok else 0)+conf/5*.15+diff/4*.10+(0 if hint else .10)
    if time>90:e-=.05
    return round(.75*old+.25*max(0,min(1,e)),3)

init()
names=list(st.session_state.learners)

if st.session_state.show_landing:
    # --- Landing Page & Cinematic Intro ---
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        
        /* --- CINEMATIC INTRO SEQUENCE --- */
        .intro-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000000; z-index: 99999;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow: hidden;
            animation: fadeOutIntro 1.5s ease-in-out forwards 9s; /* Fades out entirely at 9s */
        }
        @keyframes fadeOutIntro {
            to { opacity: 0; visibility: hidden; pointer-events: none; }
        }

        /* Scene 1: Particles */
        .intro-particles {
            position: absolute; top:0; left:0; width: 100vw; height: 100vh;
            background-image: radial-gradient(rgba(139, 92, 246, 0.3) 1px, transparent 1px);
            background-size: 40px 40px;
            opacity: 0;
            animation: fadeInParticles 3s ease-out forwards, slowPan 20s linear infinite;
        }
        @keyframes fadeInParticles { 0% { opacity:0; } 100% { opacity:0.5; } }
        @keyframes slowPan { to { background-position: 0 200px; } }

        /* Scene 2: Flowing Lines (Data Streams) */
        .intro-lines {
            position: absolute; top:0; left:0; width: 100vw; height: 100vh;
            background: linear-gradient(90deg, transparent 0%, rgba(56, 189, 248, 0.1) 50%, transparent 100%);
            background-size: 200% 100%;
            opacity: 0;
            animation: flowLines 4s ease-in-out forwards 2s;
        }
        @keyframes flowLines { 
            0% { opacity:0; background-position: -200% 0; } 
            50% { opacity:1; } 
            100% { opacity:0; background-position: 200% 0; } 
        }

        /* Scene 3 & 4: MasteryFlow Logo & Glow */
        .intro-logo {
            font-size: clamp(3rem, 8vw, 6rem); 
            font-weight: 900; 
            letter-spacing: 12px;
            color: transparent;
            background: linear-gradient(90deg, #475569, #ffffff, #475569);
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            opacity: 0;
            transform: scale(0.9);
            position: relative;
            z-index: 2;
            animation: popLogo 2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards 4s, shineLogo 3s linear infinite 5s;
        }
        @keyframes popLogo {
            0% { opacity:0; transform: scale(0.85); text-shadow: 0 0 0px rgba(255,255,255,0); }
            100% { opacity:1; transform: scale(1); text-shadow: 0 0 40px rgba(56, 189, 248, 0.6); }
        }
        @keyframes shineLogo {
            to { background-position: 200% center; }
        }

        /* Light Sweep Effect */
        .intro-logo::after {
            content: '';
            position: absolute; top: -50%; left: -50%; width: 50px; height: 200%;
            background: rgba(255, 255, 255, 0.8);
            transform: skewX(-20deg);
            filter: blur(10px);
            opacity: 0;
            animation: sweepAnim 2s ease-in-out forwards 6s;
        }
        @keyframes sweepAnim {
            0% { left: -50%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { left: 150%; opacity: 0; }
        }

        /* Subtitle */
        .intro-subtitle {
            font-size: clamp(1rem, 3vw, 1.5rem); 
            color: #94a3b8; 
            font-weight: 300; 
            letter-spacing: 6px;
            margin-top: 1rem;
            opacity: 0;
            z-index: 2;
            animation: fadeInSub 2s ease-out forwards 5.5s;
        }
        @keyframes fadeInSub { to { opacity:1; } }

        /* --- LANDING PAGE CSS --- */
        .stApp {
            background: radial-gradient(circle at center, #1e1b4b 0%, #0f172a 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }
        .particles {
            position: fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:0;
            background-image: radial-gradient(#818cf8 1px, transparent 1px), radial-gradient(#c084fc 1px, transparent 1px);
            background-size: 60px 60px, 120px 120px;
            background-position: 0 0, 30px 30px;
            animation: particleMove 25s linear infinite;
            opacity: 0.25;
        }
        @keyframes particleMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(-120px); }
        }
        .landing-container {
            position: relative; z-index: 1;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; padding: 3rem 1rem;
            opacity: 0;
            animation: revealLanding 2s ease-out forwards 8.5s; /* Reveals precisely as intro fades */
        }
        @keyframes revealLanding { 0% { opacity:0; transform:scale(0.97); } 100% { opacity:1; transform:scale(1); } }
        
        h1.main-title {
            font-size: clamp(3rem, 6vw, 5rem); font-weight: 900; margin-bottom: 0.2rem;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(129, 140, 248, 0.4);
            letter-spacing: 2px;
        }
        h2.subtitle { font-size: clamp(1.5rem, 3vw, 2.5rem); color: #f1f5f9; margin-bottom: 1rem; font-weight: 700; }
        p.desc { font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto 3rem auto; line-height: 1.6; }
        
        .features-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem;
            width: 100%; max-width: 1000px; margin-bottom: 4rem;
        }
        .feature-card {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px; padding: 1.5rem; backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .feature-card:hover {
            transform: translateY(-8px); border-color: rgba(129, 140, 248, 0.6);
            box-shadow: 0 10px 30px rgba(129, 140, 248, 0.15);
            background: rgba(255,255,255,0.05);
        }
        .feature-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
        .feature-title { font-weight: 700; color: #f8fafc; font-size: 1.1rem; }
        
        .progress-wrapper { position: relative; width: 160px; height: 160px; margin: 0 auto 1.5rem auto; }
        .progress-circle {
            width: 160px; height: 160px; border-radius: 50%;
            background: conic-gradient(#818cf8 0%, #c084fc 0%, rgba(255,255,255,0.05) 0%);
            display: flex; align-items: center; justify-content: center;
            animation: fillProgress 1.5s ease-out forwards 9.5s;
            box-shadow: 0 0 20px rgba(129, 140, 248, 0.2);
        }
        .progress-inner {
            width: 140px; height: 140px; border-radius: 50%;
            background: #111827; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }
        .progress-val { font-size: 2.2rem; font-weight: 800; color: #fff; line-height: 1.1; }
        .progress-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
        
        @keyframes fillProgress {
            from { background: conic-gradient(#818cf8 0%, #c084fc 0%, rgba(255,255,255,0.05) 0%); }
            to { background: conic-gradient(#818cf8 0%, #c084fc 92%, rgba(255,255,255,0.05) 92%); }
        }
        
        /* Specific Button Overrides */
        div[data-testid="stButton"] button {
            transition: all 0.3s ease !important;
            border-radius: 12px !important;
            padding: 10px !important;
            height: auto !important;
        }
        div[data-testid="stButton"] button p { font-size: 1.1rem !important; font-weight: 700 !important; }
        
        .btn-primary > div > button {
            background: linear-gradient(135deg, #6366f1, #a855f7) !important;
            border: none !important; color: white !important;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important;
        }
        .btn-primary > div > button:hover {
            box-shadow: 0 0 35px rgba(139, 92, 246, 0.8) !important;
            transform: scale(1.02) !important;
        }
        
        .btn-secondary > div > button {
            background: transparent !important;
            border: 2px solid rgba(139, 92, 246, 0.5) !important;
            color: #e2e8f0 !important;
        }
        .btn-secondary > div > button:hover {
            background: rgba(139, 92, 246, 0.1) !important;
            border-color: #a855f7 !important;
        }
    </style>
    
    <!-- CINEMATIC INTRO OVERLAY -->
    <div class="intro-overlay">
        <div class="intro-particles"></div>
        <div class="intro-lines"></div>
        <div class="intro-logo">MASTERYFLOW</div>
        <div class="intro-subtitle">Learn. Create. Master.</div>
    </div>
    
    <div class="particles"></div>
    <div class="landing-container">
        <h1 class="main-title">LEVEL UP YOUR LEARNING!</h1>
        <h2 class="subtitle">Welcome to MasteryFlow V2</h2>
        <p class="desc">An adaptive learning experience that turns every practice session into your next level.</p>
        
        <div class="features-grid">
            <div class="feature-card"><div class="feature-icon">⚡</div><div class="feature-title">Adaptive Challenges</div></div>
            <div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Live Progress</div></div>
            <div class="feature-card"><div class="feature-icon">🧠</div><div class="feature-title">Smart Interventions</div></div>
            <div class="feature-card"><div class="feature-icon">🗺️</div><div class="feature-title">Personalized Path</div></div>
        </div>
        
        <div class="progress-wrapper">
            <div class="progress-circle">
                <div class="progress-inner">
                    <div class="progress-val">92%</div>
                    <div class="progress-label">Current<br>Mastery</div>
                </div>
            </div>
        </div>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 2rem;">Ready to unlock your next level?</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_space1, col_btn1, col_btn2, col_space2 = st.columns([1, 2, 2, 1])
    
    with col_btn1:
        st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
        if st.button("START YOUR JOURNEY 🚀", use_container_width=True):
            st.session_state.show_landing = False
            st.session_state.mode = "learning"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_btn2:
        st.markdown("<div class='btn-secondary'>", unsafe_allow_html=True)
        if st.button("EXPLORE EVENT PLATFORM", use_container_width=True):
            st.session_state.show_landing = False
            st.session_state.mode = "events"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.mode == "events":
    import event_platform
    event_platform.render_event_platform()
else:
    # --- Main App ---
    # --- Custom CSS for Premium UI ---
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(17, 34, 64, 0.5);
            border-radius: 12px 12px 0px 0px;
            padding: 12px 24px;
            border: 1px solid rgba(255,255,255,0.08);
            border-bottom: none;
            color: #8892b0;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(249, 115, 22, 0.15);
            color: #f97316 !important;
            border-top: 3px solid #f97316;
        }

        /* Glassmorphism Metric Cards */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: rgba(14, 165, 233, 0.5);
        }
        
        /* Premium Buttons (Orange) */
        .stButton>button {
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
        }
        .stButton>button:hover {
            box-shadow: 0 6px 20px rgba(249, 115, 22, 0.6);
            transform: scale(1.03);
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: rgba(10, 25, 47, 0.95) !important;
            backdrop-filter: blur(16px);
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Dataframes */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Headers & Text */
        h1 {
            background: -webkit-linear-gradient(45deg, #f97316, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }
        h2, h3 { color: #f1f5f9 !important; font-weight: 700 !important; }

        /* --- Animations --- */
        @keyframes fadeInSlideUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulseGlow {
            0% { box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3); }
            50% { box-shadow: 0 4px 25px rgba(249, 115, 22, 0.7); }
            100% { box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3); }
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Apply animations */
        .stApp {
            background-size: 200% 200%;
            animation: gradientShift 15s ease infinite;
        }

        div[data-testid="stVerticalBlock"] > div {
            animation: fadeInSlideUp 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }

        .stButton>button {
            animation: pulseGlow 3s infinite;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4204/4204600.png", width=60)
        st.title("Settings")
        st.markdown("---")
        name = st.selectbox("👤 Select Learner", names)
        st.markdown("---")
        st.caption("Active Session: Authenticated")
        
    d = st.session_state.learners[name]

    st.title("🧠 MasteryFlow V2")
    st.markdown("<p style='font-size:18px; color:#94a3b8; margin-bottom: 30px;'>Explainable Adaptive Learning & Intervention Engine</p>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["🎯 Adaptive Practice", "📊 Teacher Dashboard", "🧪 Path Simulation", "🔗 Knowledge Graph"])

    with t1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Practice Arena")
            c = st.selectbox("Select Concept", list(PREREQS))
            q = pick(d,c)
            
            st.info(f"**Target Level:** {target(d['m'].get(c, 0))} | **Difficulty:** {q[2]} | **Type:** {q[3]}")
            st.markdown(f"#### {q[4]}")
            
            ans = st.radio("Choose your answer", q[5], index=None)
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                conf = st.slider("Confidence Level", 1, 5, 3)
            with col_s2:
                secs = st.number_input("Response Time (sec)", 1, 600, 35)
            with col_s3:
                st.write("")
                st.write("")
                hint = st.checkbox("💡 Used a hint")
                
            if st.button("Submit & Adapt", type="primary", use_container_width=True):
                if ans is None: 
                    st.error("⚠️ Please choose an answer first.")
                else:
                    ok = (ans == q[6])
                    old = d["m"].get(c, 0)
                    new = update(old, ok, conf, q[2], hint, secs)
                    d["m"][c] = new
                    d["a"].append({"id":q[0], "c":c, "correct":ok, "hint":int(hint), "difficulty":q[2], "time":datetime.now().isoformat()})
                    ac, why = action(d,c)
                    
                    if ok:
                        st.success("✨ Correct! Outstanding work.")
                        with st.expander("Detailed Explanation", expanded=False):
                            st.write(q[7])
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {q[6]}")
                        
                        st.markdown("### 🤖 AI Mentor Feedback")
                        with st.spinner("AI Mentor is analyzing your answer..."):
                            ai_feedback = get_tutor_explanation(q[4], q[6], ans)
                        st.info(ai_feedback)
                        
                        with st.expander("Standard Explanation", expanded=False):
                            st.write(q[7])
                    
                    st.warning(f"**Next Recommended Action: {ac}** — {why}")
                    if ac in ["Advance","Challenge"]: 
                        st.balloons()
                        st.success("🚀 Mastery is high enough to increase cognitive difficulty.")
                        
        with col2:
            st.markdown("### 📈 Live Stats")
            st.metric(label="Current Mastery", value=f"{d['m'].get(c, 0)*100:.0f}%", delta=f"{(d['m'].get(c, 0) - old)*100:.0f}%" if 'old' in locals() else None)
            
            if d["a"]:
                st.markdown("#### Recent History")
                st.dataframe(d["a"][-6:], use_container_width=True)

    with t2:
        st.markdown("### 👨‍🏫 Teacher Command Center")
        rows = []
        for n,x in st.session_state.learners.items():
            # Iterate over PREREQS keys to safely display all subjects
            for c in PREREQS.keys():
                m = x["m"].get(c, 0)
                ac, why = action(x,c)
                rows.append({"Learner":n, "Concept":c, "Mastery":f"{m*100:.0f}%", "Next Action":ac, "Reason":why})
        st.dataframe(rows, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ⚙️ Manual Override")
        col1, col2, col3 = st.columns(3)
        with col1:
            tn = st.selectbox("Learner", names, key="tn")
        with col2:
            tc = st.selectbox("Concept", list(PREREQS), key="tc")
        with col3:
            ta = st.selectbox("Override Action", ["Advance","Practice","Review","Remediate Prerequisite","Challenge","Teacher Intervention"])
            
        note = st.text_input("Teacher Intervention Note")
        if st.button("Apply Override"):
            st.session_state.learners[tn]["o"].append({"concept":tc, "action":ta, "note":note})
            st.success(f"✅ Override applied for {tn} on {tc}.")

    with t3:
        st.markdown("### 🧪 Path Simulation")
        st.caption("Same curriculum, entirely different paths based on evidence.")
        
        for n in names:
            st.markdown(f"#### Learner: {n}")
            cols = st.columns(4)
            for i,c in enumerate(list(PREREQS)[:4]):
                with cols[i]:
                    st.metric(label=c, value=f"{st.session_state.learners[n]['m'][c]*100:.0f}%")
                    st.caption(f"➔ {action(st.session_state.learners[n],c)[0]}")
            st.markdown("---")
        st.info("💡 **Insight:** Strong evidence increases difficulty; prerequisite gaps trigger automatic remediation.")

    with t4:
        st.markdown("### 🔗 Prerequisite Knowledge Graph")
        st.caption("The engine verifies prerequisite mastery before permitting conceptual advancement.")
        
        for c,p in PREREQS.items():
            if not p:
                st.markdown(f"🟢 **Foundation** ➔ **{c}**")
            else:
                st.markdown(f"🔵 **{', '.join(p)}** ➔ **{c}**")

    st.markdown("---")
    st.caption("MasteryFlow 2.0 • Secure, Explainable, Teacher-in-the-Loop Adaptive Learning")
