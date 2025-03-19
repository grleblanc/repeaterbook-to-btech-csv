# RepeaterBook to BTech UV-Pro CSV Converter

This Python script converts repeater data from the RepeaterBook API into a CSV file compatible with the BTech UV-Pro programming software.

## Prerequisites

- Python 3.x
- `requests` library (install with `pip install requests`)

## Usage

1.  **Save the script:** Save the Python code as a `.py` file (e.g., `repeaterbook_to_btech.py`).
2.  **Run the script:** Open a terminal or command prompt and run the script with the following arguments:

    ```bash
    python repeaterbook_to_btech.py <output_file> <state_id>
    ```

    - `<output_file>`: Path to the desired output CSV file (e.g., `repeaters.csv`).
    - `<state_id>`: The RepeaterBook state ID for the desired region.

    Example:

    ```bash
    python repeaterbook_to_btech.py repeaters_ohio.csv 33
    ```

    This example will generate a CSV file named `repeaters_ohio.csv` containing repeater data for Ohio (state ID 33).

## RepeaterBook State IDs

You can find the RepeaterBook state IDs on their website or by consulting their API documentation.

## Output CSV Format

The output CSV file is formatted to match the BTech UV-Pro programming software's import requirements. The columns include:

- `title`: Repeater callsign and location (truncated to 16 characters).
- `tx_freq`: Transmitter frequency (9 digits, trailing zeros).
- `rx_freq`: Receiver frequency (9 digits, trailing zeros).
- `tx_sub_audio(CTCSS=freq/DCS=number)`: Transmit CTCSS tone or DCS code (5 digits, trailing zeros).
- `rx_sub_audio(CTCSS=freq/DCS=number)`: Receive CTCSS tone or DCS code (5 digits, trailing zeros).
- `tx_power(H/M/L)`: Transmitter power (default: H).
- `bandwidth(12500/25000)`: Bandwidth (default: 25000).
- `scan(0=OFF/1=ON)`: Scan setting (default: 1).
- `talk around(0=OFF/1=ON)`: Talk around setting (default: 0).
- `pre_de_emph_bypass(0=OFF/1=ON)`: Pre-de-emphasis bypass setting (default: 0).
- `sign(0=OFF/1=ON)`: Sign setting (default: 0).
- `tx_dis(0=OFF/1=ON)`: Transmit disable setting (default: 0).
- `mute(0=OFF/1=ON)`: Mute setting (default: 0).
- `rx_modulation(0=FM/1=AM)`: Receive modulation (default: 0).
- `tx_modulation(0=FM/1=AM)`: Transmit modulation (default: 0).

## Important Notes

- The script requires an internet connection to fetch data from the RepeaterBook API.
- The `User-Agent` header is included in the API request. This is good practice and helps identify your script.
- Frequencies and PL/TSQ codes are padded with trailing zeros to meet the BTech UV-Pro format requirements.
- If the original frequency or PL/TSQ is too long, it will be truncated.
- Please be respectful of RepeaterBook's API usage policies.

## Author

grleblanc

## License

MIT License
