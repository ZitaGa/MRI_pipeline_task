# MRI Preprocessing Pipeline

A Python-based pipeline for basic MRI preprocessing.

## Pipeline

The project performs the following steps:

1. **DICOM → NIfTI conversion**
   Converts a DICOM MRI series into a NIfTI volume.

2. **N4 bias field correction**
   Corrects low-frequency intensity inhomogeneity using the N4 Bias Field Correction algorithm implemented in SimpleITK.

3. **Resampling**
   Resamples the MRI volume to 2 × 2 × 2 mm voxel size using linear interpolation.

4. **Brain extraction**
   Extracts the brain using FSL BET and produces both a brain-extracted image and a brain mask.

5. **Visualization**
   Provides a simple visualization of sagittal, coronal and axial MRI views for quality control.

## Project Structure

```text
mri-pipeline-task/
├── data/
│   ├── input/
│   └── output/
├── src/
│   ├── convert_mri.py
│   ├── visualize_mri.py
│   ├── resampling.py
│   ├── n4_correction.py
│   ├── brain_extraction.py
│   └── pipeline.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

Input data and generated outputs are excluded from version control.

## Requirements

* Python 3
* pydicom
* NiBabel
* NumPy
* SciPy
* Matplotlib
* SimpleITK
* FSL (required for brain extraction)

FSL must be installed separately and the `bet` command must be available in the system PATH.

## Usage

Place a DICOM series in:

```text
data/input/MR/
```

Run the complete pipeline with:

```bash
python src/pipeline.py
```

The processed images will be saved to:

```text
data/output/
```