import requests
import json


# TODO: create tests


def send_weather_msg(webhookurl, measurements, *, standards=None, indexes=None, bot_name='weather'):
    redacted_message = "Current weather: \n"
    embed = {}
    embed["title"] = "Weather"

    for key, value in measurements.items():
        redacted_message += f"{key:<12}: {value};\n"

        # check if value exceeds limits given in standards list
        if standards:
            for standard in standards:
                if key in standard['pollutant']:
                    redacted_message += f"{key} {standard['name']} standard: {standard['limit']};"
                    redacted_message += '\n\n'

    if indexes:
        for value in indexes:
            redacted_message += f"{value['name']:<12} level of toxins in the air: {value['level']}\n"
            embed['color'] = int(value['color'][1:], 16)

    embed['description'] = redacted_message
    send_msg(webhookurl, embed=embed, bot_name=bot_name)


def send_msg(webhookurl, message="@here Your info is here!", *, embed=None, bot_name='temp'):
    data = {}
    data['content'] = message
    data['username'] = bot_name
    if embed:
        data['embeds'] = []
        data['embeds'].append(embed)

    result = requests.post(webhookurl, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        # print("Payload delivered successfully, code {}.".format(result.status_code))
        pass
