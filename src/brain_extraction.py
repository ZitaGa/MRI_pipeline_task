from pathlib import Path
import subprocess


def brain_extraction(input_path, output_path, fractional_threshold=0.3):
    input_path = Path(input_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "bet",
            str(input_path),
            str(output_path),
            "-m",
            "-f",
            str(fractional_threshold),
        ],
        check=True,
    )

    mask_path = output_path.parent / (
        output_path.name.replace(".nii.gz", "") + "_mask.nii.gz"
    )

    print(f"Brain-extracted image saved to: {output_path}")
    print(f"Brain mask saved to: {mask_path}")

    return output_path, mask_path


if __name__ == "__main__":
    brain_extraction(
        "data/output/mri.nii.gz",
        "data/output/brain.nii.gz",
        fractional_threshold=0.5,
    )
