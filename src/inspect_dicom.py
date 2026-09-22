from pathlib import Path
from pydicom import dcmread


def inspect_dicom(folder_path):
    folder = Path(folder_path)
    dicom_files = list(folder.glob("*.dcm"))

    print(f"Number of DICOM files found: {len(dicom_files)}")

    if not dicom_files:
        print("No DICOM files found in the specified folder.")
        return

    datasets = [dcmread(file) for file in dicom_files]

    modalities = {ds.Modality for ds in datasets}
    series_uids = {ds.SeriesInstanceUID for ds in datasets}
    dimensions = {(ds.Rows, ds.Columns) for ds in datasets}
    pixel_spacings = {tuple(float(x) for x in ds.PixelSpacing) for ds in datasets}
    orientations = {
        tuple(float(x) for x in ds.ImageOrientationPatient) for ds in datasets
    }
    slice_thicknesses = {float(ds.SliceThickness) for ds in datasets}

    print(f"Modality: {modalities}")
    print(f"Number of series: {len(series_uids)}")
    print(f"Image dimensions: {dimensions}")
    print(f"Pixel spacing: {pixel_spacings}")
    print(f"Number of unique orientations: {len(orientations)}")
    print(f"Slice thicknesses: {slice_thicknesses}")


if __name__ == "__main__":
    inspect_dicom("data/input/MR")
