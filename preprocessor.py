import re
import pandas as pd


def _parse_whatsapp_datetime(dt_series):
    # Explicitly support both 12-hour and 24-hour exports.
    formats = [
        "%d/%m/%y, %I:%M %p",
        "%d/%m/%Y, %I:%M %p",
        "%d/%m/%y, %I:%M:%S %p",
        "%d/%m/%Y, %I:%M:%S %p",
        "%d/%m/%y, %H:%M",
        "%d/%m/%Y, %H:%M",
        "%d/%m/%y, %H:%M:%S",
        "%d/%m/%Y, %H:%M:%S",
    ]

    cleaned = (
        dt_series.astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    parsed = pd.Series(pd.NaT, index=cleaned.index, dtype="datetime64[ns]")

    for fmt in formats:
        mask = parsed.isna()
        if not mask.any():
            break
        parsed.loc[mask] = pd.to_datetime(cleaned.loc[mask], format=fmt, errors="coerce")

    # Fallback parser for uncommon locale variants.
    mask = parsed.isna()
    if mask.any():
        parsed.loc[mask] = pd.to_datetime(cleaned.loc[mask], errors="coerce", dayfirst=True)

    return parsed


def preprocess(data):
    # Supports common WhatsApp export formats:
    # 1) 12/5/23, 9:41 pm - Name: message
    # 2) [12/5/23, 9:41:02 pm] Name: message
    # 3) 12/5/2023, 21:41 - Name: message
    line_pattern = re.compile(
        r'^'
        r'(?:\[(?P<dt_bracket>[^\]]+)\]|(?P<dt_plain>\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AaPp][Mm])?))'
        r'(?:\s-\s|\s)'
        r'(?P<rest>.*)$'
    )

    rows = []
    current = None

    for raw_line in data.splitlines():
        match = line_pattern.match(raw_line)
        if match:
            if current is not None:
                rows.append(current)

            dt_text = (match.group("dt_bracket") or match.group("dt_plain") or "").strip()
            rest = (match.group("rest") or "").strip()
            current = {"message_date": dt_text, "user_message": rest}
        else:
            # Multiline message: append to previous message body.
            if current is not None:
                current["user_message"] = f"{current['user_message']}\n{raw_line}".strip()

    if current is not None:
        rows.append(current)

    if not rows:
        raise ValueError(
            "Could not parse chat file. Please export chat again in WhatsApp text format."
        )

    df = pd.DataFrame(rows)

    df["date"] = _parse_whatsapp_datetime(df["message_date"])
    df = df.dropna(subset=["date"]).copy()

    if df.empty:
        raise ValueError(
            "Could not parse dates in chat file. Try a different WhatsApp export."
        )

    users = []
    messages_clean = []

    for message in df["user_message"]:
        entry = re.split(r"^([^:]+):\s", message, maxsplit=1)
        if len(entry) >= 3:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append("group_notification")
            messages_clean.append(entry[0] if entry else "")

    df["user"] = users
    df["message"] = messages_clean
    df.drop(columns=["user_message", "message_date"], inplace=True)

    df["year"] = df["date"].dt.year
    df["only_date"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df["hour"]:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df["period"] = period
    return df