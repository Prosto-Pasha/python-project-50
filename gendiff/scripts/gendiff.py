import argparse


def parseargs():
    parser = argparse.ArgumentParser(description="Compares two configuration files and shows a difference.")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    options = parser.parse_args()


def main():
    parseargs()


if __name__ == '__main__':
    main()
