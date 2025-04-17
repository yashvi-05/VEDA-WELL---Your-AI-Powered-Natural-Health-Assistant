import streamlit as st
import sqlite3

# Function to create the database and table if they don't exist
def create_database():
    conn = sqlite3.connect("remedies.db")
    cursor = conn.cursor()
    
    # Create the remedies table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS remedies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom TEXT,
            category TEXT,
            remedy TEXT
        )
    ''')

    # Insert example data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM remedies")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO remedies (symptom, category, remedy) VALUES (?, ?, ?)
        ''', [
            ('headache', 'ayurveda', 'Take a cup of ginger tea to relieve headaches.'),
            ('stress', 'yoga', 'Practice deep breathing and meditation to reduce stress.'),
            ('cold', 'ayurveda', 'Drink warm water with honey and lemon for relief from cold.'),
            ('anxiety', 'yoga', 'Perform pranayama (breathing exercises) to reduce anxiety.'),
            ('fatigue', 'ayurveda', 'Drink ashwagandha tea to improve energy levels.'),
        ])
        conn.commit()

    conn.close()

# Function to fetch remedies from the database based on the user's input
def get_remedies(symptom):
    try:
        conn = sqlite3.connect("remedies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT category, remedy FROM remedies WHERE symptom LIKE ?", ('%' + symptom + '%',))
        results = cursor.fetchall()
        conn.close()

        if not results:
            return "⚠️ No remedy found for this symptom."
        
        formatted = ""
        for category, remedy in results:
            emoji = "🌿" if category == "ayurveda" else "🧘" if category == "yoga" else "🤲"
            formatted += f"{emoji} **{category.capitalize()}**: {remedy}\n"
        return formatted
    except sqlite3.OperationalError as e:
        return "⚠️ There was an issue accessing the remedies database. Please try again later."

# Add custom CSS for styling
custom_css = """
<style>
    body {
        background-color: #f5f7fa;
    }
    .stApp {
        background-image: linear-gradient(to right, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
        padding: 10px;
    }
    .chat-bubble {
        border-radius: 10px;
        padding: 10px;
        margin: 8px 0;
    }
    .user-bubble {
        background-color: #d4f0ff;
        border-left: 4px solid #3399ff;
    }
    .bot-bubble {
        background-color: #d9fdd3;
        border-left: 4px solid #5cb85c;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title and instructions for the chatbot
st.markdown("<h1 style='text-align: center; color: #5c5470;'>🌿 Instant Heal Chatbot 🧘‍♀️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your natural remedy assistant powered by Ayurveda, Yoga, and Mudras.</p>", unsafe_allow_html=True)

# Initialize chat memory to store conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Create the database and table if they don't exist
create_database()

# Input from the user
user_input = st.chat_input("Type a health concern or say hello...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    user_msg = user_input.lower()

    # Handling simple greetings and basic conversation
    if any(word in user_msg for word in ["hi", "hello", "hey"]):
        bot_reply = "Hello! 😊 How can I help you with your health today?"
    elif "how are you" in user_msg:
        bot_reply = "I'm doing great! Thanks for asking. How can I assist you today?"
    elif "thank" in user_msg:
        bot_reply = "You're most welcome! 🌼 Take care!"
    else:
        # Fetch remedies from the database based on the user's input
        bot_reply = get_remedies(user_msg)

    # Add the bot's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat messages
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# Footer information
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 13px;'>💡 Prototype by <b>Yashvi Shah</b> and Team</p>", unsafe_allow_html=True)

