def refine_text(text):
    text = text.strip()

    # Capitalize
    if len(text) > 0:
        text = text[0].upper() + text[1:]

    # Add punctuation if missing
    if text and text[-1] not in ".!?":
        text += "."

    return text


def split_text_into_lines(text, max_chars=40):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def format_subtitle_text(text):
    lines = split_text_into_lines(text)

    # Max 2 lines per subtitle
    if len(lines) <= 2:
        return "\n".join(lines)

    # If more than 2 lines, merge smartly
    merged = []
    temp = ""

    for line in lines:
        if len(temp + " " + line) <= 40:
            temp += (" " if temp else "") + line
        else:
            merged.append(temp)
            temp = line

    if temp:
        merged.append(temp)

    return "\n".join(merged[:2])  # strictly 2 lines


def segment_transcript(transcript_data):
    segmented = []

    for segment in transcript_data:
        refined = refine_text(segment["text"])
        formatted = format_subtitle_text(refined)

        segmented.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": formatted
        })

    return segmented