# Contributing to Vitae

Thank you for your interest in contributing to Vitae!

This project is owned and maintained by the UEFS's LASIC (Intelligent and Cognitive Systems Lab). We welcome contributions from anyone who wants to help improve the project.

## How to Contribute

1. **Fork the repository**
   Create your own copy of the project by forking the repository on GitHub.

2. **Clone your fork**
   Clone your forked repository to your local machine:

   ```
   git clone https://github.com/lasicuefs/curricFilter
   ```

3. **Create a branch**
   Make your changes in a separate branch:

   ```
   git checkout -b my-feature-branch
   ```

4. **Make your changes**
   Implement your feature or fix the bug. Please follow the existing code style and conventions. Follow clean-code principles preferably.

5. **Test your changes**
   Ensure your changes do not break existing functionality and work as expected.

6. **Commit your changes**
   Write clear, concise commit messages. Avoid "semantic commits", instead [follow this guide](https://cbea.ms/git-commit/):

   ```
   git commit -m "Description of your changes"
   ```

7. **Push to your fork**

   ```
   git push origin my-feature-branch
   ```

8. **Open a Pull Request**
   Go to the original repository and open a pull request from your fork and branch.

## Code of Conduct

Please be kind, ensuring a respectful and collaborative environment.

## Project Structure

* `queries/`: Helpful queries that may be interesting to be saved.
* `scripts/`: Helpful scripts to manage the project.
* `tests/`: Some tests are placed here to avoid polluting the source-code, others are placed along-side with the source.
* `vitae/`: Source code of the project. Read its Read-me to get more information about this.
* `build.py`: Build system to create non-technical user desktop application. Its entry is `vitae/app.py`.

## Questions?

If you have any questions or need help, feel free to open an issue or contact the maintainers.

Thank you for helping improve Vitae!
