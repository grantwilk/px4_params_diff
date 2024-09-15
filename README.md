# PX4 Parameter Diff

This script compares two PX4 `.params` files and exports the differences to a CSV file.

## Usage

```sh
python px4_params_diff.py <file1> <file2> <output_file> [--common-only]
```

### Arguments

- **file1**: The first `.params` file to compare.
- **file2**: The second `.params` file to compare.
- **output_file**: The output CSV file to save the differences.
- **--common-only**: Only compare parameters in common between the files.

## Example

```sh
python px4_params_diff.py config1.params config2.params diff_output.csv --common-only
```

## Requirements

- Python 3.x

## License

This project is licensed under the MIT License.





























