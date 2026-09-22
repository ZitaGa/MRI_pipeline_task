from pathlib import Path

import nibabel as nib
from nibabel.processing import resample_to_output


def resample_nifti(input_path, output_path, voxel_size=(2, 2, 2)):
    image = nib.load(input_path)

    original_voxel_size = image.header.get_zooms()[:3]

    print(f"Original voxel size: {original_voxel_size}")
    print(f"Original shape: {image.shape}")

    resampled = resample_to_output(image, voxel_sizes=voxel_size, order=1)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    nib.save(resampled, output_path)

    print(f"New voxel size: {resampled.header.get_zooms()[:3]}")
    print(f"New shape: {resampled.shape}")

    return resampled


if __name__ == "__main__":
    resample_nifti(
        "data/output/mri.nii.gz",
        "data/output/mri_resampled.nii.gz",
        voxel_size=(2, 2, 2),
    )
