# Titulador: Image Processing and Metadata Management Application

AITAG AutomaticTitleTagger is a PyQt5-based desktop application for processing images, analyzing their content, and managing metadata. It provides a user-friendly interface for configuring settings, selecting directories, and executing image processing tasks.

The application integrates with OpenAI's GPT-4 model to analyze images and generate titles, keywords, and categories. It offers features such as recursive directory processing, file renaming, and metadata updating for JPEG images.

## Repository Structure

- `App/`: Contains the main application logic and view models
  - `ViewModel/`: View model classes for different components
  - `app_launcher.py`: Entry point for launching the application
- `Data/`: Manages configuration and environment settings
  - `config.json`: Application configuration file
  - `env_manager.py`: Handles environment variables and API keys
  - `json_manager.py`: Manages JSON data storage and retrieval
- `Logic/`: Core image processing and analysis functionality
  - `worker/`: Background processing worker
  - `file_manager.py`: File operations and CSV creation
  - `gpt4o_mini.py`: Integration with OpenAI's GPT-4 for image analysis
  - `image_processor.py`: Main image processing logic
  - `metadata_manager.py`: Updates image metadata
- `View/`: User interface components
  - `LeftPanel/`: Left panel widgets and components
  - `configuration_window/`: Configuration window and related views
  - `titulador_app.py`: Main application window
- `test/`: Unit tests for various components
- `main.py`: Application entry point

## Usage Instructions

### Installation

1. Ensure you have Python 3.10+ installed.
2. Clone the repository:
   ```
   git clone <repository_url>
   cd AutomaticTitleTagger
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
### Run the Application

Execute the following command in the project root:

```
python main.py
```

### Configuration

1. Set up your OpenAI API key:
- Open configuration and add your API key.
- This will create an .env file to store locally your API.

2. Configure allowed file extensions selecting those you want to process.

3. Add platform name (ex. AnyImageStock) and optionally system and user prompts, to give detailed instructions to the AI  

### Using the Application

1. Select the image directory using the "Explore" button.
2. Choose the platform (created before) from the dropdown menu.
3. Click "Run Titulador" to start processing images.
4. Monitor progress in the left panel.
5. A CSV will be created where the images are located, if recursive, CSV's will be in each folder with images on it.

### Troubleshooting

- If the application fails to start, ensure all dependencies are installed correctly.
- Check the console output for any error messages. (Status bar is not yet implemented)
- Verify that the OpenAI API key is set correctly in the `.env` file.
- If image processing fails, ensure the selected directory contains supported image formats.

## Data Flow

The Titulador application processes image data through the following steps:

1. User selects an image directory and platform through the UI.
2. The application scans the directory for supported image files.
3. Each image is processed by the `ImageProcessor`:
   - Image is resized and encoded.
   - GPT-4 analyzes the image using the `ImageAnalyzer`.
   - File is renamed based on the analysis.
   - Metadata is updated for JPEG files.
4. Progress is reported back to the UI.
5. Results are saved in a CSV file.

```
[User Input] -> [UI] -> [ImageProcessor] -> [ImageAnalyzer (GPT-4)] -> [Metadata Update] -> [CSV Output]
                 ^                                                            |
                 |                                                            |
                 +------------------------------------------------------------+
                                    Progress Updates
```

