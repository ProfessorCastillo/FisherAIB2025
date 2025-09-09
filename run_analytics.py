import json
from collections import Counter

def analyze_presentations(filename='AIB_presentation_list.json'):
    """
    Reads presentation data from a JSON file and prints analytics,
    separating presenter and co-author affiliations.

    Args:
        filename (str): The name of the JSON file to analyze.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            presentations = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure the script and the JSON file are in the same directory.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. Please check the file format.")
        return

    # --- 1. Total Number of Presentations ---
    total_presentations = len(presentations)

    # --- 2. Separate Affiliation Lists ---
    presenter_affiliations = []
    coauthor_affiliations = []

    for pres in presentations:
        # A. Add the presenter's affiliation to the presenter list
        if pres.get('presenter_affiliation'):
            presenter_affiliations.append(pres['presenter_affiliation'])

        # B. Identify the presenter's full name to distinguish them from co-authors
        p_fname = pres.get('presenter_first_name', '')
        p_lname = pres.get('presenter_last_name', '')
        # Use strip() to handle any accidental whitespace
        presenter_full_name = f"{p_fname} {p_lname}".strip()

        # C. Loop through all authors to find co-authors
        if 'authors' in pres and pres['authors']:
            for author in pres['authors']:
                author_name = author.get('name', '').strip()
                
                # If the author's name doesn't match the presenter's, they are a co-author
                if author_name != presenter_full_name:
                    affiliation = author.get('affiliation')
                    # Ensure the affiliation exists and is not a placeholder
                    if affiliation and affiliation.lower() != 'n/a':
                        coauthor_affiliations.append(affiliation)

    # Count and get the top 20 for each list
    presenter_affiliation_counts = Counter(presenter_affiliations)
    top_20_presenter_affiliations = presenter_affiliation_counts.most_common(20)

    coauthor_affiliation_counts = Counter(coauthor_affiliations)
    top_20_coauthor_affiliations = coauthor_affiliation_counts.most_common(20)

    # --- 3. Counts of Disciplines ---
    all_disciplines = [pres.get('cleaned_discipline', 'Not Specified') for pres in presentations]
    discipline_counts = Counter(all_disciplines)
    sorted_discipline_counts = discipline_counts.most_common()


    # --- Print the final report ---
    print("=" * 50)
    print("      AI in Business Conference Analytics")
    print("=" * 50)
    print(f"\nTotal Number of Presentations: {total_presentations}\n")

    print("-" * 50)
    print("Top 20 Presenter Affiliations")
    print("-" * 50)
    if top_20_presenter_affiliations:
        for i, (affiliation, count) in enumerate(top_20_presenter_affiliations, 1):
            print(f"{i:2}. {affiliation}: {count} presenters")
    else:
        print("No presenter affiliation data found.")
    print("\n")

    print("-" * 50)
    print("Top 20 Co-author Affiliations")
    print("-" * 50)
    if top_20_coauthor_affiliations:
        for i, (affiliation, count) in enumerate(top_20_coauthor_affiliations, 1):
            print(f"{i:2}. {affiliation}: {count} co-authors")
    else:
        print("No co-author affiliation data found.")
    print("\n")

    print("-" * 50)
    print("Presentation Counts by Discipline")
    print("-" * 50)
    if sorted_discipline_counts:
        max_len = max(len(discipline) for discipline, count in sorted_discipline_counts)
        for discipline, count in sorted_discipline_counts:
            print(f"{discipline:<{max_len}} : {count}")
    else:
        print("No discipline data found.")
    print("\n")


if __name__ == "__main__":
    analyze_presentations()
