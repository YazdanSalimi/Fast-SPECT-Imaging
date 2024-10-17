from setuptools import setup, find_packages

setup(
    name="Fast-SPECT",
    #version="0.1.0",
    author="Yazdan Salimi",
    author_email="salimiyazdan@gmail.com",
    description="functions to facilitate deep learning enhancement of fast or low dose SPECT images",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YazdanSalimi/Fast-SPECT-Imaging",
    packages=find_packages(),
    py_modules=["DL_inference", "image_utils"],
    install_requires=[
        "pandas",
        "tqdm",
        "termcolor",
        "glob2", 
        "torch",
        "SimpleITK",
        "multiprocess",
        "numpy", 
        "natsort", 
        "monai", 
        "nibabel", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
