from pathlib import Path


def prompt_env(name: str, default: str = "") -> str:
    val = input(f"Enter {name} (default: {default}): ") or default
    return val


def main() -> None:
    print("Setup wizard for .env file")
    env_path = Path(".env")
    data = {
        "TZ": "Asia/Tokyo",
        "OPENAI_API_KEY": "",
        "TELEGRAM_BOT_TOKEN": "",
        "TELEGRAM_CHAT_ID": "",
    }
    for key, default in data.items():
        data[key] = prompt_env(key, default)
    with env_path.open("w", encoding="utf-8") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")
    print(
        "Written .env file. Configure same variables in GitHub Secrets if using Actions."
    )


if __name__ == "__main__":
    main()
