"""
Generate dummy panoramic images for testing
"""
import cv2
import numpy as np

# Panoramic image size (standard 512x1024 for Structured3D)
height, width = 512, 1024

# Create a simple gradient panorama (simulating walls/ceiling/floor)
panorama = np.zeros((height, width, 3), dtype=np.uint8)

# Sky/ceiling - light blue gradient
panorama[0:height//3, :] = [200, 220, 255]

# Walls - varied colors for different directions
# North wall (left quarter)
panorama[height//3:2*height//3, 0:width//4] = [180, 200, 180]
# East wall
panorama[height//3:2*height//3, width//4:width//2] = [200, 180, 180]
# South wall
panorama[height//3:2*height//3, width//2:3*width//4] = [180, 190, 200]
# West wall
panorama[height//3:2*height//3, 3*width//4:width] = [190, 180, 190]

# Floor - brown/beige
panorama[2*height//3:height, :] = [150, 160, 140]

# Add some texture/variation
noise = np.random.randint(-15, 15, (height, width, 3), dtype=np.int16)
panorama = np.clip(panorama.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Add a window (bright rectangle on one wall)
cv2.rectangle(panorama, (120, 180), (220, 280), (240, 240, 255), -1)
cv2.rectangle(panorama, (120, 180), (220, 280), (100, 100, 150), 2)

# Add some furniture-like rectangles
cv2.rectangle(panorama, (400, 320), (500, 400), (140, 120, 100), -1)  # Table
cv2.rectangle(panorama, (700, 340), (780, 420), (120, 100, 80), -1)   # Chair

# Save full version
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/rgb_rawlight.png', panorama)
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/rgb_coldlight.png', panorama)
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/rgb_warmlight.png', panorama)

# Create simplified empty version (no furniture)
panorama_empty = panorama.copy()
# Remove furniture rectangles by painting over with wall color
cv2.rectangle(panorama_empty, (400, 320), (500, 400), (180, 160, 150), -1)
cv2.rectangle(panorama_empty, (700, 340), (780, 420), (180, 160, 150), -1)
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/empty/rgb_rawlight.png', panorama_empty)

# Create semantic segmentation (color-coded room types)
semantic = np.zeros((height, width, 3), dtype=np.uint8)
semantic[0:height//3, :] = [96, 0, 0]        # Ceiling - class 0
semantic[height//3:2*height//3, :] = [0, 0, 96]  # Walls - class 1
semantic[2*height//3:height, :] = [0, 96, 0]  # Floor - class 2
# Window
cv2.rectangle(semantic, (120, 180), (220, 280), [192, 0, 0], -1)  # Window - class 3
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/semantic.png', semantic)

# Create instance segmentation
instance = np.zeros((height, width, 3), dtype=np.uint8)
instance[:, :] = [0, 0, 0]  # Background
# Different colors for different object instances
cv2.rectangle(instance, (400, 320), (500, 400), [255, 0, 0], -1)  # Instance 1
cv2.rectangle(instance, (700, 340), (780, 420), [0, 255, 0], -1)  # Instance 2
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/instance.png', instance)

# Create depth map (distance from camera)
depth = np.ones((height, width), dtype=np.float32) * 3.0  # 3 meters baseline
depth[0:height//3, :] = 2.5       # Ceiling closer
depth[2*height//3:height, :] = 1.2  # Floor closer
# Save as 16-bit PNG (common format for depth)
depth_uint16 = (depth * 1000).astype(np.uint16)  # Convert to millimeters
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/depth.png', depth_uint16)

# Create normal map (surface normals)
normal = np.zeros((height, width, 3), dtype=np.uint8)
normal[0:height//3, :] = [128, 128, 0]        # Ceiling points down [0,0,-1]
normal[height//3:2*height//3, :] = [128, 255, 128]  # Walls point inward (various)
normal[2*height//3:height, :] = [128, 128, 255]  # Floor points up [0,0,1]
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/normal.png', normal)

# Create albedo (surface color without lighting)
albedo = panorama.copy()
cv2.imwrite('dummy_dataset/scene_00000/2D_rendering/0/panorama/full/albedo.png', albedo)

print("✅ Generated panoramic images:")
print("   - RGB images (raw, cold, warm light)")
print("   - Semantic segmentation")
print("   - Instance segmentation")
print("   - Depth map")
print("   - Normal map")
print("   - Albedo map")
