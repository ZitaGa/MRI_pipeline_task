import nibabel as nib
import matplotlib.pyplot as plt

image = nib.load("data/output/mri_n4.nii.gz")
data = image.get_fdata()

x, y, z = [size // 2 for size in data.shape]

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

slices = [
    data[x, :, :],
    data[:, y, :],
    data[:, :, z],
]

for ax, image_slice in zip(axes, slices):
    ax.imshow(image_slice, cmap="gray", origin="lower")
    ax.axis("off")

plt.tight_layout()
plt.show()
