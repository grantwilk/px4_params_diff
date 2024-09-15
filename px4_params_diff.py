"""
This script compares two PX4 .params files and exports the differences to a CSV file.

Usage:
    python px4_params_diff.py <file1> <file2> <output_file> [--common-only]

Arguments:
    file1: The first .params file to compare.
    file2: The second .params file to compare.
    output_file: The output CSV file to save the differences.
    --common-only: Only compare parameters in common between the files.
"""

import argparse
import csv


def parse_params(file_path):
    """
    Parse the parameters from a PX4 .params file.

    Args:
        file_path (str): The path to the .params file.

    Returns:
        dict: A dictionary with parameter names as keys and their values as values.
    """
    params = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) != 5:
                continue
            _, _, name, value, _ = parts
            params[name] = value
    return params


def compare_params(params1, params2, common_only):
    """
    Compare two sets of parameters.

    Args:
        params1 (dict): The first set of parameters.
        params2 (dict): The second set of parameters.
        common_only (bool): If True, only compare parameters that are common between the two sets.

    Returns:
        list: A list of tuples containing the parameter name, value in the first set, and value in
              the second set for parameters that differ.
    """
    if common_only:
        keys_to_compare = set(params1.keys()).intersection(set(params2.keys()))
    else:
        keys_to_compare = set(params1.keys()).union(set(params2.keys()))

    differences = []
    for key in keys_to_compare:
        value1 = params1.get(key, "N/A")
        value2 = params2.get(key, "N/A")
        if value1 != value2:
            differences.append((key, value1, value2))
    return differences


def export_to_csv(differences, output_file):
    """
    Export the differences to a CSV file.

    Args:
        differences (list): A list of tuples containing the parameter name, value in the first set,
                            and value in the second set for parameters that differ.
        output_file (str): The path to the output CSV file.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["PARAMETER", "FILE1_VALUE", "FILE2_VALUE"])
        for key, value1, value2 in differences:
            csvwriter.writerow([key, value1, value2])


def main(file1, file2, output_file, common_only):
    """
    Main function to compare two PX4 .params files and export the differences to a CSV file.

    Args:
        file1 (str): The path to the first .params file.
        file2 (str): The path to the second .params file.
        output_file (str): The path to the output CSV file.
        common_only (bool): If True, only compare parameters that are common between the two files.
    """
    params1 = parse_params(file1)
    params2 = parse_params(file2)
    differences = compare_params(params1, params2, common_only)

    if differences:
        export_to_csv(differences, output_file)
        print(f"Differences exported to {output_file}")
    else:
        print("No differences found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare two PX4 .params files and export differences to a CSV file."
    )
    parser.add_argument("file1", type=str, help="The first .params file to compare.")
    parser.add_argument("file2", type=str, help="The second .params file to compare.")
    parser.add_argument(
        "output_file", type=str, help="The output CSV file to save the differences."
    )
    parser.add_argument(
        "--common-only",
        action="store_true",
        help="Only compare parameters in common between the files.",
    )

    args = parser.parse_args()
    main(args.file1, args.file2, args.output_file, args.common_only)
