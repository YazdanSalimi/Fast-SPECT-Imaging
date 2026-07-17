"""
Supplementary code: intensity normalization of full-time and fast-acquisition images.

Self-contained script. Requires only numpy and SimpleITK:
    pip install numpy SimpleITK
"""

import numpy as np
import SimpleITK as sitk

def CopyInfo(ReferenceImage, UpdatingImage, origin=True, spacing=True, direction=True):
    """Copy spatial metadata (origin/spacing/direction) from a reference image."""
    if isinstance(ReferenceImage, str):
        ReferenceImage = sitk.ReadImage(ReferenceImage)
    if isinstance(UpdatingImage, str):
        UpdatingImage = sitk.ReadImage(UpdatingImage)

    UpdatedImage = UpdatingImage
    if origin:
        UpdatedImage.SetOrigin(ReferenceImage.GetOrigin())
    if spacing:
        UpdatedImage.SetSpacing(ReferenceImage.GetSpacing())
    if direction:
        UpdatedImage.SetDirection(ReferenceImage.GetDirection())
    return UpdatedImage


def sitk_percentile(image, percentile: float = 99.0, segment=None):
    """
    Compute the percentile of an image, optionally within a segmentation mask.

    Parameters:
        image: str, sitk.Image, or np.ndarray
        percentile: float, default 99.0
        segment: str, sitk.Image, or np.ndarray (optional mask)

    Returns:
        tuple: (percentile excluding zeros, percentile including zeros)
    """
    # Convert input to numpy array
    if isinstance(image, str):
        image_array = sitk.GetArrayFromImage(sitk.ReadImage(image))
    elif isinstance(image, sitk.Image):
        image_array = sitk.GetArrayFromImage(image)
    elif isinstance(image, np.ndarray):
        image_array = image
    else:
        raise TypeError("Image must be a path (str), sitk.Image, or numpy array.")

    # Apply segmentation mask if provided
    if segment is not None and segment != "none":
        if isinstance(segment, str):
            segment_array = sitk.GetArrayFromImage(sitk.ReadImage(segment))
        elif isinstance(segment, sitk.Image):
            segment_array = sitk.GetArrayFromImage(segment)
        elif isinstance(segment, np.ndarray):
            segment_array = segment
        else:
            raise TypeError("Segment must be a path (str), sitk.Image, or numpy array.")

        image_array = image_array[segment_array != 0]

    # Calculate percentiles
    non_zero_percentile = np.percentile(image_array[image_array != 0], percentile)
    with_zero_percentile = np.percentile(image_array, percentile)

    return non_zero_percentile, with_zero_percentile


def sitk_rescale(image, input_min="image-min", input_max="image-max",
                 output_min: float = 0.0, output_max: float = 1.0):
    """
    Rescale image intensities to a new range [output_min, output_max].
    Returns both clipped and unclipped versions.
    """
    if isinstance(image, str):
        image = sitk.ReadImage(image)

    array = sitk.GetArrayFromImage(image).astype(np.float32, copy=False)

    if input_min == "image-min":
        input_min = np.min(array)
    if input_max == "image-max":
        input_max = np.max(array)

    # Perform rescaling
    scale = (output_max - output_min) / (input_max - input_min)
    array = (array - input_min) * scale + output_min

    # Unclipped version
    image_no_clip = sitk.GetImageFromArray(array)
    image_no_clip = CopyInfo(ReferenceImage=image, UpdatingImage=image_no_clip)

    # Clipped version
    image_clip = sitk.GetImageFromArray(np.clip(array, output_min, output_max))
    image_clip = CopyInfo(ReferenceImage=image, UpdatingImage=image_clip)

    return image_clip, image_no_clip


# =============================================================================
# Normalization of full-time and fast-acquisition images
# =============================================================================

# Define file paths (update these with your actual paths)
ft_url = "path/to/fulltime_image.nii.gz"          # Full-time image

fast_10_url = "path/to/fast_10_image.nii.gz"
fast_20_url = "path/to/fast_20_image.nii.gz"
fast_25_url = "path/to/fast_25_image.nii.gz"
fast_50_url = "path/to/fast_50_image.nii.gz"

# Normalize using the 99th percentile (excluding zeros) as the upper bound.
# sitk_rescale returns (clipped, unclipped); [1] selects the unclipped version.
ft_normalized = sitk_rescale(
    ft_url,
    input_min=0,
    input_max=sitk_percentile(ft_url, percentile=99)[0],
)[1]

fast_normalized_10 = sitk_rescale(
    fast_10_url,
    input_min=0,
    input_max=sitk_percentile(fast_10_url, percentile=99)[0],
)[1]

fast_normalized_20 = sitk_rescale(
    fast_20_url,
    input_min=0,
    input_max=sitk_percentile(fast_20_url, percentile=99)[0],
)[1]

fast_normalized_25 = sitk_rescale(
    fast_25_url,
    input_min=0,
    input_max=sitk_percentile(fast_25_url, percentile=99)[0],
)[1]

fast_normalized_50 = sitk_rescale(
    fast_50_url,
    input_min=0,
    input_max=sitk_percentile(fast_50_url, percentile=99)[0],
)[1]

###
#writting the full time and fast-acquisition normalized images to disk.
###
