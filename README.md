# 📦 imgcompress

A lightweight Python utility for easily compressing and uncompressing images. All core functionality is contained within a single file (`encompress.py`), making it incredibly simple to integrate into your existing projects.

## 🚀 Features

* **Simple API:** Everything is handled by just two main functions: `compress` and `uncompress`.
* **Adjustable Quality:** Control the exact compression ratio using a float value.
* **Plug & Play:** No complicated module setup or architecture. Just drop the script into your working directory.

## 📥 Installation

Simply clone the repository or download the `encompress.py` file directly into your project folder:

```bash
git clone https://github.com/avacado-a/imgcompress.git

```

## 💻 Usage

Make sure `encompress.py` is in the same directory as the script you are running, or properly added to your path.

### Compressing an Image

To compress an image, provide the source filename, the destination filename, and a `compressfactor` between `0` and `1`.

*Note: The lower the compression factor, the more compressed the image becomes, resulting in a lower quality uncompressed image.*

```python
from encompress import compress

filename = "original.png"        # Filename of the file you want to compress
tofilename = "compressed.png"    # Filename the compressed image goes to
compressfactor = 0.9             # Float between 0 and 1 representing compression level

compress(compressfactor, filename, tofilename)

```

### Uncompressing an Image

To reverse the process, use the `uncompress` function.

**⚠️ Important:** You must use the *exact same* `compressfactor` that was used to compress the original image, otherwise the decompression will not work correctly.

```python
from encompress import uncompress

filename = "compressed.png"      # Filename of the file you want to uncompress
tofilename = "uncompressed.png"  # Filename the uncompressed image goes to
compressfactor = 0.9             # Must match the factor used during compression!

uncompress(compressfactor, filename, tofilename)

```

## 📜 License

This project is open-source. Before using any code, please read the [LICENSE](https://www.google.com/search?q=LICENSE) file located in the root of the repository.
