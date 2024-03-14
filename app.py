from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

@app.route('/get_transcript/<string:video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript_data])
        return jsonify({'transcript': transcript_text})
    except Exception as e:
        return jsonify({'error': str(e)})

# Load the T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

@app.route('/summarize_transcript', methods=['POST'])
def summarize_transcript():
    try:
        # Get the transcript from the request
        data = request.get_json()
        transcript = data.get('transcript')

        # Tokenize and summarize the transcript
        inputs = tokenizer("summarize: " + transcript, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/summarize', methods=['GET'])
def summarize_youtube_video():
    try:
        # Extract YouTube video URL from query params
        youtube_url = request.args.get('youtube_url')

        # Get the transcript for the given YouTube video
        video_id = youtube_url.split('v=')[-1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript_data])

        # Tokenize and summarize the transcript
        inputs = tokenizer("summarize: " + transcript_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({'summarized_transcript': summary})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

