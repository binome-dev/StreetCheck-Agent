from openai import OpenAI
from main import get_all_data  # Assuming you still use get_all_data to get postcode information

# Set the OpenAI API key
client = OpenAI(api_key="")  # Replace with your OpenAI API key


# Define a function to generate a response using OpenAI GPT-4's chat interface
def generate_response(prompt):
    try:
        # Call OpenAI's ChatCompletion API to generate a response
        completion = client.chat.completions.create(
            model="gpt-4",  # Or use "gpt-3.5-turbo" or other models
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides detailed information and analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,  # Set a large token limit to handle long text
            temperature=0.7,  # Control the diversity of the output (0.0 to 1.0)
            top_p=1.0,  # Control nucleus sampling
            frequency_penalty=0.0,  # Control repeated generation
            presence_penalty=0.0  # Control topic diversity
        )

        # Directly access the content attribute of the message object
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating response: {e}"


# Main function: handle user input and generate a response
def handle_user_query(postcode):
    # Reuse the get_all_data function from main.py to scrape all data
    data = get_all_data(postcode)
    
    # Construct the prompt to submit to the LLM, clarifying its role
    prompt = (
        f"You are an assistant that helps people find detailed information "
        f"about a location based on its postal code. You have detailed data for the following seven categories: "
        f"Summary, Housing, People, Culture, Employment, Crime, and Nearby Services. "
        f"For each category, summarize the information provided and give an analysis. "
        f"Finally, based on all these factors, analyze the comfort of living in this area and the potential issues people might face.\n\n"
        
        f"Here is the detailed information for postcode {postcode}:\n\n"
        f"postcode {postcode}:\n\n"
        f"Summary:\n{data['Summary']}\n\n"
        f"Housing:\n{data['Housing']}\n\n"
        f"People:\n{data['People']}\n\n"
        f"Culture:\n{data['Culture']}\n\n"
        f"Employment:\n{data['Employment']}\n\n"
        f"Crime:\n{data['Crime']}\n\n"
        f"Nearby Services:\n{data['Nearby']}\n\n"
        f"Please summarize this data for the user."
    )
    
    # Generate the LLM response
    response = generate_response(prompt)
    return response

# Test function
if __name__ == "__main__":
    user_postcode = "E201GS"  # User input postcode
    llm_response = handle_user_query(user_postcode)
    print("Generated LLM Summary:\n", llm_response)
