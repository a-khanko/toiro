from aii_python_seu_clients.hermes.client import HermesClient
HERMES_URL = 'https://hermes-production.us2.turnitin.com'

hermes_client = HermesClient(HERMES_URL)

def convert_offset_byte_to_char(byte_array, byte_index):
    bytes_up_to_index = byte_array[:byte_index]
    text_as_string = bytes_up_to_index.decode('utf-8', errors='replace')
    char_offset = len(text_as_string)
    return char_offset


def get_word_offsets(doc_bytes: bytes, diff: list[int]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    num_sentences = len(diff) // 2
    offsets_char = []
    offsets_byte = []
    start = end = 0
    for i in range(num_sentences):
        start = end + diff[2 * i]
        end = start + diff[2 * i + 1]
        offsets_byte.append((start, end))

        start_char = convert_offset_byte_to_char(doc_bytes, start)
        end_char = convert_offset_byte_to_char(doc_bytes, end)
        offsets_char.append((start_char, end_char))
    return offsets_char, offsets_byte


def tokenize(text):
    """
    A method for word segmentation.

    Parameters
    ----------
    text : str
        An input text

    Returns
    -------
    words : list
        A list of words
    """
    encoded_text = text.encode('utf-8')
    output = hermes_client.language_tool(text=encoded_text, language='ja')
    diffs = output.words.token_diffs
    offsets_char, _ = get_word_offsets(encoded_text, diffs)
    words = [text[el[0]:el[1]] for el in offsets_char]
    return words


def original_usage(text):
    encoded_text = text.encode('utf-8')
    output = hermes_client.language_tool(text=encoded_text, language='ja')
    return output