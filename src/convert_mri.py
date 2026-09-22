from pathlib import Path

import nibabel as nib
import numpy as np
from pydicom import dcmread


INPUT_DIR = Path("data/input/MR")
OUTPUT_PATH = Path("data/output/mri.nii.gz")


def convert_dicom_to_nifti(input_dir, output_path):
    # Load DICOM files
    dicom_files = list(input_dir.glob("*.dcm"))

    if not dicom_files:
        raise FileNotFoundError(f"No DICOM files found in {input_dir}")

    datasets = [dcmread(file) for file in dicom_files]

    # Sort slices by their physical position
    datasets.sort(key=lambda ds: ds.ImagePositionPatient[2])

    # Create 3D volume
    volume = np.stack([ds.pixel_array for ds in datasets])

    # Extract image geometry from DICOM
    orientation = np.array(datasets[0].ImageOrientationPatient, dtype=float)

    row_direction = orientation[:3]
    col_direction = orientation[3:]

    slice_direction = np.cross(row_direction, col_direction)

    pixel_spacing = np.array(datasets[0].PixelSpacing, dtype=float)

    positions = np.array([ds.ImagePositionPatient for ds in datasets])

    # Calculate distance between adjacent slices
    slice_spacing = np.linalg.norm(positions[1] - positions[0])

    row_vector = row_direction * pixel_spacing[0]
    col_vector = col_direction * pixel_spacing[1]
    slice_vector = slice_direction * slice_spacing

    # DICOM uses LPS coordinates, while NIfTI uses RAS
    lps_to_ras = np.diag([-1, -1, 1, 1])

    affine_lps = np.eye(4)
    affine_lps[:3, 0] = slice_vector
    affine_lps[:3, 1] = row_vector
    affine_lps[:3, 2] = col_vector
    affine_lps[:3, 3] = positions[0]

    affine = lps_to_ras @ affine_lps

    # Create and save NIfTI image
    nifti_image = nib.Nifti1Image(volume, affine)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nifti_image, output_path)

    return nifti_image


if __name__ == "__main__":
    nifti_image = convert_dicom_to_nifti(INPUT_DIR, OUTPUT_PATH)

    print(f"Saved NIfTI to: {OUTPUT_PATH}")
    print(f"Shape: {nifti_image.shape}")
    print(f"Voxel sizes: {nifti_image.header.get_zooms()[:3]}")
    print(f"Orientation: {nib.aff2axcodes(nifti_image.affine)}")
