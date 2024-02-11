import json


def json_to_srt(input_file, output_file):
    with open(input_file, "r") as f:
        json_data = json.load(f)

    transcripts = json_data["results"]["transcripts"]
    items = json_data["results"]["items"]

    with open(output_file, "w") as f_out:
        index = 1
        for item in items:
            if item["type"] == "pronunciation":
                start_time = float(item["start_time"])
                end_time = float(item["end_time"])
                content = item["alternatives"][0]["content"]

                f_out.write(f"{index}\n")
                f_out.write(f"{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n")
                f_out.write(f"{content}\n\n")

                index += 1

def convert_to_srt_time(seconds):
    milliseconds = int(seconds * 1000)
    minutes, seconds = divmod(milliseconds // 1000, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds % 1000)


input_file = "newsTranscription.json"
output_file = "output.srt"
json_to_srt(input_file, output_file)
