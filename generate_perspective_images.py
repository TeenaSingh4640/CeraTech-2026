"""
Generate perspective images for testing
"""
import cv2
import numpy as np

# Create a simple perspective view (640x480 standard)
height, width = 480, 640
perspective = np.zeros((height, width, 3), dtype=np.uint8)

# Sky/ceiling gradient
for i in range(height//3):
    color = int(200 + i * 55.0 / (height//3))
    perspective[i, :] = [color, color, 255]

# Walls with perspective
perspective[height//3:2*height//3, :] = [180, 190, 200]

# Floor with depth gradient
for i in range(2*height//3, height):
    color = int(160 - (i - 2*height//3) * 20.0 / (height//3))
    perspective[i, :] = [color-10, color, color-10]

# Add some objects
cv2.rectangle(perspective, (200, 250), (350, 400), (120, 100, 80), -1)  # Table
cv2.rectangle(perspective, (450, 280), (550, 420), (140, 120, 100), -1)  # Chair

# Add noise for realism
noise = np.random.randint(-10, 10, (height, width, 3), dtype=np.int16)
perspective = np.clip(perspective.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Save all required perspective images
base_path = 'dummy_dataset/scene_00000/2D_rendering/0/perspective/full/0/'
cv2.imwrite(base_path + 'rgb_rawlight.png', perspective)

# Semantic
semantic = np.zeros((height, width, 3), dtype=np.uint8)
semantic[0:height//3, :] = [96, 0, 0]
semantic[height//3:2*height//3, :] = [0, 0, 96]
semantic[2*height//3:height, :] = [0, 96, 0]
cv2.imwrite(base_path + 'semantic.png', semantic)

# Instance
instance = np.zeros((height, width, 3), dtype=np.uint8)
cv2.rectangle(instance, (200, 250), (350, 400), [255, 0, 0], -1)
cv2.rectangle(instance, (450, 280), (550, 420), [0, 255, 0], -1)
cv2.imwrite(base_path + 'instance.png', instance)

# Depth
depth = np.ones((height, width), dtype=np.float32) * 2.5
depth_uint16 = (depth * 1000).astype(np.uint16)
cv2.imwrite(base_path + 'depth.png', depth_uint16)

# Normal
normal = np.zeros((height, width, 3), dtype=np.uint8)
normal[:, :] = [128, 128, 255]
cv2.imwrite(base_path + 'normal.png', normal)

# Albedo
cv2.imwrite(base_path + 'albedo.png', perspective)

print("✅ Generated perspective images")
