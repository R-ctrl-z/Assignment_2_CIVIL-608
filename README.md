# Assignment 2: Research Skills in the Open Science Era

## Overview

This repository contains materials and instructions for Assignment 2 of CIVIL-608: Research Skills in the Open Science Era.

The script `contraction_scour_analysis.py` analyzes a dataset of flume experiments on contraction scour, compiled from the following studies:

1. Straub, L. G. (1934). [Effect of channel‐contraction works upon regimen of movable bed‐streams](https://doi.org/10.1029/TR015i002p00454). *Transactions American Geophysical Union*, 15(2), 454–463.
2. Ashida, K. (1963). *Study on the Stable Channel through Constrictions* (Annual Report).
3. Komura, S. (1966). [Equilibrium Depth of Scour in Long Constrictions](https://doi.org/10.1061/JYCEAJ.0001504). *Journal of the Hydraulics Division*, 92(5), 17–37.
4. Gill, M. A. (1981). [Bed Erosion in Rectangular Long Contraction](https://doi.org/10.1061/JYCEAJ.0005626). *Journal of the Hydraulics Division*, 107(3), 273–284.
5. Keller, R. J. (1983). *General scour in a long contraction*. Proceedings XX IAHR Congress, 2, 280–289.
6. Webby, M. G. (1984). *General scour at a contraction*. RRU 73, 109–118.
7. Rana, M. Y. (1986). *Flume experiments on sediment bed in steady non-uniform flow*. Asian Institute of Technology.
8. Lim, S.-Y. (1993). [Clear water scour in long contractions](https://doi.org/10.1680/iwtme.1993.23590). *Proceedings of the Institution of Civil Engineers - Water, Maritime and Energy*, 101(2), 93–98.
9. Lim, S.-Y., & Cheng, N.-S. (1998). *Scouring in Long Contraction*. *Journal of Irrigation and Drainage Engineering*, 124(5), 258–261.
10. Dey, S., & Raikar, R. V. (2005). [Scour in Long Contractions](https://doi.org/10.1061/(ASCE)0733-9429(2005)131). *Journal of Hydraulic Engineering*, 131(12), 1036–1049.
11. Weise, S. (2002). *Verifikation eines zweidimensionalen Feststofftransportmodells anhand von hydraulischen Versuchen*. Diplomarbeit, Fachhochschule für Technik, Wirtschaft und Kultur, Leipzig.
12. Oliveto, G., & Marino, M. C. (2019). [Morphological patterns at river contractions](https://doi.org/10.3390/w11081683). *Water*, 11(8), 1–11.
13. Singh, R. K., Pandey, M., Pu, J. H., Pasupuleti, S., & Villuri, V. G. K. (2020). [Experimental study of clear-water contraction scour](https://doi.org/10.2166/ws.2020.014). *Water Science and Technology: Water Supply*, 20(3), 943–952.
14. Nowroozpour, A., & Ettema, R. (2021). [Observations from Contraction–Scour Experiments Conducted with a Large Rectangular Channel](https://doi.org/10.1061/(asce)hy.1943-7900.0001903). *Journal of Hydraulic Engineering*, 147(8), 1–11.
15. Lagasse, P. F., Ettema R., DeRosset W. M., Nowroozpour A., & Clopper, P. E. (2021). *Revised Clear-Water and Live-Bed Contraction Scour Analysis*. National Cooperative Highway Research Program, National Academies of Sciences, Engineering, and Medicine.

This script analyzes contraction scour data from laboratory studies, focusing on both clear-water and live-bed scour regimes. It reads experimental data from a CSV file, computes relevant hydraulic and  sediment transport parameters, and applies several established contraction scour equations (Straub 1934, Komura 1966, Gill 1981, Lim and Cheng 1998) to predict flow depth at the contracted reach. The script then compares measured and computed values for each study and visualizes the results in a series of scatter plots.

## Contents

- `pyproject.toml`: Lists the Python dependencies required for the project.
- `uv.lock`: Contains locked dependency versions for reproducibility.
- `Data/`: Directory containing datasets used in the assignment.
- `Code/`: Source code for data analysis and figure generation.
- `Figures/`: Output figures generated from the analysis.
- `LICENSE`: License information for the project.

## Getting Started

### Dependencies

The dependencies are listed in the file `pyproject.toml` and in more detail in the file `uv.lock`.

### Installing

Before installing dependencies, ensure you have a Python distribution (e.g., [Python.org](https://www.python.org/downloads/)) and a code editor (such as [VS Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/)) installed on your system.

1. **Install dependencies:**  
    Use the following command in your terminal to install the required Python packages from `pyproject.toml`:

    ```bash
    pip install -r pyproject.toml
    ```

2. **Download project directories:**  
    Download the `Data/`, `Code/`, and `Figures/` directories and place them together in a folder of your choice.

### Running the Analysis

1. Navigate to the `Code/` directory.
2. Open `contraction_scour_analysis.py` in your preferred code editor or run it directly from the terminal:

    ```bash
    python contraction_scour_analysis.py
    ```

3. The script will automatically load the dataset from the `Data/` directory and generate the output figure, which will be saved in the `Figures/` directory.

### Data

The `Data/` directory contains the dataset in CSV format required to reproduce the analysis. The script `contraction_scour_analysis.py` will load this data automatically.

### Figures

The `Figures/` directory stores the figures generated by the analysis script.

## License

This project is licensed under the CC0 1.0 Universal License - see the `LICENSE` file for details.

## Author

[Romain Van Mol](romain.vanmol@epfl.ch)
