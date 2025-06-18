from app.llm_integration import query_llm
from app.detection import analyze_output
from app.database import init_db, log_interaction

if __name__ == "__main__":
    # Initialize the database (creates table if not exists)
    init_db()

    # Get user input
    prompt = input("Enter your prompt: ")
    model = input("Choose model ('gemma' or 'openai'): ").strip()
    response = query_llm(prompt, model)
    print(f"\nResponse from {model}:\n{response}")

    # Analyze the response for bias/threats
    issues = analyze_output(response)
    if issues:
        print("\n[!] Issues detected:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\nNo bias or threat detected.")

    # Log the interaction to the database
    log_interaction(prompt, response, issues, model)
    print("\n[+] Interaction logged.")
