import re

# Regular expression to match UniProt accession IDs
acc_regex = re.compile("(?P<accession>[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})(?P<isotype>-\d+)?")
# Regular expression to match position and residue
reg_positon_residue = re.compile("_(\w)(\d+)")


def replace_special_with_dot(s: str) -> str:
    """
    Replace special characters in a string with dots.

    :param s: Input string.
    :return: String with special characters replaced by dots.
    """
    return re.sub(r'[^a-zA-Z0-9.]', '.', s)


def read_fasta(fasta_file: str) -> dict[str, str]:
    """
    Read a FASTA file into a dictionary where the key is the UniProt accession ID.

    :param fasta_file: Content of the FASTA file as a string.
    :return: Dictionary with accession IDs as keys and sequences as values.
    """
    fasta_dict = {}

    current_acc = ""
    for line in fasta_file.split("\n"):
        line = line.strip()
        if line.startswith('>'):
            match = acc_regex.search(line.replace(">", ""))
            if match:
                acc = match.groupdict(default="")["accession"]
                iso = match.groupdict(default="")["isotype"]
                fasta_dict[acc+iso] = ""
                current_acc = acc+iso
            else:
                fasta_dict[line.replace(">", "")] = ""
                current_acc = line.replace(">", "")
        else:
            fasta_dict[current_acc] += line
    return fasta_dict


def detect_delimiter_from_extension(file_name: str) -> str:
    """
    Detect the delimiter based on the file extension.

    :param file_name: Name of the file.
    :return: Delimiter character.
    """
    if file_name.endswith(".tsv"):
        return "\t"
    elif file_name.endswith(".csv"):
        return ","
    else:
        return "\t"