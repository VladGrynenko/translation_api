# This is a sample Python script.
import uvicorn

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from api.api import create_app


def main():
    print("I am in main")
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("Vovochka, Taniushka and me will be ok")
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
