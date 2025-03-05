import gradio as gr
import os
from groq import Groq

# Access the API key from the Hugging Face secret
api_key = os.getenv("GROQ_API_KEY")  

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

# Translations for English and French
translations = {
    "English": {
        "title": "<h1><strong>🤵 Fashion Assistant</strong></h1><p>Get expert outfit recommendations for any occasion!</p>",
        "fashion_advice": "Fashion Advice",
        "organize_outfit": "Organize a Fit for an Occasion",
        "language": "Language",
        "occasion_label": "Occasion (e.g., Wedding, Party, Casual, etc.)",
        "weather_label": "Weather (e.g., Winter, Summer, Wet, Dry, etc.)",
        "gender_label": "Gender",
        "headwear_label": "Headwears",
        "top_label": "Tops",
        "bottom_label": "Bottoms",
        "shoes_label": "Shoes",
        "accessories_label": "Accessories",
        "generate_outfit": "Organize an Outfit",
        "ask_button": "✋ Ask",
        "english_button": "English",
        "french_button": "French",
        "selected_language": "Selected Language is English",
        "placeholder": "Ask about fashion, trends, or outfit ideas...",
        "generated_fit": "Generated Outfit Idea",
    },
    "French": {
        "title": "<h1>🤵 Assistant de Mode</h1><p>Obtenez des recommandations de tenues d'experts pour toute occasion!</p>",
        "fashion_advice": "Conseils de Mode",
        "organize_outfit": "Organiser une tenue pour une occasion",
        "language": "Langue",
        "occasion_label": "Occasion (par exemple, Mariage, Fête, Décontracté, etc.)",
        "weather_label": "Temps (par exemple, Hiver, Été, Humide, Sec, etc.)",
        "gender_label": "Genre",
        "headwear_label": "Chapeaux",
        "top_label": "Hauts",
        "bottom_label": "Bas",
        "shoes_label": "Chaussures",
        "accessories_label": "Accessoires",
        "generate_outfit": "Organiser une tenue",
        "ask_button": "✋ Demander",
        "english_button": "Anglais",
        "french_button": "Français",
        "selected_language": "La langue sélectionnée est le français",
        "placeholder": "Renseignez-vous sur la mode, les tendances ou les idées de tenues...",
        "generated_fit": "Idée de tenue générée",
    }
}

current_language = "English"


# Initialize conversation history
conversation_history = []

   
# Chatbot Function for Fashion Advice   
def chat_with_bot_stream(user_input):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) == 1:
        conversation_history.insert(0, {
            "role": "system",
            "content": "You are an expert fashion stylist. Provide detailed outfit recommendations based on the occasion, personal style, and trends. Suggest headwear, tops, bottoms, shoes, and accessories while considering seasonality and color coordination."
        })
        
    # Generate AI response
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=conversation_history,
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,
        stop=None,
    )
    
    response_content = completion.choices[0].message.content 

    
    conversation_history.append({"role": "assistant", "content": response_content})
    
    return [(msg["content"] if msg["role"] == "user" else None, 
             msg["content"] if msg["role"] == "assistant" else None) 
            for msg in conversation_history]
    
    
def update_language(language):
    global current_language
    current_language = language
    
    return [
        translations[language]["title"],  
        translations[language]["ask_button"], 
        translations[language]["occasion_label"],  
        translations[language]["weather_label"], 
        translations[language]["gender_label"], 
        translations[language]["headwear_label"], 
        translations[language]["top_label"], 
        translations[language]["bottom_label"],  
        translations[language]["shoes_label"],  
        translations[language]["accessories_label"],  
        translations[language]["generate_outfit"],  
        translations[language]["english_button"],  
        translations[language]["french_button"], 
        translations[language]["placeholder"], 
        translations[language]["organize_outfit"], 
        translations[language]["generated_fit"],
        translations[language]["selected_language"]
        
    ]

    

# Function to handle splitting by commas and removing extra spaces
def process_item(item):
    if item.strip():
        return [i.strip() for i in item.strip().split(',')]
    else: # item is empty
        return []

# Organize a style based on what clothing you have for headwear, top, bottom, shoes, and accessories for a specific gender, occasion, and weather
def organize_a_fit(headwear, top, bottom, shoes, accessories, occasion, weather, gender):
    if not any([headwear.strip(), top.strip(), bottom.strip(), shoes.strip(), accessories.strip(), occasion.strip(), weather.strip(), gender.strip()]):  
        return "Please provide all the necessary information."

    clothing_items = []
    if headwear.strip():
        headwear_items = process_item(headwear)
        clothing_items.append(f"Headwear: {', '.join(headwear_items)}")  # Join split items
    if top.strip():
        top_items = process_item(top)
        clothing_items.append(f"Top: {', '.join(top_items)}")
    if bottom.strip():
        bottom_items = process_item(bottom)
        clothing_items.append(f"Bottom: {', '.join(bottom_items)}")
    if shoes.strip():
        shoes_items = process_item(shoes)
        clothing_items.append(f"Shoes: {', '.join(shoes_items)}")
    if accessories.strip():
        accessories_items = process_item(accessories)
        clothing_items.append(f"Accessories: {', '.join(accessories_items)}")
    
    clothing_details = "\n".join(clothing_items)
                              
    # Define the conversation with a system message and a user message
    messages = [
    {
        "role": "system",
             "content": f"Given the following available clothing items, organize multiple stylish outfit combinations for a {gender} attending a {occasion} in {weather} weather. \n\n{clothing_details}\n\nFeel free to mix and match, suggest creative styling options, and fill in missing pieces where necessary."
    }
    ]
    
    # Generate the completion with streaming
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,  # Pass the messages list here
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=0.95,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content



with gr.Blocks(
    css="""
    .gradio-container {
        background: linear-gradient(to right, #ff6600, #ff99cc);
    }
    
    .gr-button {
        color: white;
        font-weight: bold;
    }
    
    .fashion_inputs {
        background-color: transparent !important;
        border: none !important; /* Removes any default border */
        padding: none !important;
    }
    

    .chatOutput .bubble-wrap { /* The chatbot's container */
        background: linear-gradient(to right, #ff6600, #ff99cc);
        color: black; 
        border: none; /* Removes any borders */
        border-radius: 10px; 
        min-height: 500px; /* Ensures it maintains height when empty */
        padding: 10px; /* Optional: Padding for a clean look */
    }


    .block.svelte-11xb1hd { /* The outer most container for inputs in Organize a Fit for an Occasion */
        border: none;
        background: linear-gradient(to right, #ff6600, #ff99cc);
        border-radius: 10px; 
        padding: 10px; 
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
    }

    textarea.scroll-hide.svelte-173056l { /* The actual textarea field */
        background: transparent;
        color: white; 
        border: none; 
        padding: 8px; 
        font-size: 16px; 
        outline: none; 
        height: 38px; /* Keeps the height */
        resize: none; /* Prevent resizing */
    }


    textarea[disabled] { /* The fashion ouput that has its interactive as false in Organize a Fit for an Occasion*/
        opacity: 0.75;
        cursor: not-allowed; /* Adds a visual cue for users */
    }

    
    .fashion_inputs textarea, .fashion_inputs button, .chatInput button, .chatInput textarea{
        width: 100%; 
        background-color: white !important; 
        color: black !important; 
        padding: 5px; 
        outline: none !important; 
        box-shadow: none !important; 
    }
    
    .FR_language, .EN_language{
        width: 500px; 
        width: 500px; 
        padding: 5px; 
        outline: none !important; 
        box-shadow: none !important; 
        font-size: 48px; 
        display: flex; 
        gap: 25px; /* space between elements when using flex */
        background-color: white !important; 
        color: black !important;
    }

    button[role="tab"] {
        font-size: 18px; 
    }
    
    button.svelte-1tcem6n#component-39-button { /* Language tab*/
        margin-left: auto;
    }
    
    
    .fashion_markdown {
        color: white
    }
    
    h1 { 
        text-align: center; 
        font-size: 32px; 
        margin-bottom: 10px; 
    }
    
    p {
        text-align: center;
        font-size: 20px;
    }
    """
) as demo:
    
    title = gr.HTML(translations[current_language]["title"])

    with gr.Tabs():  
        with gr.TabItem(translations[current_language]["fashion_advice"]):
            chatbot = gr.Chatbot(label="Fashion Chatbot", height=500, elem_classes="chatOutput")
            with gr.Row(equal_height=True, height=50, elem_classes="chatInput"):
                user_input = gr.Textbox(
                    placeholder=translations[current_language]["placeholder"],
                    lines=1,
                    show_label = False,
                    scale=1
                )
                send_button = gr.Button(translations[current_language]["ask_button"], scale=0)
            
            # Chatbot functionality
            send_button.click(
                fn=chat_with_bot_stream,
                inputs=user_input,
                outputs=chatbot,
                queue=True
            ).then(
                fn=lambda: "",
                inputs=None,
                outputs=user_input
            )
            
        # Organize a Fit Tab
        with gr.TabItem(translations[current_language]["organize_outfit"], elem_classes="fashion_inputs"):
            fit_markdown = gr.Markdown(translations[current_language]["organize_outfit"], elem_classes="fashion_markdown")
            
            fashion_label = gr.Markdown(translations[current_language]["generated_fit"])
            fashion_output = gr.Textbox(show_label = False, interactive=False)
            
            occasion_label = gr.Markdown(translations[current_language]["occasion_label"])
            occasion_input = gr.Textbox(show_label = False)

            weather_label = gr.Markdown(translations[current_language]["weather_label"])
            weather_input = gr.Textbox(show_label = False)

            gender_label = gr.Markdown(translations[current_language]["gender_label"])
            gender_input = gr.Textbox(show_label = False)

            headwear_label = gr.Markdown(translations[current_language]["headwear_label"])
            headwear_input = gr.Textbox(show_label = False)

            top_label = gr.Markdown(translations[current_language]["top_label"])
            top_input = gr.Textbox(show_label = False)

            bottom_label = gr.Markdown(translations[current_language]["bottom_label"])
            bottom_input = gr.Textbox(show_label = False)

            shoes_label = gr.Markdown(translations[current_language]["shoes_label"])
            shoes_input = gr.Textbox(show_label = False)

            accessories_label = gr.Markdown(translations[current_language]["accessories_label"])
            accessories_input = gr.Textbox(show_label = False)

            generate_btn = gr.Button(translations[current_language]["generate_outfit"])

            generate_btn.click(
                fn=organize_a_fit,
                inputs=[headwear_input, top_input, bottom_input, shoes_input, accessories_input, occasion_input, weather_input, gender_input],
                outputs=fashion_output
            )
            
        with gr.TabItem("Language|Langue", elem_classes="language_tab"): 
            with gr.Row(): 
                english_button = gr.Button(translations[current_language]["english_button"], elem_classes="EN_language")
                french_button = gr.Button(translations[current_language]["french_button"], elem_classes="FR_language")
                
                language_label = gr.Markdown(translations[current_language]["selected_language"])
                
                english_button.click(
                    fn=lambda: update_language("English"),
                    inputs=None,
                    outputs=[
                        title,              
                        send_button,            
                        occasion_label,          
                        weather_label,            
                        gender_label,          
                        headwear_label,            
                        top_label,                
                        bottom_label,             
                        shoes_label,             
                        accessories_label,            
                        generate_btn,   
                        english_button,  
                        french_button, 
                        user_input,   
                        fit_markdown, 
                        fashion_label,  
                        language_label
                    ]
                )
                
                french_button.click(
                    fn=lambda: update_language("French"),
                    inputs=None,
                    outputs=[
                        title,
                        send_button,
                        occasion_label,          
                        weather_label,            
                        gender_label,          
                        headwear_label,            
                        top_label,                
                        bottom_label,             
                        shoes_label,             
                        accessories_label,     
                        generate_btn,
                        english_button,
                        french_button,
                        user_input,
                        fit_markdown,
                        fashion_label,
                        language_label

                    ]
                )

            
                    
demo.launch()
