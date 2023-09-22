import json
import glob

def load_json_file(file_path):
    with open(file_path) as userFile:
        return json.load(userFile)

def filter_houses(parseJson, keys_to_keep):
    modified_houses = []
    for house in parseJson['SearchResults']:
        modified_house = {}
        for key in keys_to_keep:
            if key in house:
                modified_house[key] = house[key]
        modified_houses.append(modified_house)
    return modified_houses

def save_filtered_json(filtered_json, output_file):
    with open(output_file, 'w') as f:
        json.dump(filtered_json, f)

def count_files(pattern):
    count = len(glob.glob(pattern))
    return count

def parse_json(count):
    for i in range(count):
        input_file = f"results_{i}.json"
        parseJson = load_json_file(input_file)
        modified_houses = filter_houses(parseJson, keys_to_keep)
        filtered_json = {'SearchResults': modified_houses}
        save_filtered_json(filtered_json, output_file)

pattern = "results_*"
count = count_files(pattern)
output_file = 'filtered_data.json'
keys_to_keep = ['DisplayAddress', 'PriceAsString', 'BedsString', 'SeoUrl', 'MainPhoto', 'Photos']

parse_json(count)


