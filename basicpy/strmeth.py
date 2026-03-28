def censor(message, banned_words):
    """Replace each banned word in message with '***'."""
    for word in banned_words:
        message.replace(word, "***")  # BUG: return value discarded; strings are immutable
    return message


if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog"
    banned = ["quick", "lazy"]
    result = censor(text, banned)
    print(f"Result:   {result}")
    print(f"Expected: The *** brown fox jumps over the *** dog")
