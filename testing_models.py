import gzip
import random
from n_gram import Ngram
from backoff import Backoff
from weighted import LearnedWeighted
from utils import run_model
import numpy as np


def get_from(start, size):
    enwik = open('files/enwik9', 'rb')
    enwik.seek(start)
    data = enwik.read(size)
    enwik.close()
    return data


# random data from enwik9
def get_random_enwik(size):
    start = random.randint(0, int(1e9))
    data = get_from(start, size)
    return data


def get_zip_results(starts, size):
    zip_sizes = []
    for i in range(len(starts)):
        data = get_from(starts[i], size)
        zip_out = gzip.compress(data)
        zip_sizes.append(len(zip_out))
    avg_zip_size = sum(zip_sizes) / len(zip_sizes)
    return avg_zip_size


def get_model_results(model, starts, size):
    compressed_sizes = []
    theoretical_compressions = []
    for i in range(len(starts)):
        data = get_from(starts[i], size)
        compressed_size, theoretical_compression = run_model(model, data)
        compressed_sizes.append(compressed_size)
        theoretical_compressions.append(theoretical_compression)
    avg_compressed_size = sum(compressed_sizes) / len(compressed_sizes)
    avg_theoretical_compression = sum(theoretical_compressions) / len(theoretical_compressions)
    return avg_compressed_size, avg_theoretical_compression


def format_into_table(model_results):
    # format the dictionary into a markdown table
    table = "| Model | Compressed Size | Theoretical Compression |\n"
    table += "| --- | --- | --- |\n"
    for model_name, results in model_results.items():
        table += f"| {model_name} | {results[0]} | {results[1]} |\n"
    return table


def update_readme(table, description):
    new_results_section = description + '\n' + table

    # Read the current content of the README file
    with open('README.md', 'r') as readme:
        readme_content = readme.read()

    # Find the start and end indices of the "Results" section
    start_marker = "Results:"

    start_index = readme_content.find(start_marker)

    if start_index != -1:
        # Replace the existing "Results" section with the new content
        updated_readme_content = (
                readme_content[:start_index] + new_results_section
        )

        # Write the updated content back to the README file
        with open('README.md', 'w') as readme:
            readme.write(updated_readme_content)



if __name__ == "__main__":
    size = int(1e3)
    n_tests = 5
    n = 16
    starts = np.random.randint(0, int(1e9), n_tests)
    model_results = dict()

    zip_size = get_zip_results(starts, size)
    model_results['zip'] = [zip_size, 'N/A']

    model = Ngram(n)
    c, t = get_model_results(model, starts, size)
    model_results[f'Ngram_{n}'] = [c, t]

    model = Backoff(n)
    c, t = get_model_results(model, starts, size)
    model_results[f'Backoff_{n}'] = [c, t]

    model = LearnedWeighted(n)
    c, t = get_model_results(model, starts, size)
    model_results[f'LearnedWeighted_{n}'] = [c, t]

    table = format_into_table(model_results)
    description = f'Results: \n\n averaged on {n_tests} random samples of {size} bytes from enwik9\n'
    update_readme(table, description)
