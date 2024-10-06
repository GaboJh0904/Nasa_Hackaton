<template>
  <div>
    <div v-if="showChat" class="chat-container">
      <div class="chat-header">
        <h6>Chat Assistant</h6>
        <span style="cursor: pointer;" @click="toggleChat">
          {{ showChat ? '–' : '+' }}
        </span>
      </div>
      <div class="chat-messages" ref="chatMessages">
        <div v-for="(message, index) in chatMessages" :key="index" class="message-container">
          <div v-if="message.sender === 'User'" class="user-message-container">
            <div class="user-message">
              <div class="message-meta">
                <strong>{{ message.sender }}</strong> - <small>{{ formatDate(message.timestamp) }}</small>
              </div>
              <div>
                <p v-html="formatMessage(message.text)"></p>
              </div>
            </div>
          </div>
          <div v-else class="bot-message-container">
            <div class="bot-message">
              <div class="message-meta">
                <strong>{{ message.sender }}</strong> - <small>{{ formatDate(message.timestamp) }}</small>
              </div>
              <div v-html="message.text"></div>
            </div>
          </div>
        </div>
        <div v-if="isTyping" class="typing-indicator">
          <em>Gemini Bot está escribiendo...</em>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="Escribe tu mensaje...">
        <button @click="sendMessage" class="send-button">
          <span>📤</span>
        </button>
      </div>
    </div>
    <div v-else class="chat-button-container">
      <button @click="toggleChat" class="chat-button">Abrir Chat</button>
    </div>
  </div>
</template>

<script>
import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from '@google/generative-ai';
import marked from 'marked';

const apiKey = 'AIzaSyCvn69rzg3TRORMrnHat5dOnbx66kbmI8s';
const genAI = new GoogleGenerativeAI(apiKey);

export default {
  data() {
    return {
      showChat: false,
      chatMessages: [],
      inputMessage: "",
      chatSession: null,
      isTyping: false
    };
  },
  setup() {
  },
  methods: {
    async initChat() {
      let promptIA = "";

      promptIA = "Eres un experto y profesional astrologo, tienes mucho concocimiento para atender a preguntas acerca del planeta tierra. No puedes responder nada realacionado a otra rama que no sea astronomia y te especializas en la tierra. Da una bienvenida al usuario preguntandole que le interas saber de la tierra";

      const model = genAI.getGenerativeModel({
        model: "gemini-1.5-pro-latest",
        systemInstruction: promptIA
      });

      const generationConfig = {
        temperature: 1,
        topP: 0.95,
        topK: 64,
        maxOutputTokens: 8192,
        responseMimeType: "text/plain",
      };

      const safetySettings = [
        {
          category: HarmCategory.HARM_CATEGORY_HARASSMENT,
          threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
          threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
          threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
          threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
      ];

      this.chatSession = model.startChat({
        generationConfig,
        safetySettings,
        history: [],
      });

      const result = await this.chatSession.sendMessage("INSERT_INPUT_HERE");
      const initialMessage = result.response.text();

      this.addMessage("Gemini Bot", initialMessage, true);
    },
    async toggleChat() {
      this.showChat = !this.showChat;
      if (this.showChat && !this.chatSession) {
        this.initChat();
      }
    },
    async sendMessage() {
      const userMessage = this.inputMessage.trim();
      if (userMessage === "") return;

      this.addMessage("User", userMessage);

      this.inputMessage = "";
      this.isTyping = true;
      const botResponse = await this.getBotResponse(userMessage);
      this.isTyping = false;

      this.addMessage("Gemini Bot", botResponse, true);
      this.scrollToBottom();
    },
    async getBotResponse(userMessage) {
      const result = await this.chatSession.sendMessage(userMessage);
      return result.response.text();
    },
    addMessage(sender, text, isHTML = false) {
      const timestamp = new Date();
      let formattedText = text;
      if (isHTML) {
        formattedText = marked(text);
      }
      const message = { sender, text: formattedText, timestamp, isHTML };
      this.chatMessages.push(message);
    },
    formatDate(date) {
      return date.toLocaleTimeString();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
    },
    formatMessage(text) {
      // Convert double asterisks to bold tags
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

      // Convert * items into list items
      text = text.replace(/\* (.*?)(\n|$)/g, '<li>$1</li>');

      // Wrap list items in unordered list tags
      text = text.replace(/(<li>.*<\/li>)+/g, '<ul>$&</ul>');

      return text;
    },
  }
};
</script>


<style scoped>
.chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 500px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.chat-header {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  display: flex;
  justify-content: space-between;
}

.chat-messages {
  height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.message-container {
  margin-bottom: 10px;
}

.user-message-container {
  display: flex;
  justify-content: flex-end;
}

.user-message {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border-radius: 10px;
  max-width: 70%;
}

.bot-message-container {
  display: flex;
  justify-content: flex-start;
}

.bot-message {
  background-color: #f0f0f0;
  color: #333;
  padding: 10px;
  border-radius: 10px;
  max-width: 70%;
}

.message-meta {
  font-size: 0.8em;
  margin-bottom: 5px;
  color: #666;
}

.typing-indicator {
  text-align: center;
  font-style: italic;
  color: #888;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.chat-input input {
  flex: 1;
  margin-right: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
}

.chat-input button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
}

.chat-button-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
}

.chat-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
