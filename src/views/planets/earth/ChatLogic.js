import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from '@google/generative-ai';

const apiKey = 'AIzaSyCvn69rzg3TRORMrnHat5dOnbx66kbmI8s';  // Define la API Key directamente aquí
const genAI = new GoogleGenerativeAI(apiKey);

export default {
    data() {
        return {
            chatMessages: [],
            inputMessage: ""
        };
    },
    mounted() {
        this.initChat();
    },
    methods: {
        async initChat() {
            const model = genAI.getGenerativeModel({
                model: "gemini-1.5-pro-latest",
                systemInstruction: "Eres un experto en python y tu primer mensaje es dar la bienvenida al usuario, su nombre es Max",
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

            const chatSession = model.startChat({
                generationConfig,
                safetySettings,
                history: [],
            });

            const result = await chatSession.sendMessage("INSERT_INPUT_HERE");
            const initialMessage = result.response.text();

            this.addMessage("Gemini Bot", initialMessage);
        },
        async sendMessage() {
            const userMessage = this.inputMessage.trim();
            if (userMessage === "") return;

            this.addMessage("User", userMessage);

            const botResponse = await this.getBotResponse(userMessage);

            this.addMessage("Gemini Bot", botResponse);

            this.inputMessage = "";
        },
        async getBotResponse(userMessage) {
            const result = await chatSession.sendMessage(userMessage);
            return result.response.text();
        },
        addMessage(sender, text) {
            this.chatMessages.push({sender, text});
        }
    }
};
