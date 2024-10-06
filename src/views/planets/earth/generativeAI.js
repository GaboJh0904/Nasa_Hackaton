import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from '@google/generative-ai';

const apiKey = 'AIzaSyCvn69rzg3TRORMrnHat5dOnbx66kbmI8s';  // Define la API Key directamente aquí

const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
    model: "gemini-1.5-flash-latest",
    systemInstruction: "Eres un experto en java",
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
        category: "HARM_CATEGORY_HARASSMENT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        category: "HARM_CATEGORY_HATE_SPEECH",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        category: "HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
    },
];

async function generateResponse(userInput) {
    try {
        const chatSession = model.startChat({
            generationConfig,
            safetySettings,
            history: [
                { role: "user", parts: [{ text: "Mensaje de bienvenida" }] } // El primer contenido debe tener 'parts' con un arreglo de partes
            ],
        });
        const result = await chatSession.sendMessage(userInput);
        return result.response.text;
    } catch (error) {
        console.error("Error generating response:", error);
        return "Lo siento, hubo un error al generar la respuesta.";
    }
}

export { generateResponse };