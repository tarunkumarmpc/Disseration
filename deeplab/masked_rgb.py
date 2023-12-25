import cv2
import os
import glob

def apply_mask(rgb_image_path, semantic_image_path, output_folder):
    # Read the RGB image and semantic image
    rgb_img = cv2.imread(rgb_image_path)
    semantic_img = cv2.imread(semantic_image_path)

    # Create a binary mask from the semantic image where black pixels are set to 1 and the rest are set to 0
    mask = (semantic_img[:, :, 0] == 0) & (semantic_img[:, :, 1] == 0) & (semantic_img[:, :, 2] == 0)

    # Apply the mask to the RGB image
    rgb_img[mask] = 0

    # Save the masked RGB image
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, os.path.basename(rgb_image_path))
    cv2.imwrite(output_path, rgb_img)

    print(f'Saved masked RGB image: {output_path}')

# Example usage
rgb_folder = '/home/tarun/Documents/diss_deepvo/DeepVO-pytorch/DeepVO-pytorch-master/KITTI/images/06'
semantic_folder = '/home/tarun/Documents/fastsam/deeplab/semantic_images/06'
output_folder = '/home/tarun/Documents/fastsam/deeplab/outpt/06'

rgb_image_paths = sorted(glob.glob(os.path.join(rgb_folder, '*.png')))
semantic_image_paths = sorted(glob.glob(os.path.join(semantic_folder, '*.png')))

for rgb_image_path, semantic_image_path in zip(rgb_image_paths, semantic_image_paths):
    apply_mask(rgb_image_path, semantic_image_path, output_folder)
