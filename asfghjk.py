import speech_recognition as sr
import subprocess
import platform


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


def execute_command(command):
    if command is None:
        return

    if "open telegram" in command:
        system = platform.system()
        try:
            if system == "Windows":
                # Adjust the path to where Telegram is installed
                subprocess.run(["start", "telegram"], shell=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Telegram"])
            elif system == "Linux":
                subprocess.run(["telegram-desktop"])
            print("Opening Telegram...")
        except Exception as e:
            print(f"Failed to open Telegram: {e}")
    else:
        print("Command not recognized.")


def main():
    while True:
        command = recognize_speech()
        execute_command(command)


if __name__ == "__main__":
    main()
