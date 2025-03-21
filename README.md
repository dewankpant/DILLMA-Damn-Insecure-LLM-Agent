# DILLMA-Damn-Insecure-LLM-Agent

This project is a Flask-based web application that simulates a vulnerable chatbot for educational purposes.

## Features

- **Chat Interface**: Interact with the chatbot through a web-based interface.
- **Vulnerabilities**: Simulate various security vulnerabilities for learning purposes.
- **Flag Submission**: Submit flags for discovered vulnerabilities.

## Setup and Installation

### Prerequisites

- Docker installed on your machine.
- Internet connection to download the model and dependencies.

### Building the Docker Image

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/dillma-chatbot.git
   cd dillma-chatbot
   ```

2. Build the Docker image:

   ```bash
   docker build -t dillma-chatbot .
   ```

### Running the Application

1. Run the Docker container:

   ```bash
   docker run -p 8000:8000 dillma-chatbot
   ```

2. Access the application in your web browser at `http://localhost:8000`.

## Usage

- **Chat with the Bot**: Use the chat interface to interact with the bot.
- **Explore Vulnerabilities**: Try to find and exploit vulnerabilities to learn about web security.
- **Submit Flags**: Use the flag submission page to submit flags for vulnerabilities you discover.

## Model

The application uses the Mistral-7B model, which is automatically downloaded during the Docker build process from Hugging Face.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [your-email@example.com](mailto:your-email@example.com).
