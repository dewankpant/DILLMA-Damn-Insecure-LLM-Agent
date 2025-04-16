# 🕵️ DILLMA - Damn Insecure LLM Agent

DILLMA is a deliberately insecure chatbot built with Flask, designed for educational use in LLM and web security. It's meant to help researchers, educators, and security enthusiasts explore the vulnerabilities of modern LLM applications in a safe, local environment.

This project can be used in workshops, CTFs, or personal research projects to simulate attacks, test LLM misbehavior, and understand prompt-based threats in real-time.

---

## 🚀 Features

- **Interactive Chat Interface**: Talk to the bot via a simple web-based UI.
- **Intentional LLM Vulnerabilities**: Simulates real-world risks like prompt injection, sensitive data leakage, and role confusion.
- **Flag Submission System**: Submit flags for discovered vulnerabilities to track and gamify learning progress.
- **Easy-to-Deploy Environment**: Fully containerized with Docker for fast setup.
- **Educational Focus**: Designed for security students, professionals, and trainers.

---

## 🧰 Setup & Installation

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your system.
- A stable internet connection (required to fetch the model and dependencies).

### Clone & Build

Clone the repository and build the Docker image:

```bash
git clone https://github.com/yourusername/dillma-chatbot.git
cd dillma-chatbot
docker build -t dillma-chatbot .
```

### Run the App

Launch the application locally:

```bash
docker run -p 8000:8000 dillma-chatbot
```

Once the container starts, open your browser and navigate to:

```
http://localhost:8000
```

You should see the chatbot interface ready for use.

---

## 🕹 Usage

- **Chat Freely**: Type messages to the bot and observe its behavior.
- **Explore Known Vulnerabilities**: Try prompt injections, manipulation, or attempts to bypass filters.
- **Submit Flags**: After discovering a vulnerability, use the flag submission feature to record your findings.
- **Track Challenges**: Flags may correspond to various types of vulnerabilities, so approach the app like a mini-CTF.

---

## 🤖 Model Details

The chatbot is powered by the **Mistral-7B** language model. During the Docker build, it is downloaded automatically from [Hugging Face](https://huggingface.co/).

Model use is local only, no external API calls are made at runtime.

---

## 🙌 Contributing

We welcome contributions from the security and AI communities!

To contribute:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push and open a pull request (PR)

Feel free to open issues for feature suggestions, bug reports, or ideas for new vulnerabilities to include.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full terms.

---

## 📬 Contact

Questions, issues, or collaboration ideas?

Feel free to open an issue on GitHub.

---

Happy Hacking! 🤖

