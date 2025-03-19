"""repeaterbook_to_btech.py - A utility to convert RepeaterBook API data to BTech UV-Pro CSV."""
import csv
import argparse
import requests

def convert_repeaterbook_api_to_btech(output_file, state_id):
    """
    Converts repeater data from the RepeaterBook API to a BTech UV-Pro CSV file.

    Args:
        output_file (str): Path to the output BTech UV-Pro CSV file.
        state_id (int): RepeaterBook state ID.
    """

    api_url = f"https://www.repeaterbook.com/api/export.php?state_id={state_id}"
    headers = {"User-Agent": "repeater-to-btech-csv/1.0"}

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if data and data['results']:
            repeaters = data['results']

            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                fieldnames = [
                    'title', 'tx_freq', 'rx_freq', 'tx_sub_audio(CTCSS=freq/DCS=number)',
                    'rx_sub_audio(CTCSS=freq/DCS=number)', 'tx_power(H/M/L)', 'bandwidth(12500/25000)',
                    'scan(0=OFF/1=ON)', 'talk around(0=OFF/1=ON)', 'pre_de_emph_bypass(0=OFF/1=ON)',
                    'sign(0=OFF/1=ON)', 'tx_dis(0=OFF/1=ON)', 'mute(0=OFF/1=ON)',
                    'rx_modulation(0=FM/1=AM)', 'tx_modulation(0=FM/1=AM)'
                ]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for repeater in repeaters:
                    # Format frequency to 9 digits with trailing zeros
                    frequency = repeater.get('Frequency', '').strip()
                    frequency = frequency.replace(".", "")
                    if len(frequency) == 7:
                        frequency = "0"+frequency + "00"
                    else:
                        frequency = frequency.ljust(9, '0')

                    # Format input frequency to 9 digits with trailing zeros
                    input_frequency = repeater.get('Input Freq', '').strip()
                    input_frequency = input_frequency.replace(".", "")
                    if len(input_frequency) == 7:
                        input_frequency = "0"+input_frequency + "00"
                    else:
                        input_frequency = input_frequency.ljust(9, '0')

                    # Format PL/TSQ to 5 digits with trailing zeros
                    pl = repeater.get('PL', '').strip().replace(".", "").ljust(5, '0')
                    tsq = repeater.get('TSQ', '').strip().replace(".", "").ljust(5, '0')

                    # Extract other repeater data
                    callsign = repeater.get('Callsign', '').strip()
                    city = repeater.get('Nearest City', '').strip()
                    state = repeater.get('State', '').strip()

                    # Set tx/rx sub-audio (CTCSS/DCS)
                    tx_sub_audio = pl
                    rx_sub_audio = tsq

                    # Construct channel name
                    channel_name = f"{callsign} {city}, {state}" if city and state else callsign
                    if not channel_name:
                        channel_name = frequency

                    writer.writerow({
                        'title': channel_name[:16],
                        'tx_freq': frequency,
                        'rx_freq': input_frequency,
                        'tx_sub_audio(CTCSS=freq/DCS=number)': tx_sub_audio,
                        'rx_sub_audio(CTCSS=freq/DCS=number)': rx_sub_audio,
                        'tx_power(H/M/L)': 'H',
                        'bandwidth(12500/25000)': '25000',
                        'scan(0=OFF/1=ON)': '1',
                        'talk around(0=OFF/1=ON)': '0',
                        'pre_de_emph_bypass(0=OFF/1=ON)': '0',
                        'sign(0=OFF/1=ON)': '0',
                        'tx_dis(0=OFF/1=ON)': '0',
                        'mute(0=OFF/1=ON)': '0',
                        'rx_modulation(0=FM/1=AM)': '0',
                        'tx_modulation(0=FM/1=AM)': '0'
                    })

            print(f"Conversion successful. Output saved to {output_file}")

        else:
            print("No repeaters found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from RepeaterBook API: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert RepeaterBook API data to BTech UV-Pro CSV.")
    parser.add_argument("output_file", help="Path to the output BTech UV-Pro CSV file.")
    parser.add_argument("state_id", type=int, help="RepeaterBook state ID.")
    args = parser.parse_args()

    convert_repeaterbook_api_to_btech(args.output_file, args.state_id)