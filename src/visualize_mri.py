import nibabel as nib
import matplotlib.pyplot as plt


def plot_brain_extraction(image_path, mask_path):
    image = nib.load(image_path)
    mask = nib.load(mask_path)

    image_data = image.get_fdata()
    mask_data = mask.get_fdata()

    x, y, z = [size // 2 for size in image_data.shape]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    slices = [
        image_data[x, :, :],
        image_data[:, y, :],
        image_data[:, :, z],
    ]

    masks = [
        mask_data[x, :, :],
        mask_data[:, y, :],
        mask_data[:, :, z],
    ]

    for ax, image_slice, mask_slice in zip(axes, slices, masks):
        ax.imshow(image_slice, cmap="gray", origin="lower")
        ax.imshow(
            mask_slice,
            cmap="Reds",
            alpha=0.25,
            origin="lower",
        )
        ax.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_brain_extraction(
        "data/output/mri.nii.gz",
        "data/output/brain_mask.nii.gz",
    )
