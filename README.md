# Transcript Tool

This project is designed to fetch the transcript of long-form online videos (including those over 60 hours). It utilizes audio extraction, chunking, and transcription techniques to handle lengthy videos efficiently.

## Features

- Download and process audio from video links.
- Split audio into manageable chunks for transcription.
- Transcribe audio chunks using advanced speech recognition libraries.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Jitendra-GRL/transcript-tool.git
   ```

2. Navigate to the project directory:
   ```
   cd transcript-tool
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To fetch the transcript of a video, run the main script:

```
python src/main.py <Video-URL>
```

Replace `<Video-URL>` with the URL of the video you want to transcribe.

### Example

```
python src/main.py "https://example.com/video" --chunk-size 300 --model-size large-v3
```

## Configuration

Configuration settings, such as file paths, can be found in `src/config/settings.py` (if applicable).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.