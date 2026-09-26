import requests

# only permit predefined trusted destinations
ALLOWED_URLS = {
    "1": "https://www.example.com",
    "2": "https://www.example.org"
}

print("Choose an approved website:")
print("1. Example")
print("2. Example Organization")

choice = input("Enter 1 or 2: ")

if choice not in ALLOWED_URLS:
    print("Invalid selection")

else:
    # get the URL from the approved list
    url = ALLOWED_URLS[choice]

    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False
        )

        response.raise_for_status()

        print(response.text)

    except requests.RequestException:
        print("Unable to retrieve the page")