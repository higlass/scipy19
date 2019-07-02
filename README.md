# Demos from our Scipy 2019 talk

Notebooks are 

## Getting started

#### Requirements

- Conda (**latest version!**)

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
