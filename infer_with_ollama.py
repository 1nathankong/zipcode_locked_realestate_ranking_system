import json
import subprocess

# Load top 10 listings
with open("ranked_by_composite_score_under700k.json", "r", encoding="utf-8") as f:
    listings = json.load(f)[:10]

# Build LLM prompt
prompt = "You're an Austin-based real estate advisor for tech professionals.\n"
prompt += "Evaluate these 10 properties for long-term ROI, tech location appeal, and livability:\n\n"

for i, home in enumerate(listings, 1):
    prompt += (
        f"{i}. Address: {home.get('streetAddress', 'Unknown')}, "
        f"ZIP: {home.get('zipcode')}, Price: ${home.get('price')}, "
        f"Driveability: {home.get('driveabilityScore')}, "
        f"Location: {home.get('customLocationScore')}, "
        f"Composite: {home.get('compositeScore')}\n"
    )

prompt += "\nPick the top 3 homes, justify your picks, and suggest what kind of buyer they suit best.\n"

# Run Ollama with Gemma 2B
process = subprocess.run(
    ["ollama", "run", "gemma:2b"],
    input=prompt.encode("utf-8"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Save output to file
output_file = "llm_inference_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(process.stdout.decode("utf-8"))

print(f"Inference completed using Gemma 2B — saved to {output_file}")
