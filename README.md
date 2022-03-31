# Cloudbuster
3D imaging quantification workflow

Cloudbuster provides an open source workflow to reconstruct a 3D entity from slice recorded microscopical images with or without treatment with anti-migratory small molecule inhibitors. This reconstruction produces distinct point clouds as basis for subsequent comparison of basic readout parameters using average computer processor, memory, and graphics resources within an acceptable time frame.

Requirements

Python3

Download under: https://www.python.org/downloads/release/python-380 and follow installation instructions. Do NOT use the windows warehouse installer! This installation lacks important modules.

On Windows 10 It might be necessary to install:

microsoft visual c++ 2015 redistributable
microsoft visual c++ 2013 redistributable
microsoft visual c++ 2012 redistributable

Installation

When using pip for the installation of all Python modules/packages pip3 should be used for Linux.

When using pip Windows requires the installation with:
python -m pip install -U <package name> or
py -m pip install -U <package name>


skimage library:

Follow the installation instructions under: https://scikit-image.org/docs/dev/install.html
pip3 install scikit-image
e.g. for command line installation in Linux.
Open3D library:

Follow the installation instructions under https://pypi.org/project/open3d-python/
pip3 install open3d-python

numpy:

Follow the installation instructions under https://numpy.org/install/
pip3 install numpy

Matplotlib:

Follow the installation instructions under https://matplotlib.org/stable/users/installing.html
pip3 install -U matplotlib

PCA:

Follow the installation instructions under https://pypi.org/project/pca/
pip3 install pca

Kneed:
Follow the installation instructions under https://pypi.org/project/kneed/
pip3 install kneed

Pandas:
Follow the installation instructions under https://pypi.org/project/pandas/
pip3 install pandas

Scikit-learn:
Follow the installation instructions under https://scikit-learn.org/stable/install.html
pip3 install scikit-learn

wxpython:

Follow the installation instructions under https://wxpython.org/pages/downloads/index.html
pip3 install wxPython

wxpython additionally might require the installation of the gtk3+ library: https://www.gtk.org/docs/installations/ .
  
Download the files into a single folder.
  
Running the script:

Safe the script in your local folder, in a terminal window enter the folder and type: python3 Auswahl.py to start the selection script. Depending on your python installation under windows also the command py Auswahl.py might be correct. It might be necessary to add the full path to Auswahl.py on Mac.
  
