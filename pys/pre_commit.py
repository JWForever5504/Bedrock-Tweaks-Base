import os
from json import *
import re


if str(os.getcwd()).endswith("system32"):
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
else:
    doubleclicked = False


from custom_functions import *
check("clrprint") # Check for clrprint module
check("json5","json-five")
import json5
from clrprint import clrprint


stats = [0,0]
incomplete_packs = {"Aesthetic":[],"Colorful Slime":[],"Fixes and Consistency":[],"Fun":[],"HUD and GUI":[],"Lower and Sides":[],"Menu Panoramas":[],"More Zombies":[],"Parity":[],"Peace and Quiet":[],"Retro":[],"Terrain":[],"Unobtrusive":[],"Utility":[],"Variation":[]}
cstats = [0,0]
compatibilities = []

if input("Show Compatibility Progress? [y/n]\n") == "y":
    showcomp = True
else:
    showcomp = False
clrprint("Counting Packs and Compatibilities...",clr="yellow")
# Main Loop
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}","r") as js:
        
        # Load JSON file in jsons\packs\
        try:
            file = loads(js.read())
        except JSONDecodeError as e:
            # When it has an error
            # JSONDecodeError normally prints where I am missing a comma/bracket
            # But not the file, so this brings it up as well
            # Hence why if there is an issue with the JSON, it brings up two errors at once
            clrprint(f"{os.listdir(f'{cdir()}/jsons/packs')[c]} has a skill issue.\n{e}?",clr="red")
            if doubleclicked:
                input("Press enter to exit.")
            exit(1)
    
    # For compatabilities, as it doesn't have a file
    if showcomp:
        clrprint(f'= {file["topic"]}',clr="white") 
    # Runs through the packs
    for i in range(len(file["packs"])):
        # Updates Incomplete Packs
        try:
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default') == []:
                # Adds the packid to the topic list
                incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                stats[1] += 1
            else:
                # When the packid directory has stuff inside
                stats[0] += 1
        except FileNotFoundError:
            # If the packs have not updated with the new directory type
            stats[1] += 1
            incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
        
        
        # Updates Pack Compatibilities
        if file["packs"][i]["compatibility"] != []:
            if showcomp:
                clrprint(f'= \t{file["packs"][i]["pack_id"]}',clr="yellow")
        for comp in range(len(file["packs"][i]["compatibility"])): # If it is empty, it just skips
            # Looks at compatibility folders
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{file["packs"][i]["compatibility"][comp]}') == []:
                if showcomp:
                    clrprint(f'- \t\t{file["packs"][i]["compatibility"][comp]}',clr="red")
                # Adds the packid to the list of incomplete compatibilities
                compatibilities.append(file["packs"][i]["compatibility"])
                cstats[1] += 1
            else:
                if showcomp:
                    clrprint(f'+ \t\t{file["packs"][i]["compatibility"][comp]}',clr="green")
                # When the compatibility directory has something inside
                cstats[0] += 1

clrprint("Finished Counting!",clr="green")
# Update incomplete_packs.json
with open(f"{cdir()}/jsons/others/incomplete_packs.json","w") as incomplete_packs_file:
    incomplete_packs_file.write(dumps(incomplete_packs,indent=2))
clrprint("Updated incomplete_packs.json",clr="green")
clrprint("Updating README.md...",clr="yellow")

# Just some fancy code with regex to update README.md
with open(f"{cdir()}/README.md", "r") as file:
    content = file.read()
# Regex to update link
pack_pattern = r"(https://img.shields.io/badge/Packs-)(\d+%2F\d+)(.*)"
pack_match = re.search(pack_pattern, content)
comp_pattern = r"(https://img.shields.io/badge/Compatibilities-)(\d+%2F\d+)(.*)"
comp_match = re.search(comp_pattern, content)

if pack_match and comp_match:
    # Replace the links using regex
    new_pack_url = f"{pack_match.group(1)}{stats[0]}%2F{stats[0]+stats[1]}{pack_match.group(3)}"
    updated_content = content.replace(pack_match.group(0), new_pack_url)
    new_comp_url = f"{comp_match.group(1)}{cstats[0]}%2F{cstats[0]+cstats[1]}{comp_match.group(3)}"
    updated_content = updated_content.replace(comp_match.group(0), new_comp_url)
    with open(f"{cdir()}/README.md", "w") as file:
        # Update the file
        file.write(updated_content)
else:
    # When the regex fails if I change the link
    raise IndexError("Regex Failed")

clrprint("Updated README.md!",clr="green")
clrprint("Validating JSON Files...",clr="yellow")

# JSON files validator
for root, _, files in os.walk(cdir()):
    for file in files:
        if file.lower().endswith('.json'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json5.load(f)
                    error_message = None
            except Exception as e:
                error_message = str(e)
            
            if error_message:
                # If there's an error, print it and exit with code 1
                print(f"Error in file '{file_path}': {error_message}")
                exit(1)

clrprint("JSON Files are valid!",clr="green")
if doubleclicked:
    clrprint("Press Enter to exit.",clr="green",end="")
    input()