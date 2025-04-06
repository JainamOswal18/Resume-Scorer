import ollama
from agents import score_resume, score_with_ollama

def test_ollama_direct():
    """Test direct ollama API call"""
    try:
        response = ollama.generate(model='openhermes', prompt='Hello, how are you?')
        print("\n--- Direct Ollama Response ---")
        print(response['response'])
        return True
    except Exception as e:
        print(f"Error calling Ollama directly: {e}")
        return False

def test_score_with_ollama():
    """Test our custom scoring function"""
    try:
        response = score_with_ollama("What is the capital of France?")
        print("\n--- score_with_ollama Response ---")
        print(response)
        return True
    except Exception as e:
        print(f"Error using score_with_ollama: {e}")
        return False

def test_resume_scoring():
    """Test the score_resume function with a sample resume"""
    try:
        sample_resume = "Experienced Data Scientist with 3 years of experience in machine learning and Python. Skills include TensorFlow, PyTorch, and pandas. Master's degree in Computer Science."
        sample_job_description = "Looking for a Data Scientist with Python and ML experience. Master's degree preferred."
        sample_links = ["https://github.com/jainamoswal18/"]
        
        result = score_resume(sample_resume, sample_job_description, sample_links)
        print("\n--- Resume Scoring Result ---")
        print(result)
        return True
    except Exception as e:
        print(f"Error using score_resume: {e}")
        return False

if __name__ == "__main__":
    print("Testing Ollama direct integration...")
    
    print("\n1. Testing direct Ollama API...")
    test_ollama_direct()
    
    print("\n2. Testing score_with_ollama...")
    test_score_with_ollama()
    
    print("\n3. Testing resume scoring...")
    test_resume_scoring()
    
    print("\nTests completed!") 