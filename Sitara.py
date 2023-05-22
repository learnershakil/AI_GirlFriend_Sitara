import tkinter as tk
from tkinter import scrolledtext
from nltk.sentiment import SentimentIntensityAnalyzer
import openai

class Sitara:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.conversation_history = []

    def greet(self):
        return f"Hello, I'm {self.name}! How can I assist you today?"

    def generate_response(self):
        prompt = "\n".join([f"You: {user_input}" for user_input in self.conversation_history])
        completion = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None,
            api_key=self.api_key
        )
        response = completion.choices[0].text.strip().split("\n")[-1]
        response_sentiment = self.sentiment_analyzer.polarity_scores(response)["compound"]

        # Adjust the response based on sentiment
        if response_sentiment < -0.5:
            response += " Is there something bothering you?"
        elif response_sentiment > 0.5:
            response += " That's great to hear!"

        return response

    def should_end_conversation(self, response):
        # Add logic to determine when the conversation should end
        # For example, if the response contains a certain keyword like "goodbye"
        if "goodbye" in response.lower():
            return True
        return False

class ChatGUI:
    def __init__(self, root, sitara):
        self.root = root
        self.sitara = sitara
        self.root.title("Sitara - AI Chatbot")

        self.chat_box = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.chat_box.pack(pady=10)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.input_entry = tk.Entry(self.input_frame, width=40)
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=5, pady=5)

        self.chat_box.config(state=tk.DISABLED)

    def send_message(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.sitara.conversation_history.append(user_input)
        response = self.sitara.generate_response()

        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "You: " + user_input + "\n")
        self.chat_box.insert(tk.END, "Sitara: " + response + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

        if self.sitara.should_end_conversation(response):
            self.root.quit()

if __name__ == "__main__":
    # Set your OpenAI API key
    api_key = "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"

    # Create an instance of Sitara and start the conversation
    sitara = Sitara("Sitara", api_key)

    root = tk.Tk()
    chat_gui = ChatGUI(root, sitara)
    root.mainloop()
