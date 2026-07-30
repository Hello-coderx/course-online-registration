"""
Main Entry Point
Online Course Registration System
"""
import tkinter as tk
from gui import CourseRegistrationApp


def main():
    """Main function to launch the Course Registration System"""
    root = tk.Tk()
    app = CourseRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
