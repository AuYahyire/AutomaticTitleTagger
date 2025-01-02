# Titulador: Image Processing and Metadata Management Application

Titulador is a PyQt5-based desktop application for processing images, analyzing their content, and managing metadata. It provides a user-friendly interface for configuring settings, selecting directories, and executing image processing tasks.

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

1. Ensure you have Python 3.7+ installed.
2. Clone the repository:
   ```
   git clone <repository_url>
   cd titulador
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

2. Configure allowed file extensions and platforms in `Data/config.json`

### Running the Application

Execute the following command in the project root:

```
python main.py
```

### Using the Application

1. Select the image directory using the "Explore" button.
2. Choose the platform from the dropdown menu.
3. Click "Run Titulador" to start processing images.
4. Monitor progress in the left panel.
5. Access the configuration window from the "File" menu to modify settings.

### Troubleshooting

- If the application fails to start, ensure all dependencies are installed correctly.
- Check the console output for any error messages.
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

## Testing

Run the test suite using pytest:

```
pytest
```

Key test files:
- `test_worker.py`: Tests for the background processing worker
- `test_gpt4o_mini.py`: Tests for the GPT-4 integration