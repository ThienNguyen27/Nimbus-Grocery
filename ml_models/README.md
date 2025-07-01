1. **Create a Python virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate      # macOS/Linux
    venv\Scripts\activate.bat     # Windows
    ```

2. **[Windows only] Install Microsoft C++ Build Tools**
    - Download from [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    - During installation, select:
        - Desktop development with C++
        - Windows 10/11 SDK

3. **Install CMake**
    - macOS/Linux (with Homebrew):
      ```bash
      brew install cmake
      ```
    - Windows:
      - Download from [CMake downloads](https://cmake.org/download/), or use Chocolatey:
        ```bash
        choco install cmake
        ```

4. **Install required Python packages for person detection model**
    ```bash
    pip install cmake
    pip install face_recognition
    ```

5. **Install required Python packages for grocery dection model**
    ```bash
    cd ml_models/grocery-detection-model
    pip install -r requirements.txt
    ```
---

## 📷 Usage

To run person detection model:
```bash
cd ml_models/person-detection-model
python model.py
```