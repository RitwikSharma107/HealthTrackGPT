from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
load_dotenv()

## Function to load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(llm_model, input_prompt,image):
    model=genai.GenerativeModel(llm_model)
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
        # Check if a file has been uploaded
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            st.error('Please upload a file !!!')
            raise FileNotFoundError("No file uploaded")


def main():
    st.set_page_config(page_title="Health App")
    st.sidebar.title('Generative AI Project')
    nav = st.sidebar.radio('Navigation',['Home','About',"Technologies Used"])
    if nav == 'Home':
        st.header("HealthTrackGPT")

        choice = st.sidebar.radio('What would you like to do?',['Health Analysis', 'Track Meal', 'Conversational Q&A']) 

        if choice == 'Health Analysis':
            st.subheader("Enter your details")
            age = st.number_input("Age (years):", min_value=0, max_value=100, value=25, step=1)
            gender = st.radio("Gender:", options=["Male", "Female", "Other"])
            st.write("Height:")
            height_feet = st.number_input("Feet:", min_value=0, max_value=8, value=6, step=1, key='height_feet')
            height_inches = st.number_input("Inches:", min_value=0, max_value=11, value=0, step=1, key='height_inches')
            weight = st.number_input("Weight (pounds):", min_value=0, max_value=1000, value=150, step=1)
            activity_level = st.radio("Activity Level:", options=[
                "Sedentary (No exercise)",
                "Light (Exercise 1-3 times a week)",
                "Moderate (Exercise 4-5 times a week)",
                "Active (Exercise daily)"
            ])
            submit=st.button("Analyze health")

            input_prompt=f"""
                            You are an fitness expert where you need to consider the follwing provided factors of a person:
                            Age: {age} years old,
                            Gender: {gender},
                            Height: {height_feet} feet {height_inches} inches
                            Weight: {weight} pounds
                            Activity Level: {activity_level}

                            Based on above provided factors, calculate and tell about the person's:
                            Maintenance Calorie: Display Value and don't show calculation
                            BMI: Display Value and don't show calculation
                            Body Fat(%): Display Value and don't show calculation

                            Finally, provide health advise to the person.                
                            
            """

            if submit:
                llm_model=genai.GenerativeModel('gemini-pro')
                response=llm_model.generate_content([input_prompt])
                st.subheader("Analysis")
                st.write(response.text)

        
        if choice == 'Track Meal':
            uploaded_file = st.file_uploader("Upload an image of your meal", type=["jpg", "jpeg", "png"])
            image=""   
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image.", use_column_width=True)
            submit=st.button("Track Meal")

            input_prompt="""
                            You are an expert nutritionist and dietician where you need to 
                            see the food items from the image
                            and calculate the total calories, 
                            also provide the details of every food items with calories intake in below format

                            Food Items:
                            1. Item 1 - no of calories
                            2. Item 2 - no of calories
                            3. Item 3 - no of calories
                            ----
                            ----
                            
                            Food Macronutrients:
                            Mention the percentage split of the ratio of proteins, fats, carbohydrates and fibers

                            Now, mention whether the food is healthy or not based on macronutrients of the food.

                            Advise better alternatives to the above food items to make the meal healthier.
            """

            if submit:
                image_data=input_image_setup(uploaded_file)
                response=get_gemini_repsonse('gemini-pro-vision',input_prompt,image_data)
                st.subheader("Meal Analysis")
                st.write(response)
        
        if choice == 'Conversational Q&A':
            st.subheader("Please ask any questions about health and fitness")
            user_question = st.text_input("Question")
            submit = st.button("Get Answer")

            if submit :
                input_prompt = f"""
                    You are a health and fitness expert who is professional nutritionist and dietician. Answer the following question accurately and concisely:
                    Question: {user_question}
                """
                llm_model=genai.GenerativeModel('gemini-pro')
                response=llm_model.generate_content([input_prompt])
                st.subheader("Answer")
                st.write(response.text)


    if nav == 'About':
        st.header('About')
        st.write("HealthTrackGPT is an AI-Driven Health Management App which is versatile and interactive application designed to assist users in managing their health and fitness. Utilizing the power of Generative AI, the app provides personalized health analyses, meal tracking, and a conversational Q&A feature to address users' health and nutrition-related queries. The app's user-friendly interface ensures an engaging and informative experience for all users.")

        st.subheader("Health Analysis")
        st.markdown("""
        - **User Input:** Users can input their age, gender, height, weight, and activity level.
        - **AI Analysis:** The app uses this data to provide personalized metrics:
        - Maintenance Calorie
        - BMI (Body Mass Index)
        - Body Fat Percentage
        - **Health Advice:** Based on the user's input, the app offers tailored health advice.
        """)

        st.subheader("Track Meal")
        st.markdown("""
        - **Image Upload:** Users can upload an image of their meal.
        - **AI Analysis:** The app analyzes the meal to provide:
        - Total calories
        - Detailed breakdown of each food item with its calorie count
        - Macronutrient distribution (proteins, fats, carbohydrates, fibers)
        - Health assessment of the meal
        - Suggestions for healthier alternatives
        """)

        st.subheader("Conversational Q&A")
        st.markdown("""
        - **User Interaction:** Users can ask health and fitness-related questions.
        - **AI Response:** The app provides accurate and concise answers, leveraging the expertise of a virtual health and fitness professional.
        """)
        

    if nav == 'Technologies Used':
        st.write('')
        st.header("Technologies Used")
        html5 = """
        <div>
        <ul>
            <li>Python</li>
            <li>Streamlit</li>
            <li>LangChain</li>
            <li>Google Gemini</li>
            <li>Visual Studio Code</li>
        </ul>
        </div>
        """
        st.markdown(html5,unsafe_allow_html=True)
        

    st.sidebar.header('Developed by')
    html_string = "<div><a href='https://ritwiksharma107.github.io/portfolio/' style='color:#e60067; text-decoration:none;'>Ritwik Sharma</a></div>"
    st.sidebar.markdown(html_string, unsafe_allow_html=True)

if __name__ == '__main__':
    main()