def generate_human_output(
    info_by_park_id, start_date, end_date, gen_campsite_info=False
):
    out = []
    has_availabilities = False
    for park_id, info in info_by_park_id.items():
        current, maximum, available_dates_by_site_id, park_name = info
        if current:
            emoji = Emoji.SUCCESS.value
            has_availabilities = True
        else:
            emoji = Emoji.FAILURE.value

        out.append(
            "{emoji} {park_name} ({park_id}): {current} site(s) available out of {maximum} site(s)".format(
                emoji=emoji,
                park_name=park_name,
                park_id=park_id,
                current=current,
                maximum=maximum,
            )
        )

        # Displays campsite ID and availability dates.
        if gen_campsite_info and available_dates_by_site_id:
            for site_id, dates in available_dates_by_site_id.items():
                out.append(
                    "  * Site {site_id} is available on the following dates:".format(
                        site_id=site_id
                    )
                )
                for date in dates:
                    out.append(
                        "    * {start} -> {end}".format(
                            start=date["start"], end=date["end"]
                        )
                    )
                # Log site number for Telegram bot script to detect
                out.append("SITE_AVAILABLE: {site_id}".format(site_id=site_id))

    if has_availabilities:
        out.insert(
            0,
            "there are campsites available from {start} to {end}!!!".format(
                start=start_date.strftime(DateFormat.INPUT_DATE_FORMAT.value),
                end=end_date.strftime(DateFormat.INPUT_DATE_FORMAT.value),
            ),
        )
    else:
        out.insert(0, "There are no campsites available :(")
    return "\n".join(out), has_availabilities
