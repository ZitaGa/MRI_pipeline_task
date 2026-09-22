from pathlib import Path

import SimpleITK as sitk


def n4_bias_correction(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = sitk.ReadImage(str(input_path), sitk.sitkFloat32)

    # Create a foreground mask using Otsu thresholding.
    mask = sitk.OtsuThreshold(image, 0, 1, 200)

    corrector = sitk.N4BiasFieldCorrectionImageFilter()

    # Limit the number of iterations to keep the processing time reasonable.
    corrector.SetMaximumNumberOfIterations([20, 10, 5])

    corrected_image = corrector.Execute(image, mask)

    sitk.WriteImage(corrected_image, str(output_path))

    print(f"N4-corrected image saved to: {output_path}")

    return corrected_image


if __name__ == "__main__":
    n4_bias_correction(
        "data/output/mri.nii.gz",
        "data/output/mri_n4.nii.gz",
    )
