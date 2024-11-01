import re
from typing import List, Tuple


def split_by_timestamps(text) -> List[str]:
    """
    Splits the input text by timestamps and returns a list of segments.

    :param text: The input text containing timestamps and words/phrases. The timestamps are of the form
        [t1.23] where the float value is in seconds.
    :return: A list of text segments split by timestamps.
    """
    # Match fully formed timestamps or escaped timestamps
    segments = re.split(r'(\[t\d+\.\d+\])|(\\\[t\d+\.\d+\])', text)
    return [seg for seg in segments if seg]


def interpolate_timestamps(words, start_time, end_time) -> List[Tuple[str, float, float]]:
    """
    Interpolates timestamps for a list of words evenly between start_time and end_time.

    :param words: List of words to timestamp.
    :param start_time: The start time for the first word.
    :param end_time: The end time for the last word.
    :return: A list of tuples where each tuple contains a word and its corresponding start and end time.
    """
    num_words = len(words)
    if num_words == 1:
        return [(words[0], start_time, end_time)]

    step = (end_time - start_time) / num_words
    interpolated = []

    for i in range(num_words):
        word_start = start_time + i * step
        word_end = word_start + step
        interpolated.append((words[i], word_start, word_end))

    return interpolated


def parse_timecoded_text(text) -> List[Tuple[str, float, float]]:
    """
    Parses the time-coded text and interpolates timestamps for each word based on the provided time codes.

    :param text: The input text containing words and timecodes of the form [t1.23] where the float value is in seconds.
    :return: A list of tuples where each tuple contains a word and its corresponding start and end time.
    """
    segments = split_by_timestamps(text)
    parsed_output = []
    current_words = []
    last_timestamp = 0.0
    bad_timestamp_flag = False
    total_time = 0.0
    total_words = 0

    for segment in segments:
        if segment.startswith('\\[t'):  # Escaped timestamp, treat as normal text
            current_words.append(segment.replace('\\', ''))
        elif segment.startswith('[t'):  # Timestamp
            current_time = float(segment[2:-1])
            if current_time < last_timestamp:
                current_time = last_timestamp
                bad_timestamp_flag = True

            if current_words:
                word_count = len(current_words)
                time_interval = current_time - last_timestamp

                # Update the total time and total words count
                total_time += time_interval
                total_words += word_count

                parsed_output.extend(interpolate_timestamps(current_words, last_timestamp, current_time))
                current_words = []

            last_timestamp = current_time
        else:  # Regular text
            # Tokenize the segment into words
            words = segment.split()
            current_words.extend(words)

    if current_words:
        # If there are remaining words without a timestamp, use average seconds per word for interpolation
        average_time_per_word = total_time / total_words if total_words > 0 else 2.0
        final_time = last_timestamp + average_time_per_word * len(current_words)
        parsed_output.extend(interpolate_timestamps(current_words, last_timestamp, final_time))

    if bad_timestamp_flag:
        print("Warning: Some timestamps were adjusted to prevent backward time travel.")

    return parsed_output


def print_parsed_data(parsed_data) -> None:
    """
    Prints the parsed data in a formatted manner.

    :param parsed_data: A list of tuples where each tuple contains a word, its start time, and its end time.
    """
    for word, start_time, end_time in parsed_data:
        print(f"Word: '{word}', Start Time: {start_time:.2f}s, End Time: {end_time:.2f}s")


if __name__ == "__main__":
    # Test Case 1: Beginning, ending, and every word has a timestamp
    print("Test Case 1: All words have timestamps")
    timecoded_text_1 = "[t0.0]The [t0.5]quick [t1.0]brown [t1.5]fox [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_1 = parse_timecoded_text(timecoded_text_1)
    print(parsed_data_1)
    print("-" * 40)


    # Test Case 2: Beginning missing a timestamp
    print("Test Case 2: Beginning missing a timestamp")
    timecoded_text_2 = "The [t0.5]quick [t1.0]brown [t1.5]fox [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_2 = parse_timecoded_text(timecoded_text_2)
    print(parsed_data_2)
    print("-" * 40)

    # Test Case 3: Ending missing a timestamp
    print("Test Case 3: Ending missing a timestamp")
    timecoded_text_3 = "[t0.0]The [t0.5]quick [t1.0]brown [t1.5]fox [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy dog."
    parsed_data_3 = parse_timecoded_text(timecoded_text_3)
    print(parsed_data_3)
    print("-" * 40)

    # Test Case 4: Beginning missing a timestamp for more than one word without timestamps
    print("Test Case 4: Beginning missing a timestamp for multiple words")
    timecoded_text_4 = "The quick brown [t1.5]fox [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_4 = parse_timecoded_text(timecoded_text_4)
    print(parsed_data_4)
    print("-" * 40)

    # Test Case 5: Ending missing a timestamp with more than one word without timestamps preceding
    print("Test Case 5: Ending missing a timestamp for multiple words")
    timecoded_text_5 = "[t0.0]The [t0.5]quick [t1.0]brown [t1.5]fox [t2.0]jumps over the lazy dog."
    parsed_data_5 = parse_timecoded_text(timecoded_text_5)
    print(parsed_data_5)
    print("-" * 40)

    # Test Case 6: Missing spaces
    print("Test Case 6: Some missing spaces")
    timecoded_text_5 = "[t0.0]The[t0.5]quick[t1.0]brown [t1.5]fox [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_5 = parse_timecoded_text(timecoded_text_5)
    print(parsed_data_5)
    print("-" * 40)

    # Test Case 7: Reference
    print("Test Case 7: Reference")
    timecoded_text_1 = "[t0.0]The [t0.5]quick [t1.0]brown [t1.5]fox [t1.75][2] [t2.0]jumps [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_1 = parse_timecoded_text(timecoded_text_1)
    print(parsed_data_1)
    print("-" * 40)

    # Test Case 8: Escaped
    print("Test Case 8: Escaped")
    timecoded_text_1 = "[t0.0]The [t0.5]quick [t1.0]brown [t1.5]fox \[t1.75] [t2.0]jumps\[t99.9] [t2.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_1 = parse_timecoded_text(timecoded_text_1)
    print(parsed_data_1)
    print("-" * 40)

    # Test Case 9: Broken
    print("Test Case 8: Broken")
    timecoded_text_1 = "[t0.0][t0.2]The [t0.5]quick [t1.0]brown [t1.5]fox \[t1.75 [t2.0]jumps [t99.9 [t1.5]over [t3.0]the [t3.5]lazy [t4.0]dog.[t4.5]"
    parsed_data_1 = parse_timecoded_text(timecoded_text_1)
    print(parsed_data_1)
    print("-" * 40)

    # Test Case 10: Empty
    print("Test Case 8: Empty")
    timecoded_text_1 = ""
    parsed_data_1 = parse_timecoded_text(timecoded_text_1)
    print(parsed_data_1)
    print("-" * 40)