# Demos from our Scipy 2019 talk

**Slides**: [slides.pdf](slides.pdf)

**Demos**:
- [basic-setup.ipynb](basic-setup.ipynb): Simplest example possible to check that HiGlass loads properly in Jupyter Lab.
- [temperature.ipynb](temperature.ipynb): Introduction to the python API for HiGlass using temperature measurements over the last \~50 years.
- [point-data.ipynb](point-data.ipynb): An example of how the tileset API works and how one can build their own API from scratch.
- [nyc-taxi.ipynb](nyc-taxi.ipynb): Demonstrate advanced features using the NYC Taxi dataset.
- [genomics.ipynb](genomics.ipynb): Show how to work with and extend published HiGlass dashboards for collaboration and reproducibility.

## Getting started

#### Requirements

- Conda `v4.6.14` (or higher)
- FUSE: [libfuse](https://github.com/libfuse/libfuse) `v2.9.7` (or higher) or [OSXFUSE](https://osxfuse.github.io/) `v3.9.2` (or higher)

_Other versions might work too but we only tested the above mentioned versions._

#### Installation

First, install the environment:

```
git clone https://github.com/higlass/scipy19
cd scipy19
conda env create -f environment.yml
```

Next, install HiGlass' jupyter extension:

```
conda activate higlass-scipy19
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install higlass-jupyter
```

Finally, start Jupyterlab:

```
jupyter-lab
```

## Trouble shooting

- If Conda fails to set up the environment please make sure you're using the latest version of Conda and update if necessary using:

   ```
   conda update -n base conda
   ```
   
   - If you end up with a half-created environment:
   
   ```
   CondaValueError: prefix already exists: /Users/me/miniconda3/envs/higlass-scipy19
   ```
   
   - You may have to delete it before continuing:
   
   ```
   $ rm -rf /Users/me/miniconda3/envs/higlass-scipy19
   ```

- If Conda seems to have gotten stuck, first check your processes using `top` or alike. Conda is dead slow these days and might just need some extra time. In the meantime you can make yourself a nice cup of coffee, go out for lunch, or head to Hawaii for your summer vacation.

- If starting HiGlass fails and you see an issue related to FUSE telling you a `RuntimeError` popped up with the following _super helpful and elaborate_ error message: `1`, then you most likely need to update FUSE. If HiGlass does start then you can ingore the error. The error goes away if you keep unmounting previously mounted values using `umount HttpFs`.

## References

**Weather Data:** The data was obtain from the National Centers for Environmental Information. https://www.ncei.noaa.gov/access/search/data-search/global-hourly

**Point Data:** The data is from Wang et al. Multiplexed imaging of high-density libraries of RNAs with MERFISH and expansion microscopy, _Nature Scientific Reports_, 2018.

**NYC Taxi Data:** The data is NYC Taxi & Limousine Commission, https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page.
