
# Import the fuzzy string matching library
from thefuzz import fuzz

def find_similar_names(input_name, name_list):
    """
    Finds and ranks similar names from a list based on a similarity score.

    Args:
        input_name (str): The name entered by the user.
        name_list (list): A list of names to search through.

    Returns:
        tuple: A tuple containing the best match (tuple) and a ranked list
               of all matches (list of tuples).
    """
    matches = []
    # Convert input name to lowercase for case-insensitive comparison
    input_name_lower = input_name.lower()
    
    # Calculate similarity score for each name in the dataset
    for name in name_list:
        score = fuzz.ratio(input_name_lower, name.lower())
        matches.append((name, score))
    
    # Sort the list of matches in descending order based on the score
    ranked_matches = sorted(matches, key=lambda x: x[1], reverse=True)
    
    # The best match is the first item in the sorted list
    best_match = ranked_matches[0]
    
    return best_match, ranked_matches



# Step 1: Data Preparation
name_dataset = [
    "Geetha", "Gita", "Gitu", "Geeta",
    "Priya", "Pria", "Priyah",
    "Vikram", "Vickram", "Bikram",
    "Siddharth", "Siddarth", "Sidharth", "Sidarth",
    "Mohammed", "Mohamed", "Mohammad", "Muhammad", "Mohamad",
    "Lakshmi", "Laxmi", "Lakshmy",
    "Aishwarya", "Aishwariya", "Ashwarya", "Aiswarya",
    "Rajeev", "Rajiv", "Rajib",
    "Karthik", "Kartik", "Karthick",
    "Anjali", "Anjaly"
]

# Step 2: Get user input
user_name = input("Enter a name to find matches: ")

# Step 3: Find the best and all ranked matches
best_match_result, all_matches_ranked = find_similar_names(user_name, name_dataset)

# --- Expected Output ---

# Display the best match
print("\n" + "="*30)
print("**Best Match**")
print(f"Name: {best_match_result[0]}")
print(f"Similarity Score: {best_match_result[1]}")
print("="*30 + "\n")


# Display the ranked list of all matches
print(" Ranked List of All Matches ")
for name, score in all_matches_ranked:
    print(f"- {name}: {score}")