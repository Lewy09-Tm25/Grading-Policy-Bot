from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from core.config import MODEL_NAME, OPENAI_API_KEY

# Initialize the OpenAI client using the key validated in core/config.py
client = OpenAI(api_key=OPENAI_API_KEY)

def stream_openai_response(messages: list):
    """
    Sends the conversation history to OpenAI and yields the response chunks in real-time.
    This generator function is designed to be used with Streamlit's st.write_stream().
    
    Args:
        messages (list): A list of dictionaries containing the conversation history.
                         Format: [{"role": "system"/"user"/"assistant", "content": "..."}]
                         
    Yields:
        str: Incremental text chunks returned by the LLM.
    """
    try:
        # Create the streaming API call
        response_stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.1, # Low temperature for strict adherence to the CUNY document
            stream=True      # Crucial for real-time UI updates
        )
        
        # Iterate through the incoming stream and yield the text tokens
        for chunk in response_stream:
            # Extract the text from the chunk. We use .getattr or check for None 
            # because the very last chunk is often empty when the stream closes.
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    # --- Error Handling ---
    # Catching specific OpenAI errors prevents the entire Streamlit app from crashing
    # and provides a readable error message back to the user interface.
    except RateLimitError:
        yield "\n\n**Error:** Rate limit exceeded. Please check your OpenAI billing or try again later."
    except APIConnectionError:
        yield "\n\n**Error:** Network connection failed. Please check your internet connection."
    except APIError as e:
        yield f"\n\n**API Error:** An issue occurred with OpenAI: {str(e)}"
    except Exception as e:
        yield f"\n\n**System Error:** An unexpected error occurred: {str(e)}"