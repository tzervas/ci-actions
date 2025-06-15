import subprocess
import sys

def optimize_image(image_name):
    subprocess.run(["docker-slim", "build", image_name], check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python optimize_image.py <image-name>")
        sys.exit(1)
    optimize_image(sys.argv[1])
