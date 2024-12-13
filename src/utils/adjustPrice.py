# Copyright (c) 2024 bilive.

import xml.etree.ElementTree as ET
import argparse

def update_sc_prices(file_path):
    """Adjust the price of sc and guard, see this:
            https://github.com/hihkm/DanmakuFactory/issues/53
    Args:
        file_path: str, the path of xml danmaku file
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate over all 'sc' elements
    for sc in root.findall('sc'):
        # Get the current price
        price = sc.get('price')
        if int(price) > 10000:
            # Convert price to integer, divide by 1000, and update the attribute
            new_price = int(price) / 1000
            sc.set('price', str(int(new_price)))

    for guard in root.findall('guard'):
        # Get the current price
        price_guard = guard.get('price')
        if int(price_guard) > 10000:
            # Convert price to integer, divide by 1000, and update the attribute
            new_price_guard = int(price_guard) / 1000
            guard.set('price', str(int(new_price_guard)))
    
    for toast in root.findall('toast'):
        # Get the current price
        price_toast = toast.get('price')
        if int(price_toast) > 10000:
            # Convert price to integer, divide by 1000, and update the attribute
            new_price_toast = int(price_toast) / 1000
            toast.set('price', str(int(new_price_toast)))

    # Remove 'gift' elements with price less than 1000
    for gift in root.findall('gift'):
        price_gift = gift.get('price')
        if int(price_gift) < 1000:
            root.remove(gift)

    # Write the updated XML back to the file
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Update sc prices in an XML file.')
    parser.add_argument('file_path', type=str, help='Path to the XML file')

    # Parse the arguments
    args = parser.parse_args()

    # Update sc prices
    update_sc_prices(args.file_path)

if __name__ == '__main__':
    main()