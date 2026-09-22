from pathlib import Path

from convert_mri import convert_dicom_to_nifti
from resampling import resample_nifti
from n4_correction import n4_bias_correction
from brain_extraction import brain_extraction


def run_pipeline(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. DICOM -> NIfTI
    nifti_path = output_dir / "mri.nii.gz"

    print("\n[1/4] Converting DICOM to NIfTI...")
    convert_dicom_to_nifti(
        input_dir,
        nifti_path,
    )

    # 2. N4 bias field correction
    n4_path = output_dir / "mri_n4.nii.gz"

    print("\n[2/4] Applying N4 bias field correction...")
    n4_bias_correction(
        nifti_path,
        n4_path,
    )

    # 3. Resampling
    resampled_path = output_dir / "mri_resampled.nii.gz"

    print("\n[3/4] Resampling MRI...")
    resample_nifti(
        n4_path,
        resampled_path,
        voxel_size=(2, 2, 2),
    )

    # 4. Brain extraction
    brain_path = output_dir / "brain.nii.gz"

    print("\n[4/4] Performing brain extraction...")
    brain_extraction(
        n4_path,
        brain_path,
        fractional_threshold=0.5,
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline(
        "data/input/MR",
        "data/output",
    )
