

# initialize API key (get it from https://platform.openai.com)
# client = OpenAI(api_key="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")

import streamlit as st
import streamlit.components.v1 as components

st.title("Streamlit + Botpress Chatbot")

botpress_script = """
<script src="https://cdn.botpress.cloud/webchat/v3.2/inject.js"></script>
<script>
  window.botpressWebChat.init({
    "botId": "your-bot-id",
    "hostUrl": "https://cdn.botpress.cloud/webchat/v3.2",
    "messagingUrl": "https://messaging.botpress.cloud",
    "clientId": "your-client-id",
    "botName": "My Bot",
    "configUrl": "https://files.bpcontent.cloud/2025/08/30/17/20250830171827-30BA02RV.json"
  });
</script>
"""

components.html(botpress_script, height=600)


print("Chatbot: Hello! I’m your AI assistant. Type 'bye' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chatbot: Goodbye 👋")
        break

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[{"role": "user", "content": user_input}]
    )

    print("Chatbot:", response.choices[0].message.content)